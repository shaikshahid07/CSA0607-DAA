# Pseudocode 3 - `find_signature` (all start positions of a signature in a log line)

Input: `log` (length n) and `pattern` (length m), strings indexed from 0.
Output: list of every start position i where log[i .. i+m-1] equals pattern (overlapping matches included).

## A. Corrected algorithm (brute force - defects D5 and D6 fixed)

```
ALGORITHM FindSignature_Corrected(log, pattern)
    n <- length(log);  m <- length(pattern)
    hits <- empty list
    IF m = 0 THEN RETURN hits                     // empty signature matches nothing
    FOR i <- 0 TO n - m DO                        // FIX D5: n - m INCLUSIVE, i.e. n - m + 1 alignments (was n - m - 1)
        j <- 0
        WHILE j < m AND log[i + j] = pattern[j] DO
            j <- j + 1
        END WHILE
        IF j = m THEN                             // FIX D6: all m characters matched (was "j = m - 1" after a break)
            APPEND i TO hits
        END IF
    END FOR
    RETURN hits
END ALGORITHM
```

| Case | Character comparisons | Time |
|---|---|---|
| Best (first character differs every time) | n - m + 1 | O(n) |
| Worst (e.g. log = AAAA...A, pattern = AA...AB) | m (n - m + 1) | O(n m) |
| Space | hits list only | O(1) extra |

## B. Optimised algorithms

### B1. Brute force with no redundant work
The corrected algorithm already (i) tries only the n - m + 1 alignments that fit, (ii) leaves a window at its FIRST mismatching character, and (iii) performs no extra test after the inner loop. This is the baseline for the comparison. Same complexity as A.

### B2. Horspool (skip table)

```
ALGORITHM FindSignature_Horspool(log, pattern)
    n <- length(log);  m <- length(pattern)
    hits <- empty list
    IF m = 0 OR m > n THEN RETURN hits
    // shift table: distance from the LAST occurrence of each character (excluding the final one) to the pattern end
    FOR EACH character c DO shift[c] <- m                       // default: skip the whole pattern
    FOR k <- 0 TO m - 2 DO shift[pattern[k]] <- m - 1 - k
    i <- 0
    WHILE i <= n - m DO
        k <- m - 1
        WHILE k >= 0 AND log[i + k] = pattern[k] DO            // compare right to left
            k <- k - 1
        END WHILE
        IF k < 0 THEN APPEND i TO hits
        i <- i + shift[ log[i + m - 1] ]                        // skip using the window's LAST character
    END WHILE
    RETURN hits
END ALGORITHM
```

| Case | Time |
|---|---|
| Preprocessing (shift table) | O(m + alphabet size) |
| Average | about O(n / m) comparisons for a large alphabet |
| Worst | O(n m) |

### B3. Built-in search in a loop (C implementation)

```
ALGORITHM FindSignature_Builtin(log, pattern)
    hits <- empty list
    IF pattern is empty OR m > n THEN RETURN hits
    i <- FIND(log, pattern, from 0)               // library routine, returns -1 if none
    WHILE i <> -1 DO
        APPEND i TO hits
        i <- FIND(log, pattern, from i + 1)       // i + 1 so overlapping matches are not skipped
    END WHILE
    RETURN hits
END ALGORITHM
```

All three optimised versions return exactly the same list as A (checked by `test_harness.py`).
