# Task 7 - Solve the Recurrence Relation (4 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

Recurrence from Task 6: C(n) = C(floor(n/2)) + 1 for n >= 1, C(0) = 0, equivalently T(n) = T(n/2) + c.

### Method 1 - Iteration (backward substitution)

This method is suitable because the recurrence has a single recursive term, so repeated expansion produces a simple pattern. Take n = 2^k to remove the floor function:

```text
T(n) = T(n/2) + c
```

```text
     = T(n/4) + c + c = T(n/4) + 2c
```

```text
     = T(n/8) + 3c
```

```text
     ...  = T(n/2^i) + i c
```

The expansion stops at the base case n/2^i = 1, i.e. i = log2 n. With T(1) = T(0) + c = c0 + c:

```text
T(n) = T(1) + c log2 n = c log2 n + (c0 + c)   =   Theta(log n)
```

### Method 2 - Substitution (proof for all n, not only powers of 2)

Claim: C(n) = floor(log2 n) + 1 for all n >= 1.

Basis: C(1) = C(0) + 1 = 1 = floor(log2 1) + 1. Inductive step: assume the claim for all values below n (n >= 2). Then

```text
C(n) = C(floor(n/2)) + 1 = floor(log2 floor(n/2)) + 1 + 1 = (floor(log2 n) - 1) + 2 = floor(log2 n) + 1
```

using floor(log2 floor(n/2)) = floor(log2 n) - 1 for n >= 2. The claim holds, so the exact worst-case probe count is floor(log2 n) + 1, which is also Theta(log n). It matches the direct derivation in Task 3.

### Method 3 - Master Theorem (check)

The recurrence has the form T(n) = a T(n/b) + f(n) with a = 1, b = 2, f(n) = c = Theta(1).

```text
n^(log_b a) = n^(log_2 1) = n^0 = 1
```

f(n) = Theta(1) = Theta(n^(log_b a)), so case 2 applies: T(n) = Theta(n^(log_b a) log n) = Theta(log n). Three independent methods give the same answer.

### Interpretation

Each recursive call halves the range, so the recursion depth is about log2 n: for n = 1,000 the depth is at most 10, for n = 1,000,000 at most 20 (measured: 19-20). The depth is tiny, so the recursion cannot exhaust the call stack (the default Python limit of about 1,000 frames is never approached), and the cost of recursion is only a small constant factor per call. Doubling the database adds exactly one call. Together with the sorting cost n log n from Task 3, the total for binary search is Theta(n log n + q log n).
