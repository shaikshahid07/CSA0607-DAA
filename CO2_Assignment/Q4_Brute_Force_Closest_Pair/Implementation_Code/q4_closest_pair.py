"""Q4 - Brute-force closest pair of drones. Run: python q4_closest_pair.py"""
import random, time, json, csv, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def closest_pair(pts):
    n = len(pts); best = float("inf"); pair = None; pairs = dist = 0
    for i in range(n - 1):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            pairs += 1
            dx = xi - pts[j][0]; dy = yi - pts[j][1]
            d2 = dx * dx + dy * dy; dist += 1
            if d2 < best:
                best = d2; pair = (i, j)
    return pair, math.sqrt(best), pairs, dist


def gen(n, seed=7):
    rnd = random.Random(seed)
    return [(rnd.randint(0, 10000), rnd.randint(0, 10000)) for _ in range(n)]


if __name__ == "__main__":
    # tiny hand-checkable case
    demo = [(0, 0), (10, 10), (3, 4), (11, 12)]
    print("Demo with 4 drones", demo)
    p, d, pr, dc = closest_pair(demo)
    print(f"  closest: {demo[p[0]]} and {demo[p[1]]}, distance {d:.3f}; pairs examined {pr} (= 4*3/2 = 6)")

    print("\n=== Q4: pairs, distance calculations and time ===")
    print(f"{'n':>6}{'pairs examined':>16}{'n(n-1)/2':>14}{'dist calcs':>14}{'time (s)':>10}{'us/pair':>9}{'closest dist':>14}")
    rows = []
    for n in (100, 250, 500, 1000, 2000, 4000, 8000):
        pts = gen(n); times = []
        for _ in range(3 if n <= 2000 else 1):
            t0 = time.perf_counter(); res = closest_pair(pts); times.append(time.perf_counter() - t0)
        t = min(times); pair, d, pr, dc = res
        assert pr == n * (n - 1) // 2 == dc
        rows.append(dict(n=n, pairs=pr, theory=n * (n - 1) // 2, dist_calcs=dc, time_s=round(t, 4), us_per_pair=round(t / pr * 1e6, 4), closest=round(d, 3)))
        print(f"{n:>6}{pr:>16,}{n * (n - 1) // 2:>14,}{dc:>14,}{t:>10.4f}{t / pr * 1e6:>9.3f}{d:>14.3f}")

    c = sum(r["time_s"] for r in rows[3:]) / sum(r["pairs"] for r in rows[3:])
    print(f"\nFitted cost per pair (n>=1000): {c * 1e6:.3f} microseconds")
    print("Growth check - ratio of successive times when n doubles:")
    for a, b in zip(rows[3:], rows[4:]):
        print(f"  n {a['n']} -> {b['n']}: time x{b['time_s'] / a['time_s']:.2f}   pairs x{b['pairs'] / a['pairs']:.2f}")

    LIM = 1.0
    # n for time = LIM  :  c*n(n-1)/2 = LIM
    n_lim = int((1 + math.sqrt(1 + 8 * LIM / c)) / 2)
    print(f"\nAcceptable response time = {LIM:.0f} s per position update  ->  brute force breaks at about n = {n_lim:,} drones")
    for lim in (0.1, 0.5, 1.0, 5.0):
        print(f"   limit {lim:>4} s  ->  n ~ {int((1 + math.sqrt(1 + 8 * lim / c)) / 2):,}")
    for n in (10000, 50000, 100000):
        print(f"   predicted time at n = {n:>7,}: {c * n * (n - 1) / 2:,.1f} s")

    with open(os.path.join(RES, "q4_raw.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    json.dump({"rows": rows, "c": c, "n_lim": n_lim}, open(os.path.join(RES, "q4_raw.json"), "w"), indent=1)

    ns = [r["n"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(ns, [r["pairs"] for r in rows], "o-", label="observed pairs"); ax[0].plot(ns, [r["theory"] for r in rows], "x--", label="n(n-1)/2")
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("n drones"); ax[0].set_ylabel("pairs examined"); ax[0].legend(); ax[0].set_title("Pair count vs theory")
    xs = list(range(100, 9001, 100))
    ax[1].plot(ns, [r["time_s"] for r in rows], "o", label="measured"); ax[1].plot(xs, [c * x * (x - 1) / 2 for x in xs], "-", label="fit c*n(n-1)/2")
    ax[1].axhline(LIM, color="r", ls="--", label="1 s limit"); ax[1].set_xlabel("n drones"); ax[1].set_ylabel("time (s)"); ax[1].legend(); ax[1].set_title("Execution time")
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q4_graphs.png"), dpi=130)
