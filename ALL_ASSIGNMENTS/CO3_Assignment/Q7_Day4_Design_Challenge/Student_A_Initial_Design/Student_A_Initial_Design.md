# Student A - Independent Initial Design (Stage 1)

> DRAFT written before the joint discussion. Replace or edit this file with your own genuine first idea if it was different. Marks are not deducted for an incorrect initial design.

**Problem:** Maximum subarray sum of an integer array A[0..n-1].

**Decomposition:** Split the array into a left half and a right half at the middle index.

**Base case:** One element -> its value is the answer.

**Subproblem information needed:** Only the best subarray sum inside each half.

**Combine strategy:** Answer = maximum of (best of left half, best of right half).

**Self-check (found later during Stage 2):** This design never considers a subarray that crosses the middle, so it fails on arrays such as [-2, 1, -3, 4, -1, 2, 1, -5, 4] (returns 4, correct is 6).
