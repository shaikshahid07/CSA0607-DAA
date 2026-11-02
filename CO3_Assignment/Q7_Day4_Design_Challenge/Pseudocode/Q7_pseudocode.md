# Q7 Pseudocode - Maximum Subarray Sum (Joint Final Design)

Problem used for the Day-4 challenge: given an array A of n integers (positive and negative), find the largest sum of a contiguous, non-empty subarray.

```
SOLVE(A, low, high)       // returns a record (total, prefix, suffix, best)
    if low == high
        return (A[low], A[low], A[low], A[low])               // base case
    mid = (low + high) / 2
    L = SOLVE(A, low, mid)                                    // DIVIDE
    R = SOLVE(A, mid + 1, high)                               // CONQUER
    total  = L.total + R.total                                // COMBINE
    prefix = max(L.prefix, L.total + R.prefix)
    suffix = max(R.suffix, R.total + L.suffix)
    best   = max(L.best, R.best, L.suffix + R.prefix)
    return (total, prefix, suffix, best)

MAXSUBARRAY(A)
    return SOLVE(A, 0, n - 1).best
```

Meaning of each returned value for a segment:

* total  = sum of the whole segment
* prefix = best sum of a subarray that starts at the left end of the segment
* suffix = best sum of a subarray that ends at the right end of the segment
* best   = best sum of any subarray inside the segment

Recurrence: T(n) = 2T(n/2) + Theta(1) -> Theta(n).

## Baselines used in the experiments

```
BRUTE(A)      for every i, for every j >= i, keep a running sum and track the maximum        // Theta(n^2)
SCAN-DC(A)    best of left half, right half and CROSSING(A, low, mid, high)                  // Theta(n log n)
CROSSING      best sum going left from mid  +  best sum going right from mid+1               // Theta(n)
```
