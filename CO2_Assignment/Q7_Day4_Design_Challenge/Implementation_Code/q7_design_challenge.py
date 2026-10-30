"""Q7 - Day-4 Design Challenge: redesign of the Q6 exhaustive search (airlift payload).
V0 = exhaustive (Q6), V1 = DFS + feasibility cut-off, V2 = V1 + ratio ordering + fractional upper-bound cut-off.
Run: python q7_design_challenge.py"""
import random, time, json, csv, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.setrecursionlimit(10000)

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def exhaustive(w, v, W):                      # V0 (same logic as Q6)
    n = len(w); best = -1
    for mask in range(1 << n):
        tw = tv = 0
        for i in range(n):
            if mask >> i & 1:
                tw += w[i]; tv += v[i]
        if tw <= W and tv > best:
            best = tv
    return best, 1 << n


class Capped(Exception):
    pass


def search(w, v, W, use_bound, node_cap=None):
    """V1 (use_bound=False, original order) / V2 (use_bound=True, ratio order). returns best, nodes, pruned"""
    n = len(w)
    order = sorted(range(n), key=lambda i: -v[i] / w[i]) if use_bound else list(range(n))
    ww = [w[i] for i in order]; vv = [v[i] for i in order]
    st = {"best": 0, "nodes": 0, "pruned": 0}

    def bound(k, room, val):
        for t in range(k, n):
            if ww[t] <= room:
                room -= ww[t]; val += vv[t]
            else:
                return val + vv[t] * room / ww[t]
        return val

    def explore(k, weight, value):
        st["nodes"] += 1
        if node_cap and st["nodes"] > node_cap:
            raise Capped
        if value > st["best"]:
            st["best"] = value
        if k == n:
            return
        if use_bound and int(bound(k, W - weight, value)) <= st["best"]:
            st["pruned"] += 1
            return
        if weight + ww[k] <= W:
            explore(k + 1, weight + ww[k], value + vv[k])
        explore(k + 1, weight, value)

    try:
        explore(0, 0, 0); capped = False
    except Capped:
        capped = True
    return st["best"], st["nodes"], st["pruned"], capped


def dp_optimum(w, v, W):
    dp = [0] * (W + 1)
    for wi, vi in zip(w, v):
        for c in range(W, wi - 1, -1):
            dp[c] = max(dp[c], dp[c - wi] + vi)
    return dp[W]


def rand_instance(n, seed):
    rnd = random.Random(seed)
    w = [rnd.randint(5, 50) for _ in range(n)]; v = [rnd.randint(10, 100) for _ in range(n)]
    return w, v, sum(w) // 2


def corr_instance(n, seed):                   # strongly correlated: value = weight + 10 (hard family)
    rnd = random.Random(seed)
    w = [rnd.randint(5, 50) for _ in range(n)]; v = [x + 10 for x in w]
    return w, v, sum(w) // 2


def timed(f, *a, **k):
    t0 = time.perf_counter(); r = f(*a, **k); return r, time.perf_counter() - t0


