import math
from functools import lru_cache


def sequential_search(arr, key):
    comparisons = 0
    for x in arr:
        comparisons += 1
        if x == key:
            return comparisons
    return comparisons


def binary_search(arr, key):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return comparisons
        elif key < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return comparisons


@lru_cache(maxsize=None)
def total_comparisons(n):
    if n == 0:
        return 0
    left = (n - 1) // 2
    return n + total_comparisons(left) + total_comparisons(n - 1 - left)


print("S1 - Sequential search, n = 10")
arr = list(range(10))
print("  best  (first item)        :", sequential_search(arr, 0))
print("  worst (last item / absent):", sequential_search(arr, 9),
      "/", sequential_search(arr, 99))
found_avg = sum(sequential_search(arr, k) for k in arr) / 10
print("  average when found        :", found_avg, "= (n+1)/2")
p = 0.5
avg = p * found_avg + (1 - p) * 10
print("  average with p = 0.5      :", avg, "= n(1 - p/2) + p/2")

print()
n = 1000000
p = 0.5
print("S1, n = 1,000,000 and p = 0.5")
print("  found   : (n+1)/2 =", (n + 1) / 2)
print("  absent  : n       =", n)
print("  average : 0.5 x 500000.5 + 0.5 x 1000000 =",
      p * (n + 1) / 2 + (1 - p) * n)

print()
print("S2 - Binary search, n = 15 (every item tried)")
arr = list(range(15))
counts = [binary_search(arr, k) for k in arr]
print("  best :", min(counts), " worst:", max(counts),
      " average:", round(sum(counts) / 15, 3))

print()
print("S2, n = 1,000,000")
print("  best    : 1 comparison (key is the middle item)")
print("  worst   :", int(math.log2(n)) + 1, "comparisons = floor(log2 n) + 1")
print("  average :", round(total_comparisons(n) / n, 3),
      "comparisons (about log2 n - 1)")
check = list(range(1000))
real = sum(binary_search(check, k) for k in check)
print("  formula check for n = 1000:", real == total_comparisons(1000))
