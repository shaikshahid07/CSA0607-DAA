import random
import time
import math
import sys

random.seed(2026)
sys.setrecursionlimit(10000)

school_count = 0
kara_count = 0

def to_digits(x):
    digits = []
    for ch in str(x)[::-1]:
        digits.append(int(ch))
    return digits

def standard_multiply(x, y):
    global school_count
    a = to_digits(x)
    b = to_digits(y)
    result = [0] * (len(a) + len(b))
    for i in range(len(a)):
        carry = 0
        for j in range(len(b)):
            school_count += 1
            total = result[i + j] + a[i] * b[j] + carry
            result[i + j] = total % 10
            carry = total // 10
        result[i + len(b)] += carry
    answer = 0
    for d in reversed(result):
        answer = answer * 10 + d
    return answer

def karatsuba(x, y):
    global kara_count
    if x < 10 or y < 10:
        kara_count += 1
        return x * y
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    p = 10 ** m
    x_high, x_low = divmod(x, p)
    y_high, y_low = divmod(y, p)
    z0 = karatsuba(x_low, y_low)
    z2 = karatsuba(x_high, y_high)
    z1 = karatsuba(x_low + x_high, y_low + y_high) - z0 - z2
    return z2 * p * p + z1 * p + z0

def karatsuba_hybrid(x, y, cutoff):
    if x < 10 or y < 10:
        return x * y
    if x < 10 ** cutoff or y < 10 ** cutoff:
        return standard_multiply_quiet(x, y)
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    p = 10 ** m
    x_high, x_low = divmod(x, p)
    y_high, y_low = divmod(y, p)
    z0 = karatsuba_hybrid(x_low, y_low, cutoff)
    z2 = karatsuba_hybrid(x_high, y_high, cutoff)
    z1 = karatsuba_hybrid(x_low + x_high, y_low + y_high, cutoff) - z0 - z2
    return z2 * p * p + z1 * p + z0

def standard_multiply_quiet(x, y):
    a = to_digits(x)
    b = to_digits(y)
    result = [0] * (len(a) + len(b))
    for i in range(len(a)):
        carry = 0
        for j in range(len(b)):
            total = result[i + j] + a[i] * b[j] + carry
            result[i + j] = total % 10
            carry = total // 10
        result[i + len(b)] += carry
    answer = 0
    for d in reversed(result):
        answer = answer * 10 + d
    return answer

def random_number(digits):
    first = random.randint(1, 9)
    rest = ""
    for i in range(digits - 1):
        rest += str(random.randint(0, 9))
    return int(str(first) + rest)

print("=" * 72)
print("Q3 : KARATSUBA MULTIPLICATION VS STANDARD (SCHOOL-BOOK) MULTIPLICATION")
print("=" * 72)

x = 1234
y = 5678
print("Demo : %d x %d" % (x, y))
p = 100
xh, xl = divmod(x, p)
yh, yl = divmod(y, p)
print("x = %d*10^2 + %d    y = %d*10^2 + %d" % (xh, xl, yh, yl))
z0 = xl * yl
z2 = xh * yh
z1 = (xl + xh) * (yl + yh) - z0 - z2
print("z0 = %d   z2 = %d   z1 = %d" % (z0, z2, z1))
print("z2*10^4 + z1*10^2 + z0 = %d" % (z2 * 10000 + z1 * 100 + z0))
kara_count = 0
school_count = 0
print("karatsuba  =", karatsuba(x, y), " standard =", standard_multiply(x, y), " python =", x * y)
print()

print("Experiment 1 : correctness on 200 random pairs (1 to 300 digits)")
bad = 0
for i in range(200):
    a = random_number(random.randint(1, 300))
    b = random_number(random.randint(1, 300))
    if karatsuba(a, b) != a * b or standard_multiply(a, b) != a * b:
        bad += 1
print("Wrong answers :", bad)
print()

print("Experiment 2 : single-digit multiplication counts (n-digit numbers)")
print("%-8s %-14s %-14s %-14s %-10s" % ("n", "Standard n^2", "Karatsuba", "n^1.585", "Ratio"))
count_rows = []
for k in range(1, 11):
    n = 2 ** k
    a = random_number(n)
    b = random_number(n)
    school_count = 0
    kara_count = 0
    standard_multiply(a, b)
    karatsuba(a, b)
    print("%-8d %-14d %-14d %-14.0f %-10.2f" % (n, school_count, kara_count, n ** math.log2(3), school_count / kara_count))
    count_rows.append((n, school_count, kara_count))
print()

print("Experiment 3 : timing (average of 7 runs, seconds)")
print("%-8s %-14s %-14s %-12s" % ("n", "Standard", "Karatsuba", "Faster"))
time_rows = []
sizes = [4, 8, 16, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024]
for n in sizes:
    t_std = 0
    t_kar = 0
    runs = 7
    for r in range(runs):
        a = random_number(n)
        b = random_number(n)
        start = time.perf_counter()
        standard_multiply_quiet(a, b)
        t_std += time.perf_counter() - start
        start = time.perf_counter()
        karatsuba(a, b)
        t_kar += time.perf_counter() - start
    t_std /= runs
    t_kar /= runs
    if t_std < t_kar:
        winner = "Standard"
    else:
        winner = "Karatsuba"
    print("%-8d %-14.6f %-14.6f %-12s" % (n, t_std, t_kar, winner))
    time_rows.append((n, t_std, t_kar))
print()

print("Experiment 4 : hybrid Karatsuba (switch to standard below a cutoff), n = 1024 digits")
print("%-12s %-14s" % ("Cutoff", "Time (s)"))
for cutoff in [1, 4, 8, 16, 32, 64, 128]:
    total = 0
    runs = 5
    for r in range(runs):
        a = random_number(1024)
        b = random_number(1024)
        start = time.perf_counter()
        res = karatsuba_hybrid(a, b, cutoff)
        total += time.perf_counter() - start
        if res != a * b:
            print("WRONG")
    print("%-12d %-14.6f" % (cutoff, total / runs))
print()

crossover = None
for i in range(len(time_rows)):
    stays = True
    for j in range(i, len(time_rows)):
        if time_rows[j][2] >= time_rows[j][1]:
            stays = False
    if stays:
        crossover = time_rows[i][0]
        break
print("Approximate crossover (Karatsuba wins from this size onwards) :", crossover, "digits")
