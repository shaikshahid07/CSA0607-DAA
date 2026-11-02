import random
import math
import time
import sys

random.seed(2026)
sys.setrecursionlimit(10000)

brute_count = 0
dc_count = 0
dc_calls = 0
strip_checks = 0

def dist2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

def brute_force(points):
    global brute_count
    best = float("inf")
    best_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            brute_count += 1
            d = dist2(points[i], points[j])
            if d < best:
                best = d
                best_pair = (points[i], points[j])
    return best, best_pair

def small_case(points):
    global dc_count
    best = float("inf")
    best_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dc_count += 1
            d = dist2(points[i], points[j])
            if d < best:
                best = d
                best_pair = (points[i], points[j])
    return best, best_pair

def merge_by_y(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

def closest_rec(px):
    global dc_count, dc_calls, strip_checks
    dc_calls += 1
    n = len(px)
    if n <= 3:
        best, pair = small_case(px)
        return best, pair, sorted(px, key=lambda p: p[1])
    mid = n // 2
    mid_x = px[mid][0]
    d_left, pair_left, py_left = closest_rec(px[:mid])
    d_right, pair_right, py_right = closest_rec(px[mid:])
    py = merge_by_y(py_left, py_right)
    if d_left < d_right:
        best = d_left
        best_pair = pair_left
    else:
        best = d_right
        best_pair = pair_right
    strip = []
    for p in py:
        if (p[0] - mid_x) ** 2 < best:
            strip.append(p)
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) ** 2 < best:
            dc_count += 1
            strip_checks += 1
            d = dist2(strip[i], strip[j])
            if d < best:
                best = d
                best_pair = (strip[i], strip[j])
            j += 1
    return best, best_pair, py

def closest_pair_dc(points):
    px = sorted(points)
    best, pair, py = closest_rec(px)
    return best, pair

def random_points(n, size=1000000):
    pts = set()
    while len(pts) < n:
        pts.add((random.randint(0, size), random.randint(0, size)))
    return list(pts)

def clustered_points(n):
    pts = set()
    while len(pts) < n:
        cx = random.choice([100000, 400000, 700000, 900000])
        cy = random.choice([100000, 500000, 800000])
        pts.add((cx + random.randint(0, 50000), cy + random.randint(0, 50000)))
    return list(pts)

def line_points(n):
    pts = set()
    while len(pts) < n:
        pts.add((random.randint(0, 10000000), 500))
    return list(pts)

print("=" * 72)
print("Q5 : CLOSEST PAIR OF POINTS - BRUTE FORCE VS DIVIDE AND CONQUER")
print("=" * 72)

demo = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
brute_count = 0
dc_count = 0
b = brute_force(demo)
d = closest_pair_dc(demo)
print("Demo points  :", demo)
print("Brute force  : squared distance", b[0], "pair", b[1], " distance computations =", brute_count)
print("Divide&Conq  : squared distance", d[0], "pair", d[1], " distance computations =", dc_count)
print()

print("Experiment 1 : correctness on 300 random data sets (n between 2 and 200)")
bad = 0
for i in range(300):
    n = random.randint(2, 200)
    pts = random_points(n, 500)
    b = brute_force(pts)
    d = closest_pair_dc(pts)
    if b[0] != d[0]:
        bad += 1
print("Wrong answers :", bad)
print()

print("Experiment 2 : distance computations (uniform random points)")
print("%-7s %-14s %-14s %-12s %-10s %-10s %-10s" % ("n", "Brute dists", "D&C dists", "n log2 n", "Ratio", "t brute", "t D&C"))
rows = []
for n in [50, 100, 200, 400, 800, 1600, 3200, 6400]:
    pts = random_points(n)
    brute_count = 0
    dc_count = 0
    dc_calls = 0
    if n <= 3200:
        start = time.perf_counter()
        b = brute_force(pts)
        tb = time.perf_counter() - start
        bc = brute_count
    else:
        tb = float("nan")
        bc = n * (n - 1) // 2
    start = time.perf_counter()
    d = closest_pair_dc(pts)
    td = time.perf_counter() - start
    if n <= 3200 and b[0] != d[0]:
        print("MISMATCH")
    print("%-7d %-14d %-14d %-12.0f %-10.1f %-10.4f %-10.4f" % (n, bc, dc_count, n * math.log2(n), bc / dc_count, tb, td))
    rows.append((n, bc, dc_count, tb, td))
print("(for n = 6400 the brute force time is skipped; its count is n(n-1)/2)")
print()

print("Experiment 3 : different point layouts, n = 2000")
print("%-12s %-14s %-14s %-12s" % ("Layout", "Brute dists", "D&C dists", "Strip checks"))
for name, maker in [("uniform", random_points), ("clustered", clustered_points), ("on a line", line_points)]:
    pts = maker(2000)
    brute_count = 0
    dc_count = 0
    strip_checks = 0
    b = brute_force(pts)
    d = closest_pair_dc(pts)
    print("%-12s %-14d %-14d %-12d  same answer: %s" % (name, brute_count, dc_count, strip_checks, b[0] == d[0]))
print()

print("Experiment 4 : strip work per point (uniform random points)")
print("%-7s %-14s %-14s %-18s" % ("n", "Strip checks", "Points", "Checks per point"))
for n in [500, 1000, 2000, 4000, 8000]:
    pts = random_points(n)
    dc_count = 0
    strip_checks = 0
    closest_pair_dc(pts)
    print("%-7d %-14d %-14d %-18.2f" % (n, strip_checks, n, strip_checks / n))
print()

print("Experiment 5 : timing in seconds, finding the practical crossover (average of 5 runs)")
print("%-7s %-12s %-12s %-12s" % ("n", "Brute", "D&C", "Faster"))
cross = []
for n in [4, 8, 12, 16, 24, 32, 48, 64, 100, 200]:
    tb = 0
    td = 0
    for r in range(5):
        pts = random_points(n)
        start = time.perf_counter()
        for k in range(20):
            brute_force(pts)
        tb += (time.perf_counter() - start) / 20
        start = time.perf_counter()
        for k in range(20):
            closest_pair_dc(pts)
        td += (time.perf_counter() - start) / 20
    tb /= 5
    td /= 5
    if tb < td:
        w = "Brute"
    else:
        w = "D&C"
    print("%-7d %-12.6f %-12.6f %-12s" % (n, tb, td, w))
    cross.append((n, tb, td))
