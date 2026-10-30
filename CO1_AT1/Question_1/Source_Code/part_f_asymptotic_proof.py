import math


def f(n):
    return 3 * n * n + 10 * n * math.log2(n) + 50


c1 = 3
c2 = 63
n0 = 1

print("Claim: c1 * n^2 <= f(n) <= c2 * n^2 for all n >= n0")
print("c1 =", c1, " c2 =", c2, " n0 =", n0)

ok = True
smallest = 1000
largest = 0
for n in range(n0, 1000001):
    ratio = f(n) / (n * n)
    smallest = min(smallest, ratio)
    largest = max(largest, ratio)
    if not (c1 * n * n <= f(n) <= c2 * n * n):
        ok = False
result = "bound holds" if ok else "FAILED"
print("Checked every n from 1 to 1,000,000 ->", result)
print("Smallest f(n)/n^2 =", round(smallest, 4))
print("Largest  f(n)/n^2 =", round(largest, 4))

print()
print("  n          f(n)         f(n)/n^2     f(n)/n")
for n in [10, 100, 1000, 100000, 1000000]:
    print(f"{n:>8} {f(n):>16.0f} {f(n) / n ** 2:>12.4f} {f(n) / n:>12.1f}")

print()
print("f(n) is not O(n): f(n)/n keeps growing, so no constant c works")
for c in [100, 1000, 100000]:
    n = 1
    while f(n) <= c * n:
        n += 1
    print(f"  for c = {c:>6}, f(n) > c*n already at n = {n}")
