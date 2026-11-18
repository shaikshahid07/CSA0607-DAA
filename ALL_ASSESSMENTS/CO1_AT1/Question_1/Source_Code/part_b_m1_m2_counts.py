import math


def m1_duplicate_detector(products):
    n = len(products)
    comparisons = 0
    duplicates = []
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            comparisons += 1
            if products[i] == products[j]:
                duplicates.append(j)
    return comparisons, duplicates


def m2_rate_limiter(n):
    audits = 0
    rounds = 0
    i = 1
    while i < n:
        for j in range(0, i):
            audits += 1
        i = i * 2
        rounds += 1
    return audits, rounds


print("M1 - Duplicate Listing Detector")
sample = [("Pen", "A"), ("Book", "B"), ("Pen", "A"),
          ("Bag", "C"), ("Book", "B"), ("Cup", "D")]
count, dups = m1_duplicate_detector(sample)
print("Sample products :", len(sample))
print("Comparisons     :", count, "(formula n(n-1)/2 =", 6 * 5 // 2, ")")
print("Duplicates found at positions:", dups)
print()
print("  n    counted   n(n-1)/2")
for n in [5, 10, 100, 1000]:
    products = [("P" + str(k), "S") for k in range(n)]
    counted, _ = m1_duplicate_detector(products)
    print(f"{n:>5} {counted:>9} {n * (n - 1) // 2:>10}")

print()
print("M2 - API Rate Limiter")
print("  n    counted   2^ceil(log2 n)-1   n*log2(n)")
for n in [8, 100, 1000, 1024, 5000]:
    counted, rounds = m2_rate_limiter(n)
    formula = 2 ** math.ceil(math.log2(n)) - 1
    print(f"{n:>5} {counted:>9} {formula:>17} {n * math.log2(n):>12.0f}")

print()
print("Check for n = 1024")
total = 0
i = 1
while i < 1024:
    print("  i =", i, "-> inner loop runs", i, "times")
    total += i
    i = i * 2
print("Total Audit operations =", total)
print("Claimed n log n        =", 1024 * 10)
