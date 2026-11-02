import random
import time
import math
import numpy as np

random.seed(2026)
np.random.seed(2026)

mult_count = 0
add_count = 0

def make_matrix(n):
    m = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.randint(-9, 9))
        m.append(row)
    return m

def conventional(A, B):
    global mult_count
    n = len(A)
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                mult_count += 1
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C

def add(A, B):
    global add_count
    n = len(A)
    add_count += n * n
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    global add_count
    n = len(A)
    add_count += n * n
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def split(M):
    n = len(M)
    h = n // 2
    A11 = [row[:h] for row in M[:h]]
    A12 = [row[h:] for row in M[:h]]
    A21 = [row[:h] for row in M[h:]]
    A22 = [row[h:] for row in M[h:]]
    return A11, A12, A21, A22

def join(C11, C12, C21, C22):
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bottom = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bottom

def strassen(A, B):
    global mult_count
    n = len(A)
    if n == 1:
        mult_count += 1
        return [[A[0][0] * B[0][0]]]
    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)
    return join(C11, C12, C21, C22)

def next_power_of_two(n):
    p = 1
    while p < n:
        p *= 2
    return p

def pad_matrix(M, size):
    n = len(M)
    P = [[0] * size for i in range(size)]
    for i in range(n):
        for j in range(n):
            P[i][j] = M[i][j]
    return P

def strassen_any_size(A, B):
    n = len(A)
    size = next_power_of_two(n)
    PA = pad_matrix(A, size)
    PB = pad_matrix(B, size)
    PC = strassen(PA, PB)
    return [row[:n] for row in PC[:n]]

def np_conventional(A, B, leaf):
    n = A.shape[0]
    if n <= leaf:
        return A @ B
    h = n // 2
    A11, A12, A21, A22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    B11, B12, B21, B22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]
    C = np.empty((n, n))
    C[:h, :h] = np_conventional(A11, B11, leaf) + np_conventional(A12, B21, leaf)
    C[:h, h:] = np_conventional(A11, B12, leaf) + np_conventional(A12, B22, leaf)
    C[h:, :h] = np_conventional(A21, B11, leaf) + np_conventional(A22, B21, leaf)
    C[h:, h:] = np_conventional(A21, B12, leaf) + np_conventional(A22, B22, leaf)
    return C

def np_strassen(A, B, leaf):
    n = A.shape[0]
    if n <= leaf:
        return A @ B
    h = n // 2
    A11, A12, A21, A22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    B11, B12, B21, B22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]
    M1 = np_strassen(A11 + A22, B11 + B22, leaf)
    M2 = np_strassen(A21 + A22, B11, leaf)
    M3 = np_strassen(A11, B12 - B22, leaf)
    M4 = np_strassen(A22, B21 - B11, leaf)
    M5 = np_strassen(A11 + A12, B22, leaf)
    M6 = np_strassen(A21 - A11, B11 + B12, leaf)
    M7 = np_strassen(A12 - A22, B21 + B22, leaf)
    C = np.empty((n, n))
    C[:h, :h] = M1 + M4 - M5 + M7
    C[:h, h:] = M3 + M5
    C[h:, :h] = M2 + M4
    C[h:, h:] = M1 - M2 + M3 + M6
    return C

print("=" * 72)
print("Q4 : CONVENTIONAL VS STRASSEN MATRIX MULTIPLICATION")
print("=" * 72)

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
mult_count = 0
print("Demo 2x2 : A =", A, " B =", B)
print("Conventional :", conventional(A, B), " multiplications =", mult_count)
mult_count = 0
print("Strassen     :", strassen(A, B), " multiplications =", mult_count)
print()

print("Experiment 1 : correctness (pure Python, power-of-two sizes)")
for n in [2, 4, 8, 16, 32]:
    A = make_matrix(n)
    B = make_matrix(n)
    c1 = conventional(A, B)
    c2 = strassen(A, B)
    print("n = %-3d  results equal : %s" % (n, c1 == c2))
print()