if __name__ == "__main__":
    print("=== Q7 Part A: diagnosis of the Q6 solution (measured) ===")
    for n in (14, 18, 20):
        w, v, W = rand_instance(n, n)
        ops = n * (1 << n)
        # how many candidates are infeasible, and how many feasible ones are not better than the running best
        feas = improved = 0; best = -1
        for mask in range(1 << n):
            tw = tv = 0
            for i in range(n):
                if mask >> i & 1: tw += w[i]; tv += v[i]
            if tw <= W:
                feas += 1
                if tv > best: best = tv; improved += 1
        print(f"n={n}: candidates {1 << n:,}; additions performed ~ n*2^n = {ops:,}; feasible {feas:,}; "
              f"feasible candidates that improved the best: {improved} ({improved / feas * 100:.4f}% of feasible) -> {1 << n:,} - {improved} evaluations never changed the answer")

    print("\n=== Q7 Part B: head-to-head, same instance, same optimum (random family) ===")
    hdr = f"{'n':>3}{'V0 cand.':>11}{'V1 nodes':>11}{'V2 nodes':>10}{'V2 vs 2^n':>11}{'V0 s':>8}{'V1 s':>8}{'V2 s':>9}{'speed-up V2':>12}{'optimum':>9}{'all equal':>10}"
    print(hdr)
    rows = []
    for n in (8, 10, 14, 18, 20, 22):
        w, v, W = rand_instance(n, n)
        (b0, c0), t0 = timed(exhaustive, w, v, W)
        (b1, n1, p1, _), t1 = timed(search, w, v, W, False)
        (b2, n2, p2, _), t2 = timed(search, w, v, W, True)
        eq = b0 == b1 == b2 == dp_optimum(w, v, W)
        rows.append(dict(n=n, v0_candidates=c0, v1_nodes=n1, v2_nodes=n2, v2_pruned=p2, t0=round(t0, 5), t1=round(t1, 5), t2=round(t2, 6), best=b0, equal=eq))
        print(f"{n:>3}{c0:>11,}{n1:>11,}{n2:>10,}{n2 / c0 * 100:>10.4f}%{t0:>8.4f}{t1:>8.4f}{t2:>9.5f}{t0 / t2:>11.1f}x{b0:>9}{str(eq):>10}")

    print("\n=== Q7 Part C: robustness - V2 over 10 random instances per size (node cap 3,000,000) ===")
    print(f"{'n':>4}{'median nodes':>14}{'max nodes':>12}{'median s':>10}{'max s':>9}{'median % of 2^n':>18}  all optimal(DP)")
    rob = []
    for n in (10, 20, 30, 40, 50, 60):
        ns = []; ts = []; okall = True
        for s in range(10):
            w, v, W = rand_instance(n, 1000 * n + s)
            (b, nd, pr, cap), t = timed(search, w, v, W, True, 3_000_000)
            ns.append(nd); ts.append(t); okall &= (not cap and b == dp_optimum(w, v, W))
        ns.sort(); ts.sort()
        rob.append(dict(n=n, median_nodes=ns[5], max_nodes=ns[-1], median_s=round(ts[5], 5), max_s=round(ts[-1], 5), ok=okall))
        print(f"{n:>4}{ns[5]:>14,}{ns[-1]:>12,}{ts[5]:>10.4f}{ts[-1]:>9.4f}{ns[5] / 2 ** n * 100:>17.8f}%  {okall}")

    print("\n=== Q7 Part D: adversarial family - strongly correlated (value = weight + 10), V2, 5 instances, cap 300,000 nodes ===")
    print(f"{'n':>4}{'median nodes':>14}{'max nodes':>11}{'capped runs':>13}{'median % of 2^n':>17}{'median s':>10}")
    adv = []
    for n in (16, 20, 24, 28, 32):
        ns = []; ts = []; caps = 0; ok = True
        for s in range(5):
            w, v, W = corr_instance(n, 77 * n + s)
            (b, nd, pr, cap), t = timed(search, w, v, W, True, 300_000)
            ns.append(nd); ts.append(t); caps += cap
            if not cap: ok &= (b == dp_optimum(w, v, W))
        ns.sort(); ts.sort()
        adv.append(dict(n=n, median_nodes=ns[2], max_nodes=ns[-1], capped=caps, median_s=round(ts[2], 4), ok=ok))
        print(f"{n:>4}{ns[2]:>14,}{ns[-1]:>11,}{caps:>13}{ns[2] / 2 ** n * 100:>16.5f}%{ts[2]:>10.3f}")
    # same family at n=20 with V1 / exhaustive for context
    w, v, W = corr_instance(20, 77 * 20)
    (b2, n2, _, _), t2 = timed(search, w, v, W, True); (b1, n1, _, _), t1 = timed(search, w, v, W, False); (b0, c0), t0 = timed(exhaustive, w, v, W)
    print(f"\nCorrelated n=20 instance: exhaustive {c0:,} cand {t0:.3f}s | V1 {n1:,} nodes {t1:.3f}s | V2 {n2:,} nodes {t2:.3f}s | optima equal: {b0 == b1 == b2}")
    corr20 = dict(c0=c0, t0=t0, n1=n1, t1=t1, n2=n2, t2=t2)


    print("\n=== Q7 Part E: designed worst case for the bound - all weights even, value = weight, odd payload limit (no exact fill exists) ===")
    print(f"{'n':>4}{'V2 nodes':>12}{'% of 2^n':>11}{'time s':>9}{'capped (1M)':>13}{'V1 nodes':>11}{'V0 cand.':>11}")
    advE = []
    for n in (12, 16, 20, 24):
        rnd = random.Random(5 * n); w = [2 * rnd.randint(3, 25) for _ in range(n)]; v = w[:]; W = sum(w) // 2 | 1
        (b2, n2, _, cap2), t2 = timed(search, w, v, W, True, 1_000_000)
        (b1, n1, _, cap1), t1 = timed(search, w, v, W, False, 1_000_000)
        advE.append(dict(n=n, v2_nodes=n2, capped=bool(cap2), t2=round(t2, 3), v1_nodes=n1))
        print(f"{n:>4}{n2:>12,}{n2 / 2 ** n * 100:>10.3f}%{t2:>9.3f}{str(bool(cap2)):>13}{n1:>11,}{1 << n:>11,}")

    with open(os.path.join(RES, "q7_head_to_head.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=rows[0].keys()); wr.writeheader(); wr.writerows(rows)
    json.dump({"rows": rows, "rob": rob, "adv": adv, "corr20": corr20, "advE": advE}, open(os.path.join(RES, "q7_raw.json"), "w"), indent=1)

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    ns_ = [r["n"] for r in rows]
    ax[0].semilogy(ns_, [r["v0_candidates"] for r in rows], "o-", label="V0 exhaustive 2^n"); ax[0].semilogy(ns_, [r["v1_nodes"] for r in rows], "s-", label="V1 feasibility cut")
    ax[0].semilogy(ns_, [r["v2_nodes"] for r in rows], "^-", label="V2 + bound"); ax[0].set_xlabel("n"); ax[0].set_ylabel("candidates / nodes (log)"); ax[0].legend(); ax[0].set_title("Search effort")
    ax[1].semilogy(ns_, [max(r["t0"], 1e-6) for r in rows], "o-", label="V0"); ax[1].semilogy(ns_, [r["t1"] for r in rows], "s-", label="V1"); ax[1].semilogy(ns_, [r["t2"] for r in rows], "^-", label="V2")
    ax[1].set_xlabel("n"); ax[1].set_ylabel("time (s, log)"); ax[1].legend(); ax[1].set_title("Execution time")
    ax[2].semilogy([r["n"] for r in rob], [r["median_nodes"] for r in rob], "^-", label="V2 random (median of 10)")
    ax[2].semilogy([r["n"] for r in adv], [r["median_nodes"] for r in adv], "x-", label="V2 correlated (cap 300k)")
    ax[2].semilogy([r["n"] for r in advE], [r["v2_nodes"] for r in advE], "d-", label="V2 designed worst case (cap 1M)")
    ax[2].set_xlabel("n"); ax[2].set_ylabel("nodes (log)"); ax[2].legend(); ax[2].set_title("V2 scaling: easy vs hard instances")
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q7_graphs.png"), dpi=130)
