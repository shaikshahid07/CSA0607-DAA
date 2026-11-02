# Q5 Pseudocode - Closest Pair of Points

## Brute force (from CO2)

```
BRUTE(P)
    best = infinity
    for i = 0 .. n-2
        for j = i+1 .. n-1
            if dist(P[i], P[j]) < best  best = dist(P[i], P[j])
    return best                          // n(n-1)/2 distance computations
```

## Divide and Conquer

```
CLOSEST(P)
    Px = P sorted by x                                // done once
    return REC(Px)

REC(Px)           // returns (best distance, list sorted by y)
    if |Px| <= 3
        best = BRUTE(Px)
        return (best, Px sorted by y)
    mid = |Px| / 2
    midx = Px[mid].x                                  // dividing line
    (dL, Py_left)  = REC(Px[0 .. mid-1])              // DIVIDE
    (dR, Py_right) = REC(Px[mid .. end])              // CONQUER
    Py = MERGE_BY_Y(Py_left, Py_right)
    d  = min(dL, dR)
    strip = all points p in Py with |p.x - midx| < d  // COMBINE: boundary strip
    for i = 0 .. |strip|-1
        j = i + 1
        while j < |strip| and (strip[j].y - strip[i].y) < d
            d = min(d, dist(strip[i], strip[j]))
            j = j + 1
    return (d, Py)
```

* Why the strip is special: the closest pair may have one point on each side of the line, and neither recursive call can see it.
* Why the strip needs few comparisons: points in the strip are sorted by y, and inside a d x 2d rectangle at most 8 points can exist when every side has minimum spacing d, so each point is compared with at most 7 following points.
* Recurrence: T(n) = 2T(n/2) + O(n) -> Theta(n log n).
