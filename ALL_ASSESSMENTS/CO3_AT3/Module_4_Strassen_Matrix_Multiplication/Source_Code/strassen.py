"""
Module 4 - Recommendation Scores (KartIQ)
Strassen's matrix multiplication, conventional multiplication and a hybrid.

Run:  python3 strassen.py
Student: Shaik Shahid (192424311)  |  CSA06 CO3 Case Study
"""
import math
import random
import time

import numpy as np

mult_count = 0   # scalar multiplications counted by the pure-Python versions


# ---------------------------------------------------------------- pure Python helpers
def mat_add(A, B):
    return [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(A, B)]


def mat_sub(A, B):
    return [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(A, B)]


def conventional(A, B):
    global mult_count
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
                mult_count += 1
            C[i][j] = s
    return C


def split(M):
    h = len(M) // 2
    return ([r[:h] for r in M[:h]], [r[h:] for r in M[:h]],
            [r[:h] for r in M[h:]], [r[h:] for r in M[h:]])


def join(C11, C12, C21, C22):
    return [a + b for a, b in zip(C11, C12)] + [a + b for a, b in zip(C21, C22)]


def strassen(A, B, cutoff=1, verbose=False):
    """Strassen on 2^k x 2^k matrices. Falls back to conventional when n <= cutoff."""
    global mult_count
    n = len(A)
    if n <= cutoff:
        return conventional(A, B)
    A11, A12, A21, A22 = split(A)               # DIVIDE
    B11, B12, B21, B22 = split(B)
    M1 = strassen(mat_add(A11, A22), mat_add(B11, B22), cutoff, verbose)   # CONQUER: 7 products
    M2 = strassen(mat_add(A21, A22), B11, cutoff, verbose)
    M3 = strassen(A11, mat_sub(B12, B22), cutoff, verbose)
    M4 = strassen(A22, mat_sub(B21, B11), cutoff, verbose)
    M5 = strassen(mat_add(A11, A12), B22, cutoff, verbose)
    M6 = strassen(mat_sub(A21, A11), mat_add(B11, B12), cutoff, verbose)
    M7 = strassen(mat_sub(A12, A22), mat_add(B21, B22), cutoff, verbose)
    if verbose:
        print("  M1..M7 =", [M[0][0] for M in (M1, M2, M3, M4, M5, M6, M7)])
    C11 = mat_add(mat_sub(mat_add(M1, M4), M5), M7)   # COMBINE: 8 add/sub on blocks
    C12 = mat_add(M3, M5)
    C21 = mat_add(M2, M4)
    C22 = mat_add(mat_add(mat_sub(M1, M2), M3), M6)
    return join(C11, C12, C21, C22)


# ---------------------------------------------------------------- numpy hybrid (for timing)
def strassen_np(A, B, cutoff):
    n = A.shape[0]
    if n <= cutoff:
        return A @ B                                  # optimised conventional kernel at the leaves
    h = n // 2
    A11, A12, A21, A22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    B11, B12, B21, B22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]
    M1 = strassen_np(A11 + A22, B11 + B22, cutoff)
    M2 = strassen_np(A21 + A22, B11, cutoff)
    M3 = strassen_np(A11, B12 - B22, cutoff)
    M4 = strassen_np(A22, B21 - B11, cutoff)
    M5 = strassen_np(A11 + A12, B22, cutoff)
    M6 = strassen_np(A21 - A11, B11 + B12, cutoff)
    M7 = strassen_np(A12 - A22, B21 + B22, cutoff)
    C = np.empty_like(A)
    C[:h, :h] = M1 + M4 - M5 + M7
    C[:h, h:] = M3 + M5
    C[h:, :h] = M2 + M4
    C[h:, h:] = M1 - M2 + M3 + M6
    return C


def naive_np(A, B):
    """Triple-loop conventional method, vectorised only on the inner dot product (Python loops)."""
    n = A.shape[0]
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            C[i, j] = float(np.dot(A[i, :], B[:, j]))
    return C


