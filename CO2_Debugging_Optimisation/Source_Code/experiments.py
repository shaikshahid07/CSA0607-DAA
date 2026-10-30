"""
Experiments for part (d): operation counts and run times, before vs after optimisation.

Every experiment uses a fixed random seed (SEED) so the numbers can be reproduced.
Each experiment also checks that all algorithms give the SAME answer on the data.

Run with:   python experiments.py        (takes a few minutes: the O(n^2) baselines are slow)
Results:    ../Supporting_Files/results/*.csv, ../Supporting_Files/graphs/*.png,
            ../Supporting_Files/execution_logs/experiments_log.txt
"""
import csv
import math
import random
import time
from pathlib import Path

import corrected_module as cor
import optimised_module as opt

SEED = 2026
ROOT = Path(__file__).resolve().parent.parent / "Supporting_Files"


def timed(fn, *args, **kwargs):
    """Return (result, seconds) for one call of fn."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, time.perf_counter() - t0


# ---------------------------------------------------------------- data generators
def make_alerts(n, rng, severities=10):
    return [(f"A{k}", rng.randint(1, severities)) for k in range(n)]


def make_nearly_sorted_alerts(n, rng, severities=10):
    """Highest-first order, then 1 % of the alerts are moved out of place by 1-10 positions
    (swaps only between alerts of DIFFERENT severity, so every swap really creates disorder)."""
    data = sorted(make_alerts(n, rng, severities), key=lambda a: a[1], reverse=True)
    done = 0
    while done < n // 100:
        k = rng.randrange(n - 10)
        d = rng.randint(1, 10)
        if data[k][1] != data[k + d][1]:
            data[k], data[k + d] = data[k + d], data[k]
            done += 1
    return data


def make_events(n, rng, size=1000.0):
    return [(rng.uniform(0, size), rng.uniform(0, size)) for _ in range(n)]


def count_original_style(events):
    """Re-runs the ORIGINAL loop structure (all n*n ordered pairs, incl. i == j) and counts the
    distance computations. Same arithmetic as the buggy code; used only for the 'before' baseline."""
    count = 0
    best = 0.0
    for i in range(len(events)):
        xi, yi = events[i]
        for j in range(len(events)):
            count += 1
            d = math.sqrt((xi - events[j][0]) ** 2 + (yi - events[j][1]) ** 2)
            if d > best:
                best = d
    return count


# ---------------------------------------------------------------- experiment 1: sorting
def exp_sort():
    rng = random.Random(SEED)
    rows = []
    cases = [("random", n) for n in (1000, 2000, 5000, 10000)] + \
            [("nearly sorted", n) for n in (1000, 5000, 10000, 50000)]
    for kind, n in cases:
        data = make_alerts(n, rng) if kind == "random" else make_nearly_sorted_alerts(n, rng)
        st_ins, st_tim = {}, {}
        res_ins, t_ins = timed(opt.insertion_sort_alerts, list(data), st_ins)
        res_tim, _ = timed(opt.sort_alerts_counted, data, st_tim)     # counting wrapper: for the count only
        _, t_tim = timed(opt.sort_alerts, data)                      # plain sort_alerts: for the run time
        assert res_ins == res_tim
        if n <= 2000:
            assert res_ins == cor.sort_alerts(list(data))
        rows.append(dict(data=kind, n=n, insertion_comparisons=st_ins["comparisons"],
                         insertion_shifts=st_ins["shifts"], insertion_seconds=round(t_ins, 4),
                         sorted_comparisons=st_tim["comparisons"], sorted_seconds=round(t_tim, 5)))
    # the production workload: 50,000 random alerts -> only the optimised sort is run
    data = make_alerts(50000, rng)
    st = {}
    opt.sort_alerts_counted(data, st)
    _, t = timed(opt.sort_alerts, data)
    n = 50000
    est = round(n * (n - 1) / 2 * 0.45)          # expected inversions: C(n,2) * P(s_i < s_j) = C(n,2) * 0.45
    rows.append(dict(data="random", n=n, insertion_comparisons=f"not run (estimate {est + n:,})",
                     insertion_shifts=f"estimate {est:,}", insertion_seconds="not run",
                     sorted_comparisons=st["comparisons"], sorted_seconds=round(t, 5)))
    return rows


# ---------------------------------------------------------------- experiment 2: blocklist
def exp_blocklist():
    rng = random.Random(SEED)
    rows = []
    for size in (1000, 10000, 100000):
        blocklist = [f"10.{k // 65536 % 256}.{k // 256 % 256}.{k % 256}" for k in range(size)]
        rng.shuffle(blocklist)
        # 1000 queries: half on the blocklist, half not
        queries = [rng.choice(blocklist) for _ in range(500)] + \
                  [f"192.168.{rng.randint(0, 255)}.{rng.randint(0, 255)}" for _ in range(500)]
        total = 0
        t0 = time.perf_counter()
        seq_answers = []
        for q in queries:
            st = {}
            seq_answers.append(opt.is_blocked_sequential(blocklist, q, st))
            total += st["comparisons"]
        t_seq = time.perf_counter() - t0
        index = opt.build_blocklist(blocklist)
        t0 = time.perf_counter()
        hash_answers = [opt.is_blocked(index, q) for q in queries]
        t_hash = time.perf_counter() - t0
        assert seq_answers == hash_answers
        assert hash_answers[:20] == [cor.is_blocked(blocklist, q) for q in queries[:20]]
        rows.append(dict(blocklist_size=size, queries=len(queries), sequential_comparisons=total,
                         hash_lookups=len(queries), sequential_seconds=round(t_seq, 4),
                         hash_seconds=round(t_hash, 6)))
    return rows


# ---------------------------------------------------------------- experiment 3: signature search
def exp_signature():
    """Random log over 27 symbols (A-Z and space) so that pattern letters really occur in the text,
    plus the adversarial worst case for brute force (log = AAAA...A, pattern = AA...AB)."""
    rng = random.Random(SEED)
    rows = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    n = 200000
    for pattern in ("FAIL", "BADLOGIN", "FAILEDLOGINROOTS"):
        chars = [rng.choice(alphabet) for _ in range(n)]
        for _ in range(40):                                   # plant 40 signatures
            pos = rng.randrange(n - len(pattern))
            chars[pos:pos + len(pattern)] = pattern
        log = "".join(chars)
        rows.append(_signature_row("random log", log, pattern))
    m = 8
    log, pattern = "A" * 10000, "A" * (m - 1) + "B"
    rows.append(_signature_row("worst case for brute force", log, pattern))
    return rows


def _signature_row(kind, log, pattern):
    st_b, st_h = {}, {}
    r_b, t_b = timed(opt.find_signature, log, pattern, st_b)
    r_h, t_h = timed(opt.find_signature_horspool, log, pattern, st_h)
    r_f, t_f = timed(opt.find_signature_builtin, log, pattern)
    r_c = cor.find_signature(log, pattern)
    assert r_b == r_h == r_f == r_c
    return dict(log_type=kind, log_length=len(log), pattern_length=len(pattern), occurrences=len(r_b),
                brute_comparisons=st_b["comparisons"], horspool_comparisons=st_h["comparisons"],
                brute_seconds=round(t_b, 4), horspool_seconds=round(t_h, 4), builtin_seconds=round(t_f, 6))


# ---------------------------------------------------------------- experiment 4: closest pair
def exp_closest(sizes=(1000, 2000, 4000, 8000)):
    rng = random.Random(SEED)
    rows = []
    for n in sizes:
        ev = make_events(n, rng)
        original_count, t_orig = timed(count_original_style, ev)
        st_b, st_p, st_d = {}, {}, {}
        (pair_b, d_b), t_b = timed(opt.closest_logins_bruteforce, ev, st_b)
        (pair_p, d_p), t_p = timed(opt.closest_logins, ev, st_p)
        (pair_d, d_d), t_d = timed(opt.closest_logins_dc, ev, st_d)
        assert pair_b == pair_p == pair_d and math.isclose(d_b, d_p) and math.isclose(d_b, d_d)
        assert original_count == n * n and st_b["distance_computations"] == n * (n - 1) // 2
        # the pruned / divide-and-conquer counts depend on the data, so also average 5 further random batches
        p_counts, d_counts = [], []
        for _ in range(5):
            extra = make_events(n, rng)
            sp, sd = {}, {}
            r_p = opt.closest_logins(extra, sp)
            r_d = opt.closest_logins_dc(extra, sd)
            assert r_p == r_d
            p_counts.append(sp["distance_computations"])
            d_counts.append(sd["distance_computations"])
        rows.append(dict(n=n, original_ordered_pairs=original_count,
                         corrected_bruteforce=st_b["distance_computations"],
                         optimised_pruned=st_p["distance_computations"],
                         divide_and_conquer=st_d["distance_computations"],
                         pruned_mean_of_5=round(sum(p_counts) / 5), dc_mean_of_5=round(sum(d_counts) / 5),
                         original_seconds=round(t_orig, 3), bruteforce_seconds=round(t_b, 3),
                         pruned_seconds=round(t_p, 4), dc_seconds=round(t_d, 4),
                         closest_pair=str(pair_b), closest_distance=round(d_b, 4)))
    return rows


def exp_closest_worst(sizes=(1000, 2000, 4000)):
    """Points on two vertical lines (x = 0 and x = 1000): the gap along x is 0 inside each line, so the
    simple pruning can never stop early. Divide and conquer keeps its O(n log n) guarantee."""
    rng = random.Random(SEED)
    rows = []
    for n in sizes:
        ev = [(0.0 if k % 2 == 0 else 1000.0, rng.uniform(0, 1000)) for k in range(n)]
        st_b, st_p, st_d = {}, {}, {}
        (pair_b, d_b), t_b = timed(opt.closest_logins_bruteforce, ev, st_b)
        (pair_p, d_p), t_p = timed(opt.closest_logins, ev, st_p)
        (pair_d, d_d), t_d = timed(opt.closest_logins_dc, ev, st_d)
        assert pair_b == pair_p == pair_d
        rows.append(dict(n=n, corrected_bruteforce=st_b["distance_computations"],
                         optimised_pruned=st_p["distance_computations"],
                         divide_and_conquer=st_d["distance_computations"],
                         bruteforce_seconds=round(t_b, 3), pruned_seconds=round(t_p, 3), dc_seconds=round(t_d, 4)))
    return rows


# ---------------------------------------------------------------- output helpers
def save_csv(name, rows):
    path = ROOT / "results" / name
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return path


def print_table(title, rows):
    print(f"\n{title}")
    cols = list(rows[0].keys())
    widths = [max(len(str(c)), *(len(str(r[c])) for r in rows)) for c in cols]
    print("  ".join(str(c).rjust(w) for c, w in zip(cols, widths)))
    for r in rows:
        print("  ".join(str(r[c]).rjust(w) for c, w in zip(cols, widths)))


def make_graphs(sort_rows, block_rows, sig_rows, closest_rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    g = ROOT / "graphs"

    # graph 1: closest pair distance computations (log-log)
    ns = [r["n"] for r in closest_rows]
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ax.plot(ns, [r["original_ordered_pairs"] for r in closest_rows], "o-", color="#c0392b", label="Original (n x n pairs)")
    ax.plot(ns, [r["corrected_bruteforce"] for r in closest_rows], "s-", color="#e67e22", label="Corrected brute force n(n-1)/2")
    ax.plot(ns, [r["optimised_pruned"] for r in closest_rows], "^-", color="#2471a3", label="Optimised (i<j, pruned)")
    ax.plot(ns, [r["divide_and_conquer"] for r in closest_rows], "d-", color="#1e8449", label="Divide and conquer")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Batch size n (login events)"); ax.set_ylabel("Distance computations")
    ax.set_title("closest_logins: distance computations vs batch size")
    ax.set_xticks(ns); ax.set_xticklabels([f"{n:,}" for n in ns]); ax.xaxis.set_minor_formatter(NullFormatter()); ax.grid(True, which="both", alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(g / "graph1_closest_pair_distance_computations.png", dpi=150); plt.close(fig)

    # graph 2: closest pair run time
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ax.plot(ns, [r["original_seconds"] for r in closest_rows], "o-", color="#c0392b", label="Original loop structure")
    ax.plot(ns, [r["bruteforce_seconds"] for r in closest_rows], "s-", color="#e67e22", label="Corrected brute force")
    ax.plot(ns, [r["pruned_seconds"] for r in closest_rows], "^-", color="#2471a3", label="Optimised (pruned)")
    ax.plot(ns, [r["dc_seconds"] for r in closest_rows], "d-", color="#1e8449", label="Divide and conquer")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Batch size n (login events)"); ax.set_ylabel("Run time (seconds)")
    ax.set_title("closest_logins: run time vs batch size")
    ax.set_xticks(ns); ax.set_xticklabels([f"{n:,}" for n in ns]); ax.xaxis.set_minor_formatter(NullFormatter()); ax.grid(True, which="both", alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(g / "graph2_closest_pair_run_time.png", dpi=150); plt.close(fig)

    # graph 3: insertion sort comparisons, random vs nearly sorted
    fig, ax = plt.subplots(figsize=(7, 4.4))
    for kind, color, marker in (("random", "#c0392b", "o"), ("nearly sorted", "#1e8449", "s")):
        pts = [(r["n"], r["insertion_comparisons"]) for r in sort_rows
               if r["data"] == kind and isinstance(r["insertion_comparisons"], int)]
        ax.plot(*zip(*pts), marker + "-", color=color, label=f"Insertion sort, {kind}")
    pts = [(r["n"], r["sorted_comparisons"]) for r in sort_rows if r["data"] == "random"]
    ax.plot(*zip(*pts), "^--", color="#2471a3", label="sorted() (Timsort), random")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Number of alerts n"); ax.set_ylabel("Severity comparisons")
    ax.set_title("sort_alerts: comparisons vs number of alerts")
    ax.grid(True, which="both", alpha=0.3); ax.legend(loc="lower right")
    fig.tight_layout(); fig.savefig(g / "graph3_sort_comparisons.png", dpi=150); plt.close(fig)

    # graph 4: signature search comparisons
    sig_rows = [r for r in sig_rows if r["log_type"] == "random log"]
    ms = [r["pattern_length"] for r in sig_rows]
    fig, ax = plt.subplots(figsize=(7, 4.4))
    xs = range(len(ms)); w = 0.38
    ax.bar([x - w / 2 for x in xs], [r["brute_comparisons"] for r in sig_rows], w, color="#e67e22", label="Brute force")
    ax.bar([x + w / 2 for x in xs], [r["horspool_comparisons"] for r in sig_rows], w, color="#2471a3", label="Horspool")
    ax.set_xticks(list(xs)); ax.set_xticklabels([f"m = {m}" for m in ms])
    ax.set_ylabel("Character comparisons")
    ax.set_title("find_signature: comparisons by pattern length"); ax.legend(); ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(g / "graph4_signature_comparisons.png", dpi=150); plt.close(fig)


def main():
    print(f"SentinelOps experiments, seed {SEED}")
    s = exp_sort(); print_table("E1  sort_alerts  (severity 1-10)", s)
    b = exp_blocklist(); print_table("E2  is_blocked  (1000 queries, half present)", b)
    g = exp_signature(); print_table("E3  find_signature  (random logs of 200,000 characters; last row = worst case for brute force)", g)
    c = exp_closest()
    print_table("E4a closest_logins: distance computations (random points in 1000 x 1000)",
                [{k: r[k] for k in ("n", "original_ordered_pairs", "corrected_bruteforce", "optimised_pruned",
                                    "divide_and_conquer", "pruned_mean_of_5", "dc_mean_of_5")} for r in c])
    print_table("E4b closest_logins: run time in seconds and the closest pair found",
                [{k: r[k] for k in ("n", "original_seconds", "bruteforce_seconds", "pruned_seconds",
                                    "dc_seconds", "closest_pair", "closest_distance")} for r in c])
    w = exp_closest_worst()
    print_table("E4c closest_logins WORST CASE for simple pruning: points on two vertical lines", w)
    for name, rows in (("sort_alerts.csv", s), ("is_blocked.csv", b), ("find_signature.csv", g),
                       ("closest_logins.csv", c), ("closest_logins_worst_case.csv", w)):
        save_csv(name, rows)
    make_graphs(s, b, g, c)
    print("\nAll algorithms agreed on every dataset. CSV files and graphs saved.")


if __name__ == "__main__":
    main()
