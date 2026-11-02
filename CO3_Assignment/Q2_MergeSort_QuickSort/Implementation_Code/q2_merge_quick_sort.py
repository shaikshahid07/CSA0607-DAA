import random
import math
import time
import sys

random.seed(2026)
sys.setrecursionlimit(20000)

merge_comparisons = 0
merge_depth = 0

def merge_sort(a, depth):
    global merge_comparisons, merge_depth
    if depth > merge_depth:
        merge_depth = depth
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], depth + 1)
    right = merge_sort(a[mid:], depth + 1)
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        merge_comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result = result + left[i:] + right[j:]
    return result

quick_comparisons = 0
quick_depth = 0
partition_log = []

def quick_sort(a, depth):
    global quick_comparisons, quick_depth
    if depth > quick_depth:
        quick_depth = depth
    if len(a) <= 1:
        return a
    pivot = a[0]
    left = []
    right = []
    for x in a[1:]:
        quick_comparisons += 1
        if x < pivot:
            left.append(x)
        else:
            right.append(x)
    partition_log.append((depth, len(left), len(right)))
    return quick_sort(left, depth + 1) + [pivot] + quick_sort(right, depth + 1)

def build_balanced(sorted_list):
    if len(sorted_list) <= 1:
        return list(sorted_list)
    mid = len(sorted_list) // 2
    return [sorted_list[mid]] + build_balanced(sorted_list[:mid]) + build_balanced(sorted_list[mid + 1:])

def run_quick(data):
    global quick_comparisons, quick_depth, partition_log
    quick_comparisons = 0
    quick_depth = 0
    partition_log = []
    start = time.perf_counter()
    result = quick_sort(data, 1)
    t = time.perf_counter() - start
    return result, quick_comparisons, quick_depth, t

def run_merge(data):
    global merge_comparisons, merge_depth
    merge_comparisons = 0
    merge_depth = 0
    start = time.perf_counter()
    result = merge_sort(data, 1)
    t = time.perf_counter() - start
    return result, merge_comparisons, merge_depth, t

print("=" * 72)
print("Q2 : MERGE SORT AND QUICK SORT (pivot strategy = FIRST element)")
print("=" * 72)

demo = [38, 27, 43, 3, 9, 82, 10]
r, c, d, t = run_merge(demo)
print("Demo input        :", demo)
print("Merge sort output :", r, " comparisons =", c, " depth =", d)
r, c, d, t = run_quick(demo)
print("Quick sort output :", r, " comparisons =", c, " depth =", d)
print()

print("Experiment 1 : first three partitions, n = 15")
n = 15
base = list(range(1, n + 1))
balanced = build_balanced(base)
print("Balanced input  :", balanced)
run_quick(balanced)
for item in partition_log[:7]:
    print("   depth %d : left = %d, right = %d" % item)
print("Sorted input    :", base)
run_quick(base)
for item in partition_log[:7]:
    print("   depth %d : left = %d, right = %d" % item)
print()

print("Experiment 2 : comparisons, depth and time for different inputs")
print("%-7s %-12s | %-10s %-7s %-9s | %-10s %-7s %-9s" % ("n", "Input", "QS comps", "QS dep", "QS time", "MS comps", "MS dep", "MS time"))
sizes = [127, 255, 511, 1023, 2047]
table_rows = []
for n in sizes:
    base = list(range(1, n + 1))
    inputs = {
        "balanced": build_balanced(base),
        "random": random.sample(base, n),
        "sorted": list(base),
        "reversed": list(reversed(base)),
    }
    for name in ["balanced", "random", "sorted", "reversed"]:
        data = inputs[name]
        r1, qc, qd, qt = run_quick(data)
        r2, mc, md, mt = run_merge(data)
        ok = (r1 == base) and (r2 == base)
        print("%-7d %-12s | %-10d %-7d %-9.5f | %-10d %-7d %-9.5f %s" % (n, name, qc, qd, qt, mc, md, mt, "" if ok else "WRONG"))
        table_rows.append((n, name, qc, qd, qt, mc, md, mt))
print()

print("Experiment 3 : partition sizes for n = 1023 (first 5 partitions)")
base = list(range(1, 1024))
for name, data in [("balanced", build_balanced(base)), ("sorted", list(base))]:
    run_quick(data)
    print(name)
    for item in partition_log[:5]:
        print("   depth %d : left = %d, right = %d" % item)
print()

print("Experiment 4 : height of the recursion tree for different split ratios (n = 1,000,000)")
n = 1000000
print("%-10s %-22s %-15s" % ("Split", "Height formula", "Height"))
for ratio in [0.5, 0.25, 0.1, 0.01]:
    big = 1 - ratio
    height = math.log(n) / math.log(1 / big)
    print("%-10s log(n) / log(1/%.2f)    %-15.1f" % ("%d:%d" % (round(ratio * 100), round(big * 100)), big, height))
print("Totally unbalanced (1 : n-1) gives height n =", n)
print()

print("Experiment 5 : quick sort comparisons vs n^2/2 and n log2 n on sorted input")
print("%-8s %-14s %-14s %-14s" % ("n", "QS comps", "n(n-1)/2", "n log2 n"))
for n in [100, 200, 400, 800, 1600]:
    data = list(range(n))
    r, c, d, t = run_quick(data)
    print("%-8d %-14d %-14d %-14.0f" % (n, c, n * (n - 1) // 2, n * math.log2(n)))
