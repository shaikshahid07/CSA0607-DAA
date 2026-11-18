# Q4 – Brute-Force Closest Pair (Pseudocode, derivation, predictions)

```
ClosestPair(D[0..n-1])        // D[i] = (x_i, y_i)
  best <- infinity ; pairsExamined <- 0 ; distCalcs <- 0
  for i <- 0 to n-2
      for j <- i+1 to n-1                  // j > i : each unordered pair once
          pairsExamined++
          d2 <- (xi-xj)^2 + (yi-yj)^2      // squared distance, no sqrt needed to compare
          distCalcs++
          if d2 < best then best <- d2 ; (a,b) <- (i,j)
  return D[a], D[b], sqrt(best)
```
* Candidate pairs = all unordered pairs of distinct drones.
* Duplicates avoided by fixing j > i (pair (i,j) and (j,i) are the same pair; i = j is meaningless).
* Count: outer loop i has (n-1-i) partners, so  sum_{i=0}^{n-2}(n-1-i) = (n-1)+(n-2)+...+1 = n(n-1)/2 = C(n,2).
  Check: choose 2 of n drones = n!/(2!(n-2)!) = n(n-1)/2. Growth is Theta(n^2).

## Experiment
n = 100, 500, 1000, 2000, 4000, 8000 random drones in a 10,000 x 10,000 grid (fixed seed). Record pairs examined, distance calculations, time (median of repeats); compare with n(n-1)/2 and fit time = c x pairs.
Acceptability criterion (my choice): **one position report must be processed within 1 second** (drones report about once per second; a slower check cannot keep up).

## Predictions (before execution)
* Pairs examined = distance calculations = n(n-1)/2 exactly: 4,950; 124,750; 499,500; 1,999,000; 7,998,000; 31,996,000.
* Doubling n multiplies the time by about 4.
* Pure Python about 0.2-0.5 microseconds per pair, so n = 2,000 about 0.4-1 s: boundary of practicality expected around n = 2,000-3,500.
* The inefficiency comes from comparing pairs that are obviously far apart; a redesign must avoid looking at far-apart pairs (e.g. by spatial ordering/partitioning), not just compute a distance faster.
