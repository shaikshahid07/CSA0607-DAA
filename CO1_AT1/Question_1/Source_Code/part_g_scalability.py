import math
import random
import time

SPEED = 100000000
WINDOW = 600


def nice_time(seconds):
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} microseconds"
    if seconds < 60:
        return f"{seconds:.3f} seconds"
    if seconds < 7200:
        return f"{seconds / 60:.1f} minutes"
    return f"{seconds / 3600:.1f} hours"


def operations(n):
    L = math.log2(n)
    return [
        ("M1 duplicate detector", n * (n - 1) // 2),
        ("M2 rate limiter", 2 ** math.ceil(L) - 1),
        ("S2 binary search", int(L) + 1),
        ("M4 current design", 2 * n * n - n),
        ("M4 redesign", n * L + n),
        ("M5 analytics engine", n * L * (L + 1) / 2 + n),
        ("Report generator f(n)", 3 * n * n + 10 * n * L + 50),
    ]


for n in [100000, 1000000]:
    print(f"n = {n:,}")
    print(f"{'Module':<24}{'Operations':>20}{'Time':>20}  Status")
    for name, ops in operations(n):
        seconds = ops / SPEED
        status = "OK" if seconds <= WINDOW else "FAILS"
        print(f"{name:<24}{ops:>20,.0f}{nice_time(seconds):>20}  {status}")
    print()


def find_duplicates_slow(products):
    found = set()
    for i in range(len(products) - 1):
        for j in range(i + 1, len(products)):
            if products[i] == products[j]:
                found.add(j)
    return found


def find_duplicates_fast(products):
    seen = set()
    found = set()
    for j in range(len(products)):
        if products[j] in seen:
            found.add(j)
        else:
            seen.add(products[j])
    return found


random.seed(1)
products = []
for _ in range(4000):
    title = "Item" + str(random.randint(1, 2000))
    seller = "S" + str(random.randint(1, 3))
    products.append((title, seller))
start = time.time()
slow = find_duplicates_slow(products)
slow_time = time.time() - start
start = time.time()
fast = find_duplicates_fast(products)
fast_time = time.time() - start
print("M1 redesign test with 4,000 products")
print("  nested loops :", len(slow), "duplicates,",
      round(slow_time, 3), "seconds")
print("  hash set     :", len(fast), "duplicates,",
      round(fast_time, 5), "seconds")
print("  same answer  :", slow == fast)
