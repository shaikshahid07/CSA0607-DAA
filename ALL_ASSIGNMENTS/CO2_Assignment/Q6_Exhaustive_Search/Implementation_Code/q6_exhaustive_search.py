"""Q6 - Exhaustive search for the airlift payload (0/1 knapsack). Run: python q6_exhaustive_search.py"""
import random, time, json, csv, os, itertools, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def exhaustive(w, v, W):
    n = len(w); best = -1; bmask = 0; feasible = 0
    for mask in range(1 << n):
        tw = tv = 0
        for i in range(n):
            if mask >> i & 1:
                tw += w[i]; tv += v[i]
        if tw <= W:
            feasible += 1
            if tv > best:
                best = tv; bmask = mask
    return best, bmask, 1 << n, feasible


def dp_optimum(w, v, W):                       # independent check (dynamic programming over weight)
    dp = [0] * (W + 1)
    for wi, vi in zip(w, v):
        for c in range(W, wi - 1, -1):
            dp[c] = max(dp[c], dp[c - wi] + vi)
    return dp[W]


def instance(n, seed=None):
    rnd = random.Random(n if seed is None else seed)
    w = [rnd.randint(5, 50) for _ in range(n)]; v = [rnd.randint(10, 100) for _ in range(n)]
    return w, v, sum(w) // 2


if __name__ == "__main__":
    # ---------- correctness: hand-checkable instance ----------
    names = ["Water", "Medicine", "Food", "Blankets", "Generator"]
    w = [4, 3, 5, 2, 6]; v = [40, 30, 45, 15, 55]; W = 10
    print("=== Q6 correctness check, n=5, payload limit W=10 ===")
    print("Package   weight  value:", ", ".join(f"{a}({x},{y})" for a, x, y in zip(names, w, v)))
    print(f"{'mask':>6}{'subset':<30}{'weight':>8}{'value':>7}  feasible")
    for mask in range(32):
        sub = [names[i] for i in range(5) if mask >> i & 1]
        tw = sum(w[i] for i in range(5) if mask >> i & 1); tv = sum(v[i] for i in range(5) if mask >> i & 1)
        print(f"{mask:>6}  {'{' + ','.join(sub) + '}':<28}{tw:>8}{tv:>7}  {'yes' if tw <= W else 'no'}")
    best, bmask, cand, feas = exhaustive(w, v, W)
    chosen = [names[i] for i in range(5) if bmask >> i & 1]
    it = max((sum(v[i] for i in c), c) for r in range(6) for c in itertools.combinations(range(5), r) if sum(w[i] for i in c) <= W)
    print(f"\nProgram: best value {best}, subset {chosen}, candidates {cand}, feasible {feas}")
    print(f"Check 1 itertools.combinations: best value {it[0]}   Check 2 dynamic programming: {dp_optimum(w, v, W)}")
    print("Hand check: {Water,Generator} weight 4+6=10 <= 10, value 40+55=95; scanning the 32-row table above, no feasible row exceeds 95 -> 95 expected")
    assert best == it[0] == dp_optimum(w, v, W)

    # ---------- growth ----------
    print("\n=== Growth with number of packages (random instance, seed = n, W = half of total weight) ===")
    print(f"{'n':>4}{'candidates 2^n':>16}{'feasible':>12}{'time (s)':>10}{'time ratio':>11}{'us/candidate':>14}{'best value':>12}{'DP check':>10}")
    rows = []; prev = None
    for n in (8, 10, 12, 14, 16, 18, 20, 22):
        w, v, W = instance(n)
        t0 = time.perf_counter(); best, bm, cand, feas = exhaustive(w, v, W); t = time.perf_counter() - t0
        ok = best == dp_optimum(w, v, W)
        rows.append(dict(n=n, candidates=cand, feasible=feas, time_s=round(t, 4), best=best, dp_ok=ok))
        print(f"{n:>4}{cand:>16,}{feas:>12,}{t:>10.3f}{(t / prev if prev else float('nan')):>11.2f}{t / cand * 1e6:>14.3f}{best:>12}{str(ok):>10}")
        prev = t
    # time ratio per added package from the last two points (2 packages -> 4x candidates)
    r_pkg = math.sqrt(rows[-1]["time_s"] / rows[-2]["time_s"])
    print(f"\nObserved time multiplier per extra package (from n=20->22): x{r_pkg:.2f}  (candidates x2.00)")
    c = rows[-1]["time_s"] / rows[-1]["candidates"]
    for n in (24, 26, 28, 30, 40):
        t = c * 2 ** n * (n / 22)
        print(f"  extrapolated n={n}: {t:,.0f} s = {t / 3600:,.2f} h" + (f" = {t / 86400 / 365:,.1f} years" if t > 3.15e7 else ""))
    LIM = 5.0
    nmax = max(r["n"] for r in rows if r["time_s"] <= LIM)
    print(f"\nResponse-time limit {LIM:.0f} s -> largest measured n inside the limit: {nmax}")
    with open(os.path.join(RES, "q6_raw.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=rows[0].keys()); wr.writeheader(); wr.writerows(rows)
    json.dump({"rows": rows, "c": c, "nmax": nmax, "r_pkg": r_pkg}, open(os.path.join(RES, "q6_raw.json"), "w"), indent=1)

    ns = [r["n"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].semilogy(ns, [r["candidates"] for r in rows], "o-"); ax[0].set_xlabel("packages n"); ax[0].set_ylabel("candidate subsets (log)"); ax[0].set_title("Candidates = 2^n")
    ax[1].semilogy(ns, [r["time_s"] for r in rows], "o-", label="measured"); ax[1].axhline(LIM, color="r", ls="--", label="5 s limit")
    ax[1].set_xlabel("packages n"); ax[1].set_ylabel("time (s, log)"); ax[1].set_title("Execution time"); ax[1].legend()
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q6_graphs.png"), dpi=130)
