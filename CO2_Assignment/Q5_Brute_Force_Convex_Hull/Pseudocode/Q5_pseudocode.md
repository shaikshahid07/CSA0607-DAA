# Q5 – Brute-Force Convex Hull derived from a geometric principle

## Step 1 – from the principle to a formula
1. Two points p1=(x1,y1), p2=(x2,y2) define the line  a x + b y = c  with a = y2 - y1, b = x1 - x2, c = x1*y2 - y1*x2.
2. The position of another point q relative to that line is the sign of  s(q) = a*qx + b*qy - c  (equivalently the cross product (p2-p1) x (q-p1)).
   s > 0: q is on the left of the directed line p1->p2; s < 0: right; s = 0: q on the line.
3. Decision rule: the directed segment p1->p2 is a hull edge iff **every other point has s >= 0** (all on one closed side) and every point with s = 0 lies inside the segment p1p2 (so only the extreme points of a collinear run become vertices).
4. Boundary construction: every accepted directed edge goes in a map  next[p1] = p2.  Starting from the lowest-leftmost point, follow next[] until the start is reached again -> vertices in counter-clockwise order.

## Pseudocode
```
ConvexHull(P)
  P <- remove duplicate points
  if |P| < 3 or all points collinear: return the two extreme points (or the points)
  edges <- empty map ; tests <- 0
  for each unordered pair (i, j), i < j
      seenPos <- false ; seenNeg <- false ; ok <- true
      a,b,c <- line through P[i], P[j]
      for each k != i, j
          tests++
          s <- a*P[k].x + b*P[k].y - c
          if s > 0 then seenPos <- true
          if s < 0 then seenNeg <- true
          if s = 0 and P[k] is outside segment P[i]P[j] then ok <- false ; break
          if seenPos and seenNeg then ok <- false ; break        // early exit
      if ok then
          if not seenNeg then edges[i] <- j        // all on left: directed i -> j
          else                  edges[j] <- i      // all on right: directed j -> i
  start <- lowest then leftmost point ; walk edges from start until returning
```
Integer coordinates are used so the sign test is exact (no floating-point error).
Work: C(n,2) candidate lines x up to (n-2) tests = n(n-1)(n-2)/2 without early exit (Theta(n^3)). The early-exit count is also recorded.

## Test configurations
* T1: 20 points with a mix of boundary and interior points.
* T2 (designed to challenge the algorithm): square corners, extra points lying ON the sides, interior points, and duplicated points.
* T3: all points collinear (degenerate).
* T4: points on a circle (every point on the hull, many near-hull lines).
* Growth: random points, n = 20, 40, 80, 160, 320, 640; tests with early exit vs n(n-1)(n-2)/2.

## Predictions (before execution)
* T1 hull = the visually extreme points; interior points never appear.
* T2 hull = only the 4 corners (collinear mid-side points rejected by the segment rule, duplicates removed).
* T3 returns the 2 extreme points only.
* T4 returns all n points.
* Work without early exit is exactly n(n-1)(n-2)/2 (exponent 3). With early exit most non-hull pairs are rejected after a few points, so random-point work should look closer to n^2 (exponent about 2-2.5).
