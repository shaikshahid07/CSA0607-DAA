import math


def binary_search_iterative(arr, key):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        elif key < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons


def binary_search_recursive(arr, key, low, high, depth=1):
    if low > high:
        return -1, 0, depth
    mid = (low + high) // 2
    if arr[mid] == key:
        return mid, 1, depth
    if key < arr[mid]:
        idx, c, d = binary_search_recursive(arr, key, low, mid - 1, depth + 1)
    else:
        idx, c, d = binary_search_recursive(arr, key, mid + 1, high, depth + 1)
    return idx, c + 1, d


def T(n):
    if n == 1:
        return 1
    return T(n // 2) + 1


print("Backward substitution for n = 1024")
n = 1024
k = 0
while n >= 1:
    print(f"  k = {k:>2}:  T(1024) = T({n}) + {k}")
    n = n // 2
    k += 1
print("  T(1) = 1, so T(1024) = 1 + 10 =", T(1024))

print()
print("  n       worst case   log2(n)+1")
for p in range(1, 15):
    n = 2 ** p
    arr = [2 * x for x in range(n)]
    worst = 0
    for key in range(-1, 2 * n + 2):
        found, c = binary_search_iterative(arr, key)
        worst = max(worst, c)
    print(f"{n:>6} {worst:>12} {int(math.log2(n)) + 1:>12}")

print()
n = 1000000
arr = [2 * x for x in range(n)]
found, c = binary_search_iterative(arr, 2 * n - 2)
print("n = 1,000,000, iterative, search for last item:", c, "comparisons")
found, c, depth = binary_search_recursive(arr, 2 * n - 2, 0, n - 1)
print("n = 1,000,000, recursive, comparisons:", c, " stack depth:", depth)
print("floor(log2 n) + 1 =", int(math.log2(n)) + 1)
