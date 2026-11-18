# Pseudocode 2 - `is_blocked` (is an IP address on the blocklist?)

Input: `blocklist` - list of IP-address strings; `ip` - the address to check.
Output: TRUE if `ip` is on the blocklist, otherwise FALSE.

## A. Corrected algorithm (sequential search - defects D3 and D4 fixed)

```
ALGORITHM IsBlocked_Corrected(blocklist, ip)
    n <- length(blocklist)
    FOR i <- 0 TO n - 1 DO
        IF blocklist[i] = ip THEN
            RETURN TRUE                           // FIX D3: a match means BLOCKED (was FALSE)
        END IF
        // FIX D4: no "else RETURN FALSE" here - one non-matching entry proves nothing
    END FOR
    RETURN FALSE                                  // FIX D4: decided only after EVERY entry was checked
END ALGORITHM                                     //         (also correct for an empty blocklist)
```

| Case | Comparisons | Time |
|---|---|---|
| Best (first entry matches) | 1 | O(1) |
| Worst (last entry, or not present) | n | O(n) |
| Space | none extra | O(1) |

## B. Optimised algorithm (hash-set index built once)

```
ALGORITHM BuildBlocklist(blocklist)               // run ONCE, e.g. when the blocklist is loaded
    index <- empty hash set
    FOR EACH address IN blocklist DO
        INSERT address INTO index
    END FOR
    RETURN index
END ALGORITHM

ALGORITHM IsBlocked_Optimised(index, ip)          // run for EVERY query
    RETURN (ip IS A MEMBER OF index)              // hash ip, look in one bucket
END ALGORITHM
```

| Step | Time | Space |
|---|---|---|
| Build index | O(n) once | O(n) |
| One lookup (average) | O(1) | O(1) |
| One lookup (worst case, all hash collisions) | O(n) - extremely unlikely | O(1) |

Why: with q queries the sequential search costs O(q x n); the index costs O(n + q). For 1,000 queries against 100,000 addresses: about 75 million comparisons versus 1,000 lookups.
