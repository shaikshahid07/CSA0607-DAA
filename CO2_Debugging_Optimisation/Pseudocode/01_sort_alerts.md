# Pseudocode 1 - `sort_alerts` (sort alerts by severity, highest first)

Input: `alerts` - list of (alert_id, severity) pairs, indexed from 0.
Output: the alerts ordered by severity, highest first; equal severities keep their arrival order (stable).

## A. Corrected algorithm (insertion sort - original idea, defects D1 and D2 fixed)

```
ALGORITHM SortAlerts_Corrected(alerts)
    n <- length(alerts)
    FOR i <- 1 TO n - 1 DO
        key <- alerts[i]                          // alert to be inserted
        j <- i - 1
        WHILE j >= 0 AND severity(alerts[j]) < severity(key) DO     // FIX D1: j >= 0 (was j > 0)
            alerts[j + 1] <- alerts[j]            // shift the lower-severity alert one place right
            j <- j - 1
        END WHILE
        alerts[j + 1] <- key                      // FIX D2: slot j + 1 (was slot j)
    END FOR
    RETURN alerts
END ALGORITHM
```

The comparison is strict (`<`), so an alert is never moved past one with EQUAL severity - this is what makes the sort stable.

| Case | Comparisons | Time |
|---|---|---|
| Best (already ordered) | n - 1 | O(n) |
| Average (random) | about n^2 / 4 | O(n^2) |
| Worst (reverse order) | n(n-1)/2 | O(n^2) |
| Space | one extra variable | O(1) |

## B. Optimised algorithm (hybrid merge/insertion sort = Timsort, via `sorted`)

```
ALGORITHM SortAlerts_Optimised(alerts)
    RETURN SORTED(alerts, KEY = severity, ORDER = descending, STABLE)
END ALGORITHM
```

How the built-in sort works (Timsort), in outline:

```
    split the list into natural runs (already ordered stretches; descending runs are reversed)
    extend short runs to a minimum length using binary insertion sort
    merge neighbouring runs, always keeping the merge stable
```

`reverse = TRUE` keeps equal-severity alerts in their original order, so the output is identical to the corrected insertion sort.

| Case | Comparisons | Time |
|---|---|---|
| Best (one long run) | n - 1 | O(n) |
| Average / worst | at most about n log2 n | O(n log n) |
| Space | temporary merge buffer | O(n) |

Why: for 50,000 alerts the corrected insertion sort needs about 562 million comparisons on random data; the optimised sort needs about 356 thousand.
