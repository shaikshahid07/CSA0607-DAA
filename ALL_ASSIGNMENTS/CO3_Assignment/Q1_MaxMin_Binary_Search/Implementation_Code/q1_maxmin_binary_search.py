import random
random.seed(2026)
import math

count = 0

def max_min(a, low, high):
    global count
    if low == high:
        return a[low], a[low]
    if high == low + 1:
        count += 1
        if a[low] > a[high]:
            return a[low], a[high]
        return a[high], a[low]
    mid = (low + high) // 2
    max1, min1 = max_min(a, low, mid)
    max2, min2 = max_min(a, mid + 1, high)
    count += 1
    if max1 > max2:
        big = max1
    else:
        big = max2
    count += 1
    if min1 < min2:
        small = min1
    else:
        small = min2
    return big, small

def simple_max_min(a):
    c = 0
    big = a[0]
    small = a[0]
    for i in range(1, len(a)):
        c += 1
        if a[i] > big:
            big = a[i]
        c += 1
        if a[i] < small:
            small = a[i]
    return big, small, c

def binary_search(a, target):
    low = 0
    high = len(a) - 1
    c = 0
    while low <= high:
        mid = (low + high) // 2
        c += 1
        if a[mid] == target:
            return mid, c
        if a[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, c

def predicted_maxmin(n):
    return math.ceil(3 * n / 2) - 2

def recurrence_value(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    left = n // 2
    right = n - left
    return recurrence_value(left) + recurrence_value(right) + 2

print("=" * 70)
print("Q1 PART A : FINDING MAXIMUM AND MINIMUM (DIVIDE AND CONQUER)")
print("=" * 70)

small_list = [8, 3, 15, 1, 9, 22, 4, 7]
count = 0
big, small = max_min(small_list, 0, len(small_list) - 1)
print("Demo list      :", small_list)
print("Max, Min       :", big, small)
print("Comparisons    :", count)
print()

print("Experiment 1 : random data, sizes that are powers of two")
print("%-8s %-12s %-12s %-12s %-10s %-8s" % ("n", "Predicted", "Observed", "Straight", "Saved", "Correct"))
for k in range(1, 15):
    n = 2 ** k
    data = random.sample(range(1, 10 * n), n)
    count = 0
    big, small = max_min(data, 0, n - 1)
    sb, ss, sc = simple_max_min(data)
    ok = (big == max(data)) and (small == min(data))
    print("%-8d %-12d %-12d %-12d %-10d %-8s" % (n, predicted_maxmin(n), count, sc, sc - count, ok))
print()

print("Experiment 2 : sizes that are NOT powers of two")
print("%-8s %-12s %-12s %-12s %-12s %-8s" % ("n", "3n/2-2", "Recurrence", "Observed", "Straight", "Correct"))
for n in [3, 5, 6, 7, 10, 25, 100, 333, 1000, 5000, 12345]:
    data = random.sample(range(1, 10 * n), n)
    count = 0
    big, small = max_min(data, 0, n - 1)
    sb, ss, sc = simple_max_min(data)
    ok = (big == max(data)) and (small == min(data))
    print("%-8d %-12d %-12d %-12d %-12d %-8s" % (n, predicted_maxmin(n), recurrence_value(n), count, sc, ok))
print()
print("For n that is not a power of two the simple formula 3n/2-2 is only a lower estimate.")
print("The exact recurrence T(n)=T(n/2)+T(n-n/2)+2 matches the observed count every time.")
print()

print("Experiment 3 : different kinds of data (n = 1024)")
n = 1024
kinds = {
    "random": random.sample(range(1, 10 * n), n),
    "ascending": list(range(n)),
    "descending": list(range(n, 0, -1)),
    "all equal": [5] * n,
}
for name in kinds:
    data = kinds[name]
    count = 0
    big, small = max_min(data, 0, n - 1)
    print("%-12s comparisons = %d   (max=%d, min=%d)" % (name, count, big, small))
print()

print("=" * 70)
print("Q1 PART B : BINARY SEARCH")
print("=" * 70)

demo = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("Sorted list    :", demo)
for t in [23, 2, 91, 40]:
    pos, c = binary_search(demo, t)
    print("Search %-4d -> index %-3d  comparisons = %d" % (t, pos, c))
print()

print("Experiment 4 : successful and unsuccessful searches (every element tested)")
print("%-10s %-10s %-12s %-12s %-12s %-12s" % ("n", "log2(n)", "Best case", "Worst succ", "Avg succ", "Unsucc(max)"))
for k in [4, 6, 8, 10, 12, 14, 16, 18]:
    n = 2 ** k
    a = [2 * i for i in range(n)]
    counts = []
    unsucc = []
    for i in range(n):
        pos, c = binary_search(a, a[i])
        counts.append(c)
        pos, c = binary_search(a, a[i] + 1)
        unsucc.append(c)
    pos, c = binary_search(a, -1)
    unsucc.append(c)
    print("%-10d %-10d %-12d %-12d %-12.2f %-12d" % (n, k, min(counts), max(counts), sum(counts) / len(counts), max(unsucc)))
print()
print("Note: each loop pass counts as ONE comparison (the equality check at mid).")
print("Worst case should be floor(log2 n) + 1 comparisons (log2 n + 1 when n = 2^k).")
print()

print("Experiment 5 : one million element array, a few searches")
n = 1000000
a = list(range(0, 2 * n, 2))
for t in [a[0], a[n // 2], a[n - 1], 777, -5]:
    pos, c = binary_search(a, t)
    print("target %-9d index %-8d comparisons = %d" % (t, pos, c))
print("Linear search would need up to", n, "comparisons.  log2(n) =", round(math.log2(n), 2))
