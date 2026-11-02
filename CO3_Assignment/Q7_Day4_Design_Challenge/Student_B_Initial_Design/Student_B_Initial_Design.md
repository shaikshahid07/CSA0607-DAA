# Student B - Independent Initial Design (Stage 1)

> DRAFT written before the joint discussion. Replace or edit this file with your own genuine first idea if it was different. Marks are not deducted for an incorrect initial design.

**Problem:** Maximum subarray sum of an integer array A[0..n-1].

**Decomposition:** Split the array into a left half and a right half at the middle index.

**Base case:** One element -> the segment's total, best prefix, best suffix and best subarray are all that element.

**Subproblem information needed:** For each half: total sum, best prefix sum, best suffix sum, best subarray sum.

**Combine strategy:**
* total  = total_L + total_R
* prefix = max(prefix_L, total_L + prefix_R)
* suffix = max(suffix_R, total_R + suffix_L)
* best   = max(best_L, best_R, suffix_L + prefix_R)

**Possible weakness:** four values per call make the code longer, and the design was not yet checked against an all-negative array.
