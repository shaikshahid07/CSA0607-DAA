# Stage 2 - Comparison of the Two Initial Designs

| Point | Student A | Student B |
|---|---|---|
| Decomposition | Two halves at the middle | Two halves at the middle (same) |
| Base case | Single element | Single element (same) |
| Information returned | 1 value (best) | 4 values (total, prefix, suffix, best) |
| Combine | max(best_L, best_R) | max(best_L, best_R, suffix_L + prefix_R) plus total/prefix/suffix updates |
| Handles a subarray crossing the middle? | No | Yes |
| Combine cost | O(1) | O(1) |

**Where the designs agree:** same divide step and same base case.

**Where they differ:** A returns only one number, so information about the ends of each half is lost; B keeps exactly the information needed to build a crossing subarray.

**Strength / weakness of A:** simple, but incorrect (demo array gives 4 instead of 6; wrong on 1831 of 2000 random tests).

**Strength / weakness of B:** correct and O(1) combine, but needs four values; the all-negative case must be checked.

**Missing cases found in discussion:** crossing subarray, all-negative array, odd length, single element.

**Ideas retained:** the common decomposition from both; B's four-value record. A's idea of "best of the halves" survives as one of the three candidates inside B's `best`.

**Alternative also considered:** the textbook version that keeps only `best` but scans outward from the middle (O(n) per call -> O(n log n) total). It is kept as a baseline in the experiments.
