import random
import time
import sys

random.seed(2026)
sys.setrecursionlimit(20000)

ops = 0

def design_a(a, low, high):
    global ops
    if low == high:
        return a[low]
    mid = (low + high) // 2
    left_best = design_a(a, low, mid)
    right_best = design_a(a, mid + 1, high)
    ops += 1
    if left_best > right_best:
        return left_best
    return right_best

def crossing_sum(a, low, mid, high):
    global ops
    best_left = float("-inf")
    total = 0
    for i in range(mid, low - 1, -1):
        total += a[i]
        ops += 1
        if total > best_left:
            best_left = total
    best_right = float("-inf")
    total = 0
    for i in range(mid + 1, high + 1):
        total += a[i]
        ops += 1
        if total > best_right:
            best_right = total
    return best_left + best_right

def design_scan(a, low, high):
    global ops
    if low == high:
        return a[low]
    mid = (low + high) // 2
    left_best = design_scan(a, low, mid)
    right_best = design_scan(a, mid + 1, high)
    cross = crossing_sum(a, low, mid, high)
    ops += 2
    return max(left_best, right_best, cross)

def design_b(a, low, high):
    global ops
    if low == high:
        return a[low], a[low], a[low], a[low]
    mid = (low + high) // 2
    l_total, l_prefix, l_suffix, l_best = design_b(a, low, mid)
    r_total, r_prefix, r_suffix, r_best = design_b(a, mid + 1, high)
    total = l_total + r_total
    ops += 1
    prefix = max(l_prefix, l_total + r_prefix)
    ops += 1
    suffix = max(r_suffix, r_total + l_suffix)
    ops += 1
    best = max(l_best, r_best, l_suffix + r_prefix)
    ops += 2
    return total, prefix, suffix, best

def joint_final(a):
    total, prefix, suffix, best = design_b(a, 0, len(a) - 1)
    return best

def brute_force(a):
    global ops
    best = float("-inf")
    n = len(a)
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += a[j]
            ops += 1
            if total > best:
                best = total
    return best

def kadane(a):
    best = a[0]
    current = a[0]
    for x in a[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best

print("=" * 72)
print("Q7 : DAY-4 DESIGN CHALLENGE - MAXIMUM SUBARRAY SUM (DIVIDE AND CONQUER)")
print("=" * 72)

demo = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("Demo array :", demo)
print("Student A initial design (best of the two halves only) :", design_a(demo, 0, len(demo) - 1))
print("Student B initial design (total, prefix, suffix, best) :", design_b(demo, 0, len(demo) - 1)[3])
print("Joint final design                                     :", joint_final(demo))
print("Brute force baseline                                   :", brute_force(demo))
print("Kadane (independent check)                             :", kadane(demo))
print("Correct answer is 6 from the subarray [4, -1, 2, 1] which crosses the middle.")
print()

print("Experiment 1 : designed correctness test cases")
cases = [
    ("single element", [7]),
    ("two elements", [-1, 3]),
    ("all negative", [-8, -3, -6, -2, -5, -4]),
    ("all positive", [1, 2, 3, 4, 5]),
    ("answer in left half", [5, 4, -10, 1, 1, 1]),
    ("answer in right half", [1, -1, -10, 6, 7, -2]),
    ("answer crosses middle", [-2, 1, -3, 4, -1, 2, 1, -5, 4]),
    ("whole array", [3, -1, 3, -1, 3]),
    ("zeros and negatives", [0, -1, 0, -2, 0]),
    ("odd length", [2, -5, 4, -1, 3, -6, 2]),
]
print("%-24s %-8s %-8s %-8s %-8s %-8s" % ("Case", "Brute", "Kadane", "A", "B", "Final"))
for name, arr in cases:
    b = brute_force(arr)
    k = kadane(arr)
    a_res = design_a(arr, 0, len(arr) - 1)
    b_res = design_b(arr, 0, len(arr) - 1)[3]
    f = joint_final(arr)
    flag = ""
    if a_res != b:
        flag = "  <- design A fails"
    print("%-24s %-8d %-8d %-8d %-8d %-8d%s" % (name, b, k, a_res, b_res, f, flag))
print()

print("Experiment 2 : 2000 random arrays (length 1 to 60, values -50 to 50)")
bad_a = 0
bad_scan = 0
bad_final = 0
for i in range(2000):
    n = random.randint(1, 60)
    arr = [random.randint(-50, 50) for j in range(n)]
    expected = brute_force(arr)
    if design_a(arr, 0, n - 1) != expected:
        bad_a += 1
    if design_scan(arr, 0, n - 1) != expected:
        bad_scan += 1
    if joint_final(arr) != expected or kadane(arr) != expected:
        bad_final += 1
print("Design A wrong answers      :", bad_a, "out of 2000")
print("Crossing-scan version wrong :", bad_scan)
print("Joint final design wrong    :", bad_final)
print()

print("Experiment 3 : counted operations for increasing n")
print("%-8s %-14s %-14s %-14s %-12s %-12s" % ("n", "Brute n(n+1)/2", "Scan version", "Joint final", "n log2 n", "5(n-1)"))
rows = []
for k in range(4, 14):
    n = 2 ** k
    arr = [random.randint(-100, 100) for j in range(n)]
    ops = 0
    brute_force(arr)
    ob = ops
    ops = 0
    design_scan(arr, 0, n - 1)
    os_ = ops
    ops = 0
    design_b(arr, 0, n - 1)
    of = ops
    print("%-8d %-14d %-14d %-14d %-12d %-12d" % (n, ob, os_, of, n * k, 5 * (n - 1)))
    rows.append((n, ob, os_, of))
print("Joint final design performs exactly 5(n-1) counted operations : a straight line in n.")
print()

print("Experiment 4 : timing in seconds (average of 3 runs)")
print("%-8s %-12s %-12s %-12s %-12s" % ("n", "Brute", "Scan D&C", "Joint final", "Kadane"))
for n in [100, 500, 1000, 2000, 4000, 8000, 16000, 64000, 256000]:
    tb = 0
    ts = 0
    tf = 0
    tk = 0
    runs = 3
    for r in range(runs):
        arr = [random.randint(-100, 100) for j in range(n)]
        if n <= 4000:
            start = time.perf_counter()
            brute_force(arr)
            tb += time.perf_counter() - start
        start = time.perf_counter()
        design_scan(arr, 0, n - 1)
        ts += time.perf_counter() - start
        start = time.perf_counter()
        joint_final(arr)
        tf += time.perf_counter() - start
        start = time.perf_counter()
        kadane(arr)
        tk += time.perf_counter() - start
    if n <= 4000:
        brute_text = "%.5f" % (tb / runs)
    else:
        brute_text = "skipped"
    print("%-8d %-12s %-12.5f %-12.5f %-12.5f" % (n, brute_text, ts / runs, tf / runs, tk / runs))
print()

print("Experiment 5 : doubling test for the joint final design")
previous = None
print("%-8s %-14s %-10s" % ("n", "Operations", "Ratio"))
for k in range(10, 17):
    n = 2 ** k
    arr = [random.randint(-100, 100) for j in range(n)]
    ops = 0
    design_b(arr, 0, n - 1)
    if previous is None:
        ratio = "-"
    else:
        ratio = "%.3f" % (ops / previous)
    print("%-8d %-14d %-10s" % (n, ops, ratio))
    previous = ops
print("A ratio of about 2 when n doubles means linear growth, which matches T(n) = 2T(n/2) + O(1).")
