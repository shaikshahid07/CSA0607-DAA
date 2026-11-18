# Q4 Pseudocode - Conventional and Strassen Matrix Multiplication

## Conventional block multiplication (8 multiplications)

```
BLOCKMULT(A, B)           // n x n, n a power of 2
    if n == 1  return A * B
    split A into A11 A12 / A21 A22 and B into B11 B12 / B21 B22
    C11 = BLOCKMULT(A11,B11) + BLOCKMULT(A12,B21)
    C12 = BLOCKMULT(A11,B12) + BLOCKMULT(A12,B22)
    C21 = BLOCKMULT(A21,B11) + BLOCKMULT(A22,B21)
    C22 = BLOCKMULT(A21,B12) + BLOCKMULT(A22,B22)
    return joined C
```
T(n) = 8T(n/2) + O(n^2) -> Theta(n^3).

## Strassen (7 multiplications)

```
STRASSEN(A, B)
    if n == 1  return A * B
    split A and B into four n/2 x n/2 blocks each
    M1 = STRASSEN(A11 + A22, B11 + B22)
    M2 = STRASSEN(A21 + A22, B11)
    M3 = STRASSEN(A11, B12 - B22)
    M4 = STRASSEN(A22, B21 - B11)
    M5 = STRASSEN(A11 + A12, B22)
    M6 = STRASSEN(A21 - A11, B11 + B12)
    M7 = STRASSEN(A12 - A22, B21 + B22)
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    return joined C
```
T(n) = 7T(n/2) + 18(n/2)^2 -> Theta(n^(log2 7)) = Theta(n^2.807).

## Padding when n is not a power of two

```
STRASSENANY(A, B)
    size = smallest power of 2 >= n
    PA, PB = A and B copied into size x size zero matrices
    PC = STRASSEN(PA, PB)
    return top-left n x n part of PC
```
Extra cost: up to (size / n)^3 times more scalar multiplications for the conventional method (and (size/n)^2.807 for Strassen).