# ---------------------------------------------------------------- counting formulas
def strassen_mults(n, cutoff=1):
    """Scalar multiplications: 7 T(n/2) down to cutoff, then n^3 per leaf."""
    return n ** 3 if n <= cutoff else 7 * strassen_mults(n // 2, cutoff)


def strassen_adds(n, cutoff=1):
    """Scalar additions/subtractions: 18 (n/2)^2 per level, leaf n^2 (n-1)."""
    if n <= cutoff:
        return n * n * (n - 1)
    return 7 * strassen_adds(n // 2, cutoff) + 18 * (n // 2) ** 2


# ---------------------------------------------------------------- demos
def demo_sample():
    global mult_count
    A = [[1, 7], [3, 5]]
    B = [[1, 3], [7, 5]]
    print("=" * 70)
    print("MODULE 4 - STRASSEN on the 2 x 2 sample")
    print("=" * 70)
    print("A =", A, " B =", B)
    a11, a12, a21, a22 = A[0][0], A[0][1], A[1][0], A[1][1]
    b11, b12, b21, b22 = B[0][0], B[0][1], B[1][0], B[1][1]
    M1 = (a11 + a22) * (b11 + b22)
    M2 = (a21 + a22) * b11
    M3 = a11 * (b12 - b22)
    M4 = a22 * (b21 - b11)
    M5 = (a11 + a12) * b22
    M6 = (a21 - a11) * (b11 + b12)
    M7 = (a12 - a22) * (b21 + b22)
    print(f"M1 = (a11+a22)(b11+b22) = ({a11}+{a22})({b11}+{b22}) = {M1}")
    print(f"M2 = (a21+a22) b11      = ({a21}+{a22})({b11})       = {M2}")
    print(f"M3 = a11 (b12-b22)      = {a11}({b12}-{b22})         = {M3}")
    print(f"M4 = a22 (b21-b11)      = {a22}({b21}-{b11})         = {M4}")
    print(f"M5 = (a11+a12) b22      = ({a11}+{a12})({b22})       = {M5}")
    print(f"M6 = (a21-a11)(b11+b12) = ({a21}-{a11})({b11}+{b12}) = {M6}")
    print(f"M7 = (a12-a22)(b21+b22) = ({a12}-{a22})({b21}+{b22}) = {M7}")
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    print(f"C11 = M1+M4-M5+M7 = {M1}+{M4}-{M5}+{M7} = {C11}")
    print(f"C12 = M3+M5       = {M3}+{M5} = {C12}")
    print(f"C21 = M2+M4       = {M2}+{M4} = {C21}")
    print(f"C22 = M1-M2+M3+M6 = {M1}-{M2}+{M3}+{M6} = {C22}")
    S = [[C11, C12], [C21, C22]]
    mult_count = 0
    conv = conventional(A, B)
    print("Strassen result    :", S)
    print("Conventional result:", conv, f"(8 multiplications; Strassen used 7)")
    assert S == conv
    print("Verification: MATCH")
    print("Library function strassen():", strassen(A, B, cutoff=1, verbose=True))

    print("\nA 4 x 4 check (random integers) with full recursion:")
    random.seed(4)
    A4 = [[random.randint(-5, 9) for _ in range(4)] for _ in range(4)]
    B4 = [[random.randint(-5, 9) for _ in range(4)] for _ in range(4)]
    assert strassen(A4, B4) == conventional(A4, B4)
    print("  strassen(A4,B4) == conventional(A4,B4): MATCH")
    print("  mults conventional =", 4 ** 3, " Strassen =", strassen_mults(4), "(7^2)")


def theory():
    print("\n" + "=" * 70)
    print("SCALAR OPERATIONS FOR n = 1024")
    print("=" * 70)
    n = 1024
    k = int(math.log2(n))
    conv_m = n ** 3
    conv_a = n * n * (n - 1)
    print(f"Conventional: multiplications n^3 = {conv_m:,}; additions n^2(n-1) = {conv_a:,}; total = {conv_m + conv_a:,}")
    print(f"Strassen (full recursion to 1x1): multiplications 7^{k} = {strassen_mults(n):,}")
    print(f"   multiplication ratio = {strassen_mults(n) / conv_m:.4f}  (saving {100 * (1 - strassen_mults(n) / conv_m):.1f}%)")
    print(f"   additions 6(7^{k}-4^{k}) = {strassen_adds(n):,}; total = {strassen_mults(n) + strassen_adds(n):,}")
    print(f"   exponent log2(7) = {math.log2(7):.4f};  n^log2(7) = {n ** math.log2(7):,.0f}")
    print("\nHybrid: Strassen above the cutoff, conventional at the leaves")
    print(f"{'cutoff':>7} {'multiplications':>16} {'additions':>16} {'total ops':>16} {'vs conventional':>16}")
    for c in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024):
        m, a = strassen_mults(n, c), strassen_adds(n, c)
        print(f"{c:>7} {m:>16,} {a:>16,} {m + a:>16,} {(m + a) / (conv_m + conv_a):>15.3f}x")
    mb = n * n * 8 / 2 ** 20
    print(f"\nMemory: one 1024x1024 float64 matrix = {mb:.0f} MiB; A, B, C = {3 * mb:.0f} MiB.")
    print(f"Strassen temporaries (M1..M7 and the block sums) need about 3n^2 elements = {3 * mb:.0f} MiB extra "
          f"with the straightforward implementation (geometric sum over the recursion levels).")


def timing(out_csv):
    print("\nTIMING (numpy, float64)")
    rows = []
    np.random.seed(5)
    print(f"{'n':>6} {'conv(py loops)':>15} {'numpy BLAS':>11} {'Strassen c=1':>13} {'hybrid c=64':>12} {'hybrid c=128':>13}")
    for n in (64, 128, 256, 512, 1024):
        A, B = np.random.rand(n, n), np.random.rand(n, n)
        t = {}
        if n <= 256:
            t0 = time.perf_counter(); C0 = naive_np(A, B); t["conv"] = time.perf_counter() - t0
        else:
            t["conv"] = float("nan")
        t0 = time.perf_counter(); Cb = A @ B; t["blas"] = time.perf_counter() - t0
        if n <= 256:
            t0 = time.perf_counter(); C1 = strassen_np(A, B, 1); t["s1"] = time.perf_counter() - t0
            assert np.allclose(C1, Cb)
        else:
            t["s1"] = float("nan")
        t0 = time.perf_counter(); C64 = strassen_np(A, B, 64); t["h64"] = time.perf_counter() - t0
        t0 = time.perf_counter(); C128 = strassen_np(A, B, 128); t["h128"] = time.perf_counter() - t0
        assert np.allclose(C64, Cb) and np.allclose(C128, Cb)
        rows.append((n, t["conv"], t["blas"], t["s1"], t["h64"], t["h128"]))
        print(f"{n:>6} {t['conv']:>15.4f} {t['blas']:>11.4f} {t['s1']:>13.4f} {t['h64']:>12.4f} {t['h128']:>13.4f}")
    with open(out_csv, "w") as f:
        f.write("n,conventional_loops_s,numpy_blas_s,strassen_cutoff1_s,hybrid64_s,hybrid128_s\n")
        for r in rows:
            f.write(str(r[0]) + "," + ",".join(f"{x:.6f}" if x == x else "" for x in r[1:]) + "\n")

    print("\nCutoff experiment, n = 512 (numpy leaves, float64):")
    n = 512
    A, B = np.random.rand(n, n), np.random.rand(n, n)
    cut_rows = []
    for c in (8, 16, 32, 64, 128, 256, 512):
        best = min(_time(lambda: strassen_np(A, B, c)) for _ in range(3))
        cut_rows.append((c, best))
        print(f"  cutoff {c:>4}: {best:.4f}s")
    with open(out_csv.replace("strassen_timing", "strassen_cutoff"), "w") as f:
        f.write("cutoff,seconds\n")
        for c, s in cut_rows:
            f.write(f"{c},{s:.6f}\n")


def _time(fn):
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


if __name__ == "__main__":
    demo_sample()
    theory()
    timing("../../Supporting_Files/datasets/strassen_timing.csv")
