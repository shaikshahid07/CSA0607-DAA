"""Q5 - Brute-force convex hull from the 'all other points on one side' principle. Run: python q5_convex_hull.py"""
import random, time, json, csv, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def side(p1, p2, q):
    """sign of a*qx + b*qy - c for the line through p1,p2: a=y2-y1, b=x1-x2, c=x1*y2-y1*x2 (exact for integers)"""
    a = p2[1] - p1[1]; b = p1[0] - p2[0]; c = p1[0] * p2[1] - p1[1] * p2[0]
    return a * q[0] + b * q[1] - c


def in_segment(p1, p2, q):
    return min(p1[0], p2[0]) <= q[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= q[1] <= max(p1[1], p2[1])


def convex_hull(points, early_exit=True, shuffle_scan=False):
    """returns hull vertices (counter-clockwise), number of side tests performed"""
    P = sorted(set(points))                      # remove duplicates
    if shuffle_scan:
        random.Random(0).shuffle(P)              # scan order experiment only
    n = len(P); tests = 0
    if n < 3:
        return P, 0
    nxt = {}
    for i in range(n - 1):
        for j in range(i + 1, n):
            pos = neg = False; ok = True
            for k in range(n):
                if k == i or k == j:
                    continue
                tests += 1
                s = side(P[i], P[j], P[k])
                if s > 0: pos = True
                elif s < 0: neg = True
                elif not in_segment(P[i], P[j], P[k]):
                    ok = False
                    if early_exit: break
                if pos and neg:
                    ok = False
                    if early_exit: break
            if ok and not (pos and neg):
                if not neg and pos: nxt[P[i]] = P[j]             # all on left  : i -> j
                elif not pos and neg: nxt[P[j]] = P[i]           # all on right : j -> i
                else:                                            # all collinear: both directions
                    nxt[P[i]] = P[j]; nxt.setdefault(P[j], P[i])
    if not nxt:
        return P, tests
    # degenerate collinear set: nxt has two mutual entries
    start = min(nxt, key=lambda p: (p[1], p[0]))
    hull = [start]; cur = nxt[start]; guard = 0
    while cur != start and guard <= n:
        hull.append(cur); cur = nxt.get(cur, start); guard += 1
    return hull, tests


def gen(n, seed=3, span=10000):
    rnd = random.Random(seed)
    return [(rnd.randint(0, span), rnd.randint(0, span)) for _ in range(n)]


def plot_cfg(ax, pts, hull, title):
    xs, ys = zip(*pts); ax.scatter(xs, ys, s=18, c="tab:blue", zorder=2)
    if len(hull) >= 2:
        hx = [h[0] for h in hull] + [hull[0][0]]; hy = [h[1] for h in hull] + [hull[0][1]]
        ax.plot(hx, hy, "r-o", ms=5, lw=1.6, zorder=3)
    ax.set_title(title, fontsize=9); ax.set_aspect("equal", adjustable="datalim")


if __name__ == "__main__":
    T1 = [(2, 3), (4, 9), (6, 5), (8, 1), (10, 7), (12, 12), (14, 4), (16, 9), (3, 7), (7, 8), (9, 4), (11, 9), (13, 7), (5, 2), (15, 14), (1, 11), (9, 15), (18, 6), (8, 6), (12, 5)]
    T2 = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 0), (10, 5), (5, 10), (0, 5), (3, 0), (7, 10), (5, 5), (4, 6), (5, 5), (0, 0), (2, 8), (8, 2)]
    T3 = [(i, 2 * i + 1) for i in range(8)]
    rnd = random.Random(1)
    T4 = [(round(100 * math.cos(2 * math.pi * k / 12)), round(100 * math.sin(2 * math.pi * k / 12))) for k in range(12)]
    print("=== Q5: convex hull tests ===")
    results = {}
    for name, pts in (("T1 mixed boundary/interior", T1), ("T2 designed: corners + on-edge + duplicates + interior", T2),
                      ("T3 all collinear", T3), ("T4 12 points on a circle", T4)):
        hull, tests = convex_hull(pts); full = len(set(pts)) * (len(set(pts)) - 1) * (len(set(pts)) - 2) // 2
        results[name] = (pts, hull)
        print(f"\n{name}\n  input points: {len(pts)} ({len(set(pts))} distinct)\n  hull vertices ({len(hull)}): {hull}\n  side tests with early exit: {tests:,}   without early exit: {full:,}")

    # cross-check hull against an independent monotone-chain implementation
    def mono(P):
        P = sorted(set(P))
        if len(P) < 3: return P
        cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        lo = []
        for p in P:
            while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
            lo.append(p)
        up = []
        for p in reversed(P):
            while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
            up.append(p)
        return lo[:-1] + up[:-1]
    print("\nCross-check against independent algorithm (set equality of hull vertices):")
    for name, (pts, hull) in results.items():
        print(f"  {name[:28]:<30} -> {'MATCH' if set(hull) == set(mono(pts)) else 'DIFFERENT'}")
    for sd in range(20):
        pts = gen(40, sd, 50)
        assert set(convex_hull(pts)[0]) == set(mono(pts)), sd
    print("  20 random clustered 40-point sets (many collinear/duplicates): all MATCH")

    print("\n=== Growth of work with n (random points) ===")
    print(f"{'n':>5}{'hull size':>10}{'tests (early exit)':>20}{'tests/n^2':>11}{'full scan n(n-1)(n-2)/2':>26}{'time (s)':>10}")
    rows = []
    for n in (20, 40, 80, 160, 320, 640):
        pts = gen(n); t0 = time.perf_counter(); h, tests = convex_hull(pts); t = time.perf_counter() - t0
        full = n * (n - 1) * (n - 2) // 2
        rows.append(dict(n=n, hull=len(h), tests=tests, full=full, time_s=round(t, 4)))
        print(f"{n:>5}{len(h):>10}{tests:>20,}{tests / n ** 2:>11.2f}{full:>26,}{t:>10.3f}")
    import numpy as np
    sl = np.polyfit(np.log([r["n"] for r in rows]), np.log([r["tests"] for r in rows]), 1)[0]
    print(f"Log-log slope of early-exit tests vs n: {sl:.2f}   (full scan slope = 3)")
    pts = gen(320)
    ts = convex_hull(pts, shuffle_scan=True)[1]
    print(f"Scan-order experiment n=320: sorted-by-x scan order = {rows[4]['tests']:,} tests; shuffled scan order = {ts:,} tests")
    # worst case for early exit: points on a circle-like arrangement scanned fully, and a no-early-exit run
    h, tfull = convex_hull(gen(80), early_exit=False)
    print(f"No-early-exit run at n=80: {tfull:,} tests (formula {80 * 79 * 78 // 2:,})")

    with open(os.path.join(RES, "q5_raw.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    json.dump({"rows": rows, "slope": float(sl), "hulls": {k: v[1] for k, v in results.items()}}, open(os.path.join(RES, "q5_raw.json"), "w"), indent=1)

    fig, axs = plt.subplots(2, 3, figsize=(13, 8))
    names = list(results)
    for ax, nm in zip(axs.flat[:4], names):
        plot_cfg(ax, *results[nm], nm)
    pts = gen(120, 11); h, _ = convex_hull(pts); plot_cfg(axs.flat[4], pts, h, "120 random points")
    ax = axs.flat[5]; ns = [r["n"] for r in rows]
    ax.loglog(ns, [r["tests"] for r in rows], "o-", label="tests, early exit"); ax.loglog(ns, [r["full"] for r in rows], "s--", label="n(n-1)(n-2)/2")
    ax.set_xlabel("n"); ax.set_ylabel("side tests"); ax.legend(); ax.set_title("Work growth")
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q5_hull_visualisation.png"), dpi=120)
