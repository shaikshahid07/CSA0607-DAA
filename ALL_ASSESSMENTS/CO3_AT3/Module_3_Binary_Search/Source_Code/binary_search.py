"""
Module 3 - Order Lookup (KartIQ)
Binary Search on the timestamp-sorted list produced by Module 1,
plus the modified version that returns the FIRST order with a given timestamp.

Run:  python3 binary_search.py
Student: Shaik Shahid (192424311)  |  CSA06 CO3 Case Study
"""
import math
import random

steps = 0


def binary_search_any(a, key):
    """Standard version: returns SOME index with timestamp == key (not necessarily the first)."""
    global steps
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        steps += 1
        if a[mid][0] == key:
            return mid
        elif a[mid][0] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_first(a, key, trace=False):
    """Modified version: keep searching LEFT after a hit; returns the FIRST index with the key."""
    global steps
    lo, hi, first = 0, len(a) - 1, -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2            # overflow-safe mid
        steps += 1
        if trace:
            print(f"  lo={lo} hi={hi} mid={mid} a[mid]={a[mid]}", end=" ")
        if a[mid][0] == key:
            first = mid                       # record hit, but look for an earlier one
            hi = mid - 1
            if trace: print("-> hit, record, search left")
        elif a[mid][0] < key:
            lo = mid + 1
            if trace: print("-> go right")
        else:
            hi = mid - 1
            if trace: print("-> go left")
    return first


def binary_search_recursive(a, key, lo, hi):
    """Recursive form showing the divide-and-conquer structure T(n) = T(n/2) + 1."""
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if a[mid][0] == key:
        return mid
    if a[mid][0] < key:
        return binary_search_recursive(a, key, mid + 1, hi)
    return binary_search_recursive(a, key, lo, mid - 1)


def demo():
    global steps
    # consolidated list exactly as produced by Module 1
    orders = [(101, "O4"), (102, "O2"), (102, "O5"), (103, "O6"), (105, "O1"), (105, "O3")]
    print("=" * 70)
    print("MODULE 3 - BINARY SEARCH on Module 1 output")
    print("=" * 70)
    print("Sorted list:", orders)

    print("\nSearch for 102 using the STANDARD version:")
    steps = 0
    idx = binary_search_any(orders, 102)
    print(f"  returned index {idx} -> {orders[idx]} (steps={steps}); the first 102 is at index 1")

    for key in (102, 105, 101, 103, 104, 99):
        print(f"\nSearch for {key} using the FIRST-OCCURRENCE version:")
        steps = 0
        idx = binary_search_first(orders, key, trace=True)
        res = orders[idx] if idx >= 0 else "not found"
        print(f"  result index = {idx} -> {res}   (iterations = {steps})")
        expected = next((i for i, o in enumerate(orders) if o[0] == key), -1)
        assert idx == expected

    print("\nWhy sorted order matters: binary search on UNSORTED data")
    unsorted = [(105, "O1"), (102, "O2"), (105, "O3"), (101, "O4"), (102, "O5"), (103, "O6")]
    steps = 0
    idx = binary_search_first(unsorted, 101)
    print(f"  unsorted list, key 101 exists at index 3 but binary search returns {idx}  -> WRONG")


def theory():
    print("\n" + "=" * 70)
    print("MAXIMUM COMPARISONS FOR 10,000,000 ORDERS")
    print("=" * 70)
    n = 10_000_000
    print(f"floor(log2 n) + 1 = floor({math.log2(n):.4f}) + 1 = {math.floor(math.log2(n)) + 1} iterations")
    print(f"Linear search worst case = {n:,} comparisons -> speed-up = {n / (math.floor(math.log2(n)) + 1):,.0f}x")
    print("Simulating worst case (key larger than everything) on 10,000,000 sorted timestamps...")
    global steps
    big = [(t, "") for t in range(n)]
    steps = 0
    binary_search_first(big, n + 5)
    print(f"  measured iterations = {steps}")
    worst = 0
    for key in random.sample(range(n), 2000) + [0, n - 1]:
        steps = 0
        binary_search_first(big, key)
        worst = max(worst, steps)
    print(f"  max iterations over 2,002 sampled keys = {worst}")


def table():
    print("\nSTEPS vs n (first-occurrence version, worst case)")
    global steps
    print(f"{'n':>12} {'measured max':>14} {'floor(lg n)+1':>15}")
    for n in [10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]:
        arr = [(t, "") for t in range(n)]
        worst = 0
        for key in [-1, n, 0, n - 1, n // 2, n // 3]:
            steps = 0
            binary_search_first(arr, key)
            worst = max(worst, steps)
        print(f"{n:>12,} {worst:>14} {math.floor(math.log2(n)) + 1:>15}")


def timing(out_csv):
    import time
    n = 1_000_000
    arr = [(t // 3, "") for t in range(n)]     # duplicates: each timestamp appears 3 times
    keys = random.sample(range(n // 3), 200)
    t0 = time.perf_counter()
    for k in keys:
        binary_search_first(arr, k)
    tb = (time.perf_counter() - t0) / len(keys)
    t0 = time.perf_counter()
    for k in keys[:20]:
        next(i for i, o in enumerate(arr) if o[0] == k)
    tl = (time.perf_counter() - t0) / 20
    with open(out_csv, "w") as f:
        f.write("method,n,avg_seconds_per_lookup\n")
        f.write(f"binary_first,{n},{tb:.9f}\nlinear,{n},{tl:.9f}\n")
    print(f"\nAverage lookup in 1,000,000 orders: binary {tb * 1e6:.1f} microseconds, "
          f"linear {tl * 1e3:.2f} ms ({tl / tb:,.0f}x slower)")


if __name__ == "__main__":
    random.seed(3)
    demo()
    theory()
    table()
    timing("../../Supporting_Files/datasets/binary_search_timing.csv")
