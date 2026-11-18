"""Q2 - Sequential search on aircraft tool-issue records. Run: python q2_sequential_search.py"""
import random, time, json, csv, os, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def make_records(n, seed=1):
    rnd = random.Random(seed)
    ids = list(range(1, n + 1)); rnd.shuffle(ids)
    # (ToolID, TechnicianID, IssueTime, WorkBay) in issue order
    return [(f"T-{t}", f"TECH-{rnd.randint(1, 400)}", i, f"BAY-{rnd.randint(1, 12)}") for i, t in enumerate(ids)]


def sequential_search(records, key):
    comps = 0
    for i, rec in enumerate(records):
        comps += 1
        if rec[0] == key:
            return i, comps
    return -1, comps


if __name__ == "__main__":
    sizes = [100, 1000, 10000, 100000]
    rows = []
    print("=== Q2 Part 1: comparisons for successful / unsuccessful searches ===")
    print(f"{'n':>8}{'first':>8}{'25%':>8}{'middle':>8}{'75%':>8}{'last':>8}{'unsucc.':>9}{'avg succ (1000 rnd)':>21}{'(n+1)/2':>10}")
    for n in sizes:
        recs = make_records(n)
        at = lambda p: recs[min(n - 1, max(0, p))][0]
        c = [sequential_search(recs, at(p))[1] for p in (0, n // 4 - 1, n // 2 - 1, 3 * n // 4 - 1, n - 1)]
        cu = sequential_search(recs, "T-NOT-ISSUED")[1]
        rnd = random.Random(9)
        avg = statistics.mean(sequential_search(recs, recs[rnd.randrange(n)][0])[1] for _ in range(1000))
        print(f"{n:>8}{c[0]:>8}{c[1]:>8}{c[2]:>8}{c[3]:>8}{c[4]:>8}{cu:>9}{avg:>21.1f}{(n + 1) / 2:>10.1f}")
        rows.append(dict(n=n, first=c[0], q25=c[1], middle=c[2], q75=c[3], last=c[4], unsuccessful=cu, avg_success=round(avg, 1)))

    # measure time per comparison with an unsuccessful scan on the biggest list
    recs = make_records(100000)
    ts = []
    for _ in range(7):
        t0 = time.perf_counter(); sequential_search(recs, "T-NOT-ISSUED"); ts.append(time.perf_counter() - t0)
    t_c = min(ts) / 100000           # seconds per comparison (best of 7)
    idx = {r[0]: r for r in recs}
    t0 = time.perf_counter()
    for k in range(100000):
        idx.get("T-NOT-ISSUED")
    t_hash = (time.perf_counter() - t0) / 100000
    print(f"\nMeasured cost per comparison (best of 7 full scans of 100,000): {t_c * 1e9:.1f} ns")
    print(f"Measured hash-index lookup (dict on ToolID): {t_hash * 1e9:.1f} ns per lookup")

    print("\n=== Q2 Part 2: latency of one sequential search (avg successful = n/2, unsuccessful = n) ===")
    print(f"{'n':>9}{'avg successful':>17}{'unsuccessful':>15}")
    for n in (100, 1000, 10000, 100000, 1000000):
        print(f"{n:>9}{n / 2 * t_c * 1e3:>14.4f} ms{n * t_c * 1e3:>12.4f} ms")

    # operating boundary model
    LAT = 0.050   # 50 ms response budget per lookup
    CPU = 0.10    # <= 10% of one core spent on searching
    print(f"\n=== Q2 Part 3: operating boundary (latency budget {LAT * 1e3:.0f} ms, CPU budget {CPU * 100:.0f}% of one core) ===")
    n_lat = int(LAT / t_c)
    print(f"Latency boundary: worst-case scan <= 50 ms -> n <= {n_lat:,} records (independent of request rate)")
    print(f"{'requests/s':>12}{'max n (CPU 10%, avg n/2 scan)':>34}{'max n (unsuccessful, n scan)':>32}")
    bound = []
    for f in (0.1, 1, 10, 100, 1000, 10000):
        n_avg = int(CPU / (f * 0.5 * t_c)); n_unc = int(CPU / (f * t_c))
        bound.append((f, n_avg, n_unc))
        print(f"{f:>12}{n_avg:>34,}{n_unc:>32,}")

    print("\n=== Q2 Part 4: changed condition - one hangar vs 20 facilities (model) ===")
    scen = [("1 hangar", 800, 0.2), ("20 facilities (x20 records, x20 requests)", 16000, 4.0),
            ("20 facilities, busy shift peak (x10 burst)", 16000, 40.0),
            ("20 facilities, organisation-wide dashboards/bots", 16000, 500.0)]
    print(f"{'scenario':<52}{'records':>9}{'req/s':>8}{'scan ms (n/2)':>15}{'CPU load %':>12}{'hash CPU %':>12}")
    sc_rows = []
    for name, n, f in scen:
        ms = n / 2 * t_c * 1e3; cpu = f * n / 2 * t_c * 100; hcpu = f * t_hash * 100
        sc_rows.append((name, n, f, ms, cpu, hcpu))
        print(f"{name:<52}{n:>9,}{f:>8}{ms:>15.4f}{cpu:>12.4f}{hcpu:>12.6f}")

    with open(os.path.join(RES, "q2_raw.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    json.dump({"rows": rows, "t_c": t_c, "t_hash": t_hash, "n_lat": n_lat, "bound": bound, "scen": sc_rows},
              open(os.path.join(RES, "q2_raw.json"), "w"), indent=1)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for key, lab in (("first", "first"), ("middle", "middle"), ("last", "last"), ("unsuccessful", "unsuccessful")):
        ax[0].plot(sizes, [r[key] for r in rows], "o-", label=lab)
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("list size n"); ax[0].set_ylabel("comparisons")
    ax[0].set_title("Comparisons vs list size"); ax[0].legend()
    fs = [0.1, 1, 10, 100, 1000, 10000]
    ax[1].plot([b[0] for b in bound], [b[1] for b in bound], "o-", label="n_max at 10% CPU")
    ax[1].axhline(n_lat, color="r", ls="--", label="n_max at 50 ms latency")
    ax[1].set_xscale("log"); ax[1].set_yscale("log"); ax[1].set_xlabel("requests per second"); ax[1].set_ylabel("max records")
    ax[1].set_title("Operating boundary for sequential search"); ax[1].legend()
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q2_graphs.png"), dpi=130)
