import math


def master_theorem(a, b, d):
    p = math.log(a, b)
    if round(d, 9) < round(p, 9):
        return "Case 1: Theta(n^" + str(round(p)) + ")"
    if round(d, 9) == round(p, 9):
        if round(p) == 1:
            return "Case 2: Theta(n log n)"
        return "Case 2: Theta(n^" + str(round(p)) + " log n)"
    return "Case 3: Theta(n^" + str(d) + ")"


def solve(a, f, kmax):
    values = [1]
    for k in range(1, kmax + 1):
        values.append(a * values[k - 1] + f(2 ** k, k))
    return values


print("M4 current   T(n) = 4T(n/2) + n : a=4 b=2 n^(log2 4)=n^2 f(n)=n")
print("  ", master_theorem(4, 2, 1))
print("M4 redesign  T(n) = 2T(n/2) + n : a=2 b=2 n^(log2 2)=n   f(n)=n")
print("  ", master_theorem(2, 2, 1))
print("M5  T(n) = 2T(n/2) + n log n : f(n)=n log n, n^(log2 2)=n")
print("   Not Case 1, 2 or 3 -> use recursion tree: Theta(n log^2 n)")

old = solve(4, lambda n, k: n, 20)
new = solve(2, lambda n, k: n, 20)
m5 = solve(2, lambda n, k: n * k, 20)

print()
print("  k        n     T_old(n)    2n^2-n    T_new(n)   n log n + n")
for k in [3, 10, 20]:
    n = 2 ** k
    print(f"{k:>3} {n:>8} {old[k]:>12} {2 * n * n - n:>9} "
          f"{new[k]:>11} {n * k + n:>11}")

print()
print("Doubling the data (n = 2^19 -> 2^20)")
print("  current  T(2n)/T(n) =", round(old[20] / old[19], 3))
print("  redesign T(2n)/T(n) =", round(new[20] / new[19], 3))
print("  M5       T(2n)/T(n) =", round(m5[20] / m5[19], 3))

print()
print("M5: T(n) / (n log^2 n) settles near a constant (0.5)")
for k in [5, 10, 15, 20]:
    n = 2 ** k
    print(f"  n = 2^{k:<2}  T/(n log n) = {m5[k] / (n * k):5.2f}"
          f"   T/(n log^2 n) = {m5[k] / (n * k * k):.3f}")
exact = all(m5[k] == 2 ** k * k * (k + 1) // 2 + 2 ** k for k in range(21))
print("Exact form T(n) = n*k(k+1)/2 + n matches for every k:", exact)
