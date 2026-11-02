# Q2 Pseudocode - Merge Sort and Quick Sort

## Merge Sort

```
MERGESORT(A)
    if length(A) <= 1  return A                      // base case
    mid = length(A) / 2
    L = MERGESORT(A[0 .. mid-1])                     // DIVIDE (always equal halves)
    R = MERGESORT(A[mid .. end])
    return MERGE(L, R)                               // COMBINE: linear work

MERGE(L, R)
    i = 0, j = 0, result = empty
    while i < |L| and j < |R|
        if L[i] <= R[j]  append L[i], i = i + 1
        else             append R[j], j = j + 1
    append the rest of L, then the rest of R
    return result
```

Recurrence: T(n) = 2T(n/2) + n -> Theta(n log n) for **every** input. Depth = ceil(log2 n) + 1.

## Quick Sort - pivot strategy: FIRST element

```
QUICKSORT(A)
    if length(A) <= 1  return A
    pivot = A[0]
    left  = all x in A[1..] with x <  pivot           // DIVIDE (n-1 comparisons)
    right = all x in A[1..] with x >= pivot
    return QUICKSORT(left) + [pivot] + QUICKSORT(right)   // COMBINE: just join
```

* Balanced input: pivot is the median at every level -> split n/2 : n/2 -> T(n) = 2T(n/2) + n.
* Unbalanced input (already sorted): left is empty at every level -> T(n) = T(n-1) + n -> O(n^2).

## Building the experiment inputs

```
BUILDBALANCED(sorted S)             // first element of the list becomes the median
    if |S| <= 1  return S
    m = |S| / 2
    return [S[m]] + BUILDBALANCED(S[0..m-1]) + BUILDBALANCED(S[m+1..])
```

Sorted and reverse-sorted arrays give the severely unbalanced case (1 : n-1) for the first-element pivot.
