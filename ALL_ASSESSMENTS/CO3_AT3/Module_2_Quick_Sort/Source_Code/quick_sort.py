"""
Module 2 - Live Seller Leaderboard (KartIQ)
Quick Sort: first-element pivot (current) vs median-of-three pivot (proposed).

Run:  python3 quick_sort.py
Student: Shaik Shahid (192424311)  |  CSA06 CO3 Case Study
"""
import math
import random
import time

comparisons = 0
max_depth = 0


# ---------------------------------------------------------------- current design
def partition_first(a, lo, hi):
    """Pivot = a[lo]. Returns final pivot index. (Lomuto-style with pivot at the front.)"""
    global comparisons
    pivot = a[lo]
    i = lo
    for j in range(lo + 1, hi + 1):
        comparisons += 1
        if a[j] < pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[lo], a[i] = a[i], a[lo]
    return i


def quick_sort_first(a, lo, hi, depth=1):
    global max_depth
    if lo < hi:
        max_depth = max(max_depth, depth)
        p = partition_first(a, lo, hi)             # DIVIDE (work is done here)
        quick_sort_first(a, lo, p - 1, depth + 1)  # CONQUER
        quick_sort_first(a, p + 1, hi, depth + 1)  # CONQUER  (COMBINE = nothing)


# ---------------------------------------------------------------- proposed design
def median_of_three_index(a, lo, hi):
    mid = (lo + hi) // 2
    trio = sorted([(a[lo], lo), (a[mid], mid), (a[hi], hi)])
    return trio[1][1]


def quick_sort_m3(a, lo, hi, depth=1):
    """Median-of-three pivot moved to the front, same partition."""
    global max_depth
    while lo < hi:
        max_depth = max(max_depth, depth)
        m = median_of_three_index(a, lo, hi)
        a[lo], a[m] = a[m], a[lo]
        p = partition_first(a, lo, hi)
        # recurse into the smaller side, loop on the larger (stack depth O(log n))
        if p - lo < hi - p:
            quick_sort_m3(a, lo, p - 1, depth + 1)
            lo = p + 1
        else:
            quick_sort_m3(a, p + 1, hi, depth + 1)
            hi = p - 1
        depth += 1


def quick_sort_random(a, lo, hi, depth=1):
    global max_depth
    if lo < hi:
        max_depth = max(max_depth, depth)
        r = random.randint(lo, hi)
        a[lo], a[r] = a[r], a[lo]
        p = partition_first(a, lo, hi)
        quick_sort_random(a, lo, p - 1, depth + 1)
        quick_sort_random(a, p + 1, hi, depth + 1)


def nearly_sorted(n):
    """Leaderboard-like data: already sorted, ~1% of neighbouring scores swapped between refreshes."""
    data = list(range(n))
    for _ in range(max(1, n // 100)):
        i = random.randrange(n - 1)
        data[i], data[i + 1] = data[i + 1], data[i]
    return data


def run(sorter, data):
    global comparisons, max_depth
    a = list(data)
    comparisons = 0
    max_depth = 0
    sorter(a, 0, len(a) - 1)
    assert a == sorted(data)
    return comparisons, max_depth


# ---------------------------------------------------------------- demos
def demo_partition():
    print("=" * 70)
    print("MODULE 2 - ONE PARTITION STEP on sample scores (pivot = first element)")
    print("=" * 70)
    a = [42, 17, 63, 8, 55, 29]
    print("Input:", a)
    pivot = a[0]
    i = 0
    print(f"pivot = {pivot}, i = 0")
    for j in range(1, len(a)):
        if a[j] < pivot:
            i += 1
            val = a[j]
            a[i], a[j] = a[j], a[i]
            print(f"  j={j}: {val} < {pivot} -> i={i}, swap a[{i}],a[{j}] -> {a}")
        else:
            print(f"  j={j}: {a[j]} >= {pivot} -> no swap, i={i} -> {a}")
    a[0], a[i] = a[i], a[0]
    print(f"Place pivot: swap a[0],a[{i}] -> {a}")
    print(f"Pivot {pivot} is at index {i}; left = {a[:i]} (all < {pivot}); right = {a[i + 1:]} (all >= {pivot})")
    print("Comparisons in this partition: 5 (= n - 1)")

    print("\nFULL SORT of the sample (first-element pivot):")
    b = [42, 17, 63, 8, 55, 29]
    c, d = run(quick_sort_first, b)
    print(f"  sorted = {sorted(b)}, comparisons = {c}, recursion depth = {d}")


def demo_worst_case():
    print("\n" + "=" * 70)
    print("WORST-CASE DEMONSTRATION: nearly sorted data, first-element pivot")
    print("=" * 70)
    import sys
    sys.setrecursionlimit(20000)
    print(f"{'n':>6} {'first-pivot cmp':>16} {'n(n-1)/2':>12} {'depth':>6} | "
          f"{'median3 cmp':>12} {'depth':>6} | {'random cmp':>11} | {'n lg n':>10}")
    for n in [100, 200, 400, 800, 1600, 3200]:
        data = nearly_sorted(n)
        c1, d1 = run(quick_sort_first, data)
        c2, d2 = run(quick_sort_m3, data)
        c3, _ = run(quick_sort_random, data)
        print(f"{n:>6} {c1:>16,} {n * (n - 1) // 2:>12,} {d1:>6} | {c2:>12,} {d2:>6} | {c3:>11,} | {n * math.log2(n):>10,.0f}")


def theory():
    print("\n" + "=" * 70)
    print("ESTIMATES FOR 100,000 SELLERS")
    print("=" * 70)
    n = 100_000
    print(f"Worst case (nearly sorted, first pivot): n(n-1)/2 = {n * (n - 1) // 2:,} comparisons")
    print(f"Best / balanced case: ~ n lg n = {n * math.log2(n):,.0f} comparisons")
    print(f"Ratio worst/best = {n * (n - 1) / 2 / (n * math.log2(n)):,.0f}x")
    print(f"Recursion depth worst = {n:,} frames (stack overflow risk) vs ~{math.ceil(math.log2(n))} balanced")
    print(f"Average case (random pivot) ~ 2 n ln n = {2 * n * math.log(n):,.0f} comparisons")


def timing_experiment(out_csv):
    import sys
    sys.setrecursionlimit(20000)
    sizes = [250, 500, 1000, 2000, 4000]
    rows = []
    for n in sizes:
        data = nearly_sorted(n)
        res = []
        for s in (quick_sort_first, quick_sort_m3, quick_sort_random):
            t0 = time.perf_counter()
            c, _ = run(s, data)
            res.append((c, time.perf_counter() - t0))
        rows.append((n,) + tuple(x for pair in res for x in pair))
    with open(out_csv, "w") as f:
        f.write("n,first_cmp,first_s,median3_cmp,median3_s,random_cmp,random_s\n")
        for r in rows:
            f.write(",".join(str(x) if isinstance(x, int) else f"{x:.6f}" for x in r) + "\n")
    return rows


if __name__ == "__main__":
    random.seed(2)
    demo_partition()
    theory()
    demo_worst_case()
    print("\nTIMING (nearly sorted data)")
    for r in timing_experiment("../../Supporting_Files/datasets/quick_sort_timing.csv"):
        print(f"n={r[0]:>5} first: {r[1]:>9,} cmp {r[2]:.4f}s | median3: {r[3]:>7,} cmp {r[4]:.4f}s | "
              f"random: {r[5]:>7,} cmp {r[6]:.4f}s")
