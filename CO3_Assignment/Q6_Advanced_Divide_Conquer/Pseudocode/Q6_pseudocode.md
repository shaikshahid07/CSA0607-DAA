# Q6 Pseudocode - Median of Medians and Meet-in-the-Middle

## A. Median of Medians (k-th smallest)

```
SELECT(A, k)
    if |A| <= 5  return k-th smallest of A (sort)
    split A into groups of 5
    medians = median of each group                    // insertion sort inside each group
    pivot = SELECT(medians, ceil(|medians| / 2))      // median of the medians (recursion)
    low   = elements < pivot
    equal = elements == pivot
    high  = elements > pivot
    if k <= |low|                  return SELECT(low, k)
    if k <= |low| + |equal|        return pivot
    return SELECT(high, k - |low| - |equal|)
```

Guarantee: at least 3n/10 elements are <= pivot and at least 3n/10 are >= pivot, so the next call has at most 7n/10 elements.
Recurrence: T(n) = T(n/5) + T(7n/10) + O(n) -> Theta(n) because 1/5 + 7/10 < 1.

## QuickSelect (comparison)

```
QUICKSELECT(A, k, pivot rule)       // rule = first element / last element / random element
    repeat
        choose pivot by the rule
        split into low, equal, high
        keep only the part that contains the k-th element
```
Expected O(n) with a random pivot, O(n^2) worst case.

## B. Meet-in-the-Middle Subset Sum

```
SUBSETSUMS(list)
    sums = [0]
    for x in list  sums = sums + [s + x for s in sums]
    return sums                                       // 2^|list| values

MITM(nums, target)
    half = n / 2
    L = SUBSETSUMS(nums[0 .. half-1])                 // 2^(n/2) sums
    R = SUBSETSUMS(nums[half .. n-1])                 // 2^(n/2) sums
    sort L ascending, sort R ascending
    i = 0, j = |R| - 1
    while i < |L| and j >= 0
        total = L[i] + R[j]
        if total == target  return TRUE
        if total < target   i = i + 1
        else                j = j - 1
    return FALSE
```

Time O(2^(n/2) * n), memory O(2^(n/2)), compared with O(2^n) time for plain enumeration.
