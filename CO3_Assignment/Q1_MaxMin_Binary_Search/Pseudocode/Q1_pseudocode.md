# Q1 Pseudocode - Max/Min and Binary Search (Divide and Conquer)

## Part A - Finding Maximum and Minimum

**Divide-and-Conquer idea:** split the list into two halves, find (max, min) of each half, then combine with two comparisons.

```
MAXMIN(A, low, high)
    if low == high                          // one element
        return (A[low], A[low])             // 0 comparisons
    if high == low + 1                      // two elements
        if A[low] > A[high]  return (A[low], A[high])
        else                 return (A[high], A[low])      // 1 comparison
    mid = (low + high) / 2
    (max1, min1) = MAXMIN(A, low, mid)              // DIVIDE
    (max2, min2) = MAXMIN(A, mid + 1, high)         // CONQUER
    max = larger of max1, max2                      // COMBINE: 1 comparison
    min = smaller of min1, min2                     // COMBINE: 1 comparison
    return (max, min)
```

* Base cases: size 1 (0 comparisons) and size 2 (1 comparison).
* Each subproblem returns a **pair** (max, min).
* Recurrence: T(n) = 2T(n/2) + 2, T(2) = 1  ->  T(n) = 3n/2 - 2 (n = power of 2).
* Independent scan needs 2(n - 1) comparisons.

## Part B - Binary Search

```
BINARYSEARCH(A, n, target)          // A is sorted ascending
    low = 0, high = n - 1
    while low <= high
        mid = (low + high) / 2
        if A[mid] == target   return mid          // found
        if A[mid] < target    low  = mid + 1      // throw away left half and mid
        else                  high = mid - 1      // throw away right half and mid
    return -1                                     // search space empty
```

* Each pass throws away at least half of the remaining search space.
* Recurrence: T(n) = T(n/2) + 1  ->  T(n) = floor(log2 n) + 1 comparisons.
