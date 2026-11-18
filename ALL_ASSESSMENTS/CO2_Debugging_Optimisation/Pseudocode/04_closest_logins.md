# Pseudocode 4 - `closest_logins` (closest pair of login locations)

Input: `events` - list of n points (x, y), indexed from 0.
Output: ((i, j), d) - the indices (i < j) of the two closest points and their distance d; (NONE, NONE) if n < 2.
Ties: the pair with the smallest (i, j) wins.

## A. Corrected algorithm (brute force - defects D7, D8 and D9 fixed)

```
ALGORITHM ClosestLogins_Corrected(events)
    n <- length(events)
    IF n < 2 THEN RETURN (NONE, NONE)
    minDist <- INFINITY                           // FIX D7: was 0
    pair <- NONE
    FOR i <- 0 TO n - 1 DO
        FOR j <- i + 1 TO n - 1 DO                // FIX D9: only pairs with i < j (was j from 0)
            d <- SQRT( (x[i] - x[j])^2 + (y[i] - y[j])^2 )
            IF d < minDist THEN                   // FIX D8: smaller is better (was d > minDist)
                minDist <- d;  pair <- (i, j)
            END IF
        END FOR
    END FOR
    RETURN (pair, minDist)
END ALGORITHM
```

Distance computations: n(n-1)/2 -> O(n^2).  The original performed n x n.

## B. Optimised algorithm 1 - pruned brute force

```
ALGORITHM ClosestLogins_Optimised(events)
    n <- length(events)
    IF n < 2 THEN RETURN (NONE, NONE)
    axis <- the coordinate (x or y) with the LARGER spread (max - min)
    order <- indices 0..n-1 sorted by coordinate axis             // O(n log n)
    best <- INFINITY                              // best SQUARED distance
    bestPair <- NONE
    FOR a <- 0 TO n - 1 DO
        FOR b <- a + 1 TO n - 1 DO
            gap <- axis-coordinate(order[b]) - axis-coordinate(order[a])
            IF gap^2 > best THEN BREAK            // every later point is even farther along the axis
            d2 <- (x[order[a]] - x[order[b]])^2 + (y[order[a]] - y[order[b]])^2     // no square root
            cand <- (MIN(order[a], order[b]), MAX(order[a], order[b]))
            IF d2 < best OR (d2 = best AND cand < bestPair) THEN
                best <- d2;  bestPair <- cand
            END IF
        END FOR
    END FOR
    RETURN (bestPair, SQRT(best))                 // ONE square root in total
END ALGORITHM
```

Time: O(n log n) for the sort plus the scan; the scan is close to O(n) for spread-out points and O(n^2) in the worst case (all points inside a very thin band). Space O(n).

## C. Optimised algorithm 2 - divide and conquer (for comparison)

```
ALGORITHM ClosestLogins_DC(events)
    px <- points sorted by x;  py <- the same points sorted by y         // done ONCE
    RETURN Solve(px, py)

FUNCTION Solve(px, py)
    IF |px| <= 3 THEN RETURN brute force on px
    mid <- |px| DIV 2;  midX <- x of px[mid]
    (pxL, pyL) <- left half  (points px[0..mid-1], kept in y order)
    (pxR, pyR) <- right half (points px[mid..],    kept in y order)
    best <- BETTER( Solve(pxL, pyL), Solve(pxR, pyR) )                   // smaller distance, ties -> smaller pair
    strip <- points of py whose (x - midX)^2 <= best                     // in y order
    FOR EACH point p IN strip DO
        FOR EACH later point q IN strip DO
            IF (y[q] - y[p])^2 > best THEN BREAK                         // at most a few q per p
            best <- BETTER(best, distance(p, q))
        END FOR
    END FOR
    RETURN best
END FUNCTION
```

Recurrence T(n) = 2 T(n/2) + O(n)  ->  T(n) = O(n log n).  Space O(n).
