# Stage 3 - Joint Final Design

**Decomposition:** split A[low..high] at mid = (low + high) / 2.

**Subproblems:** the left half A[low..mid] and the right half A[mid+1..high] - same problem, half the size.

**Base case:** one element x -> (total, prefix, suffix, best) = (x, x, x, x).

**Information returned:** the record (total, prefix, suffix, best).

**Combine operation (O(1)):**
* total  = L.total + R.total
* prefix = max(L.prefix, L.total + R.prefix)
* suffix = max(R.suffix, R.total + L.suffix)
* best   = max(L.best, R.best, L.suffix + R.prefix)

**Complete pseudocode:** see `../Pseudocode/Q7_pseudocode.md`. **Code:** `../Implementation_Code/q7_max_subarray.py`.

**Stage 4 - Mathematical validation (Student A):** T(n) = 2T(n/2) + c, T(1) = d.
Recursion tree: level i has 2^i nodes each costing c, there are log2 n levels, so the total is c(1 + 2 + ... + n/2) + d*n = c(n - 1) + d*n = Theta(n). Master theorem: a = 2, b = 2, f(n) = Theta(1) = O(n^(1-e)) -> Case 1 -> Theta(n^(log2 2)) = Theta(n).

**Stage 4 - Experimental validation (Student B):** test cases, random tests and operation counts are in `../Output_Screenshots/Q7_output.txt`; the joint design performs exactly 5(n-1) counted operations and the doubling ratio is 2.000.

**Stage 5 - Cross-defence:** see Section 8.5 of the report.
