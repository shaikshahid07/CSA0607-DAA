# Task 6 - Formulate the Recurrence Relation (3 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

The recursive algorithm in this assignment is the recursive binary search (Task 1, Approach B). The recurrence is derived from its code, not quoted from a textbook.

```text
ALGORITHM BinarySearch(A[low..high], K)       // A sorted ascending
    if low > high then return -1                // base case: empty range
    mid <- floor((low + high) / 2)
    if A[mid] = K then return mid               // basic operation (one probe)
    else if K < A[mid] then
        return BinarySearch(A, K, low, mid - 1)  // left half
    else
        return BinarySearch(A, K, mid + 1, high) // right half
```

**Table 6.1  Components of the recurrence**

| Component | Identification from the algorithm |
|---|---|
| Input size of the original problem | n = high - low + 1, the number of records still in the range being searched (initially the whole database) |
| Size of the recursive subproblem | mid = floor((low + high)/2). The left range low..mid-1 has floor((n-1)/2) elements; the right range mid+1..high has floor(n/2) elements. The larger of the two, floor(n/2), is used for the worst case. |
| Number of recursive calls | Exactly one (either left or right, never both), so a = 1 |
| Work outside the recursive call | Compute mid, one comparison A[mid] = K, one comparison K < A[mid]: a constant amount c, so f(n) = Theta(1). Counted as C(n): one probe = 1. |
| Base case | low > high, i.e. n = 0: the range is empty, the key is absent, and the call returns -1 without any probe. T(0) = c0 (C(0) = 0). |

How the components combine. A call on a range of n >= 1 elements does constant work (probe at mid) and, if the key was not at mid, makes a single call on a range of at most floor(n/2) elements. Therefore:

```text
T(n) = T(floor(n/2)) + c        for n >= 1
```

```text
T(0) = c0                         (base case)
```

In terms of the basic operation (key probes), the same structure gives:

```text
C(n) = C(floor(n/2)) + 1       for n >= 1,        C(0) = 0
```

For analysis with the Master Theorem the usual simplification T(n) = T(n/2) + Theta(1) is used (a = 1, b = 2, f(n) = Theta(1)). Note the contrast with a recurrence such as T(n) = 2T(n/2) + n: only one half is solved, which is the property that makes the algorithm logarithmic.
