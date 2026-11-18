# Q6 – Exhaustive Search for the Airlift Payload Problem

Packages 0..n-1 with weight w[i] and humanitarian value v[i]; payload limit W. Choose a subset with total weight <= W and maximum total value.

## Design
* **Representation:** a candidate solution is an n-bit integer `mask` (0 .. 2^n - 1); bit i = 1 means package i is loaded.
* **Generation:** loop mask from 0 to 2^n - 1; this enumerates every subset exactly once.
* **Feasibility:** total weight = sum of w[i] for set bits; feasible iff <= W.
* **Evaluation:** total value = sum of v[i] for set bits (only for feasible masks).
* **Retention:** keep (bestValue, bestMask); replace only on a strictly higher value (ties keep the earlier mask).

```
Exhaustive(w, v, W, n)
  bestValue <- -1 ; bestMask <- 0 ; candidates <- 0 ; feasible <- 0
  for mask <- 0 to 2^n - 1
      candidates++
      tw <- 0 ; tv <- 0
      for i <- 0 to n-1
          if bit i of mask is 1 then tw <- tw + w[i] ; tv <- tv + v[i]
      if tw <= W then
          feasible++
          if tv > bestValue then bestValue <- tv ; bestMask <- mask
  return bestValue, bestMask
```

## Correctness check
Small instance n = 5 (weights/values chosen by hand, W = 10): all 32 subsets listed in a table with weight, value, feasibility; the optimum found by hand is compared with the program, with `itertools.combinations` and with an independent dynamic-programming check.

## Predictions (before execution)
* Candidates = 2^n: n=10: 1,024; n=14: 16,384; n=18: 262,144; n=20: 1,048,576; n=22: 4,194,304. Each extra package doubles the number of candidates (each old subset exists with and without the new item).
* Total basic operations about n x 2^n, so time should grow by slightly more than 2x per added package (about 2.1-2.2x).
* Pure Python about 2-5 microseconds per candidate at n = 20, so n = 20 about 2-5 s and n = 22 about 10-25 s.
* Deployment limit (response time chosen as 5 seconds): about n = 20 packages.