print("Experiment 2 : correctness when n is NOT a power of two (padding)")
for n in [3, 5, 6, 10, 13, 20, 33]:
    A = make_matrix(n)
    B = make_matrix(n)
    c1 = conventional(A, B)
    c2 = strassen_any_size(A, B)
    size = next_power_of_two(n)
    print("n = %-3d padded to %-3d  equal : %-5s  extra work (size/n)^3 = %.2f" % (n, size, c1 == c2, (size / n) ** 3))
print()

print("Experiment 3 : multiplication and addition counts (recursion down to 1x1)")
print("%-6s %-14s %-14s %-14s %-14s" % ("n", "Conv mults", "Strassen mults", "Strassen adds", "n^2.807"))
count_rows = []
for k in range(1, 7):
    n = 2 ** k
    A = make_matrix(n)
    B = make_matrix(n)
    mult_count = 0
    conventional(A, B)
    cm = mult_count
    mult_count = 0
    add_count = 0
    strassen(A, B)
    print("%-6d %-14d %-14d %-14d %-14.0f" % (n, cm, mult_count, add_count, n ** math.log2(7)))
    count_rows.append((n, cm, mult_count, add_count))
print()

print("Experiment 4 : pure Python timing, recursion down to 1x1 (average of 3 runs)")
print("%-6s %-14s %-14s %-12s" % ("n", "Conventional", "Strassen", "Faster"))
py_rows = []
for n in [2, 4, 8, 16, 32, 64]:
    tc = 0
    ts = 0
    for r in range(3):
        A = make_matrix(n)
        B = make_matrix(n)
        start = time.perf_counter()
        conventional(A, B)
        tc += time.perf_counter() - start
        start = time.perf_counter()
        strassen(A, B)
        ts += time.perf_counter() - start
    tc /= 3
    ts /= 3
    if tc < ts:
        w = "Conventional"
    else:
        w = "Strassen"
    print("%-6d %-14.6f %-14.6f %-12s" % (n, tc, ts, w))
    py_rows.append((n, tc, ts))
print()

print("Experiment 5 : NumPy block versions, same leaf size (64), average of 3 runs (1 run for n = 4096)")
print("%-6s %-14s %-14s %-14s %-12s %-8s" % ("n", "Conv blocks", "Strassen", "np full (@)", "Faster", "Equal"))
np_rows = []
for n in [128, 256, 512, 1024, 2048, 4096]:
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    tc = 0
    ts = 0
    tf = 0
    runs = 3
    if n > 2048:
        runs = 1
    for r in range(runs):
        start = time.perf_counter()
        c1 = np_conventional(A, B, 64)
        tc += time.perf_counter() - start
        start = time.perf_counter()
        c2 = np_strassen(A, B, 64)
        ts += time.perf_counter() - start
        start = time.perf_counter()
        c3 = A @ B
        tf += time.perf_counter() - start
    tc /= runs
    ts /= runs
    tf /= runs
    if tc < ts:
        w = "Conventional"
    else:
        w = "Strassen"
    print("%-6d %-14.5f %-14.5f %-14.5f %-12s %-8s" % (n, tc, ts, tf, w, np.allclose(c1, c2) and np.allclose(c1, c3)))
    np_rows.append((n, tc, ts, tf))
print()

print("Experiment 6 : effect of the leaf size, n = 1024 (NumPy Strassen)")
print("%-10s %-14s" % ("Leaf", "Time (s)"))
A = np.random.rand(1024, 1024)
B = np.random.rand(1024, 1024)
for leaf in [16, 32, 64, 128, 256, 512]:
    start = time.perf_counter()
    np_strassen(A, B, leaf)
    print("%-10d %-14.5f" % (leaf, time.perf_counter() - start))
print()

print("Experiment 7 : padding cost, n = 1025 compared with n = 1024 (NumPy Strassen, leaf 64)")
for n in [1024, 1025]:
    size = next_power_of_two(n)
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    PA = np.zeros((size, size))
    PB = np.zeros((size, size))
    PA[:n, :n] = A
    PB[:n, :n] = B
    start = time.perf_counter()
    C = np_strassen(PA, PB, 64)[:n, :n]
    t = time.perf_counter() - start
    print("n = %-5d padded size = %-5d time = %.5f s   correct = %s" % (n, size, t, np.allclose(C, A @ B)))
