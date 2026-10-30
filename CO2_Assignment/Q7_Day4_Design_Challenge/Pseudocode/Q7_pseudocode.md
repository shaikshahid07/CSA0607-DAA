# Q7 – Day-4 Design Challenge: Diagnose, Redesign, Validate (selected solution: Q6 exhaustive search)

## A. Diagnosis targets (to be confirmed by measurement)
1. Effort is spent enumerating 2^n subsets and, for each, re-adding up to n weights/values: about n x 2^n additions.
2. Repeated work: subsets sharing a prefix of packages recompute the same partial sums; once a prefix is overweight, every superset is enumerated and rejected anyway.
3. Candidates that cannot beat the best solution already found are still fully evaluated.
4. Root cause: the algorithm treats every subset as independent and has no way to say "this whole family of subsets is hopeless".

## B. Design objective
* O1: examine far fewer than 2^n candidates (target: at least 90% fewer nodes than 2^n at n = 20 on random instances).
* O2: O(1) incremental work per search node instead of O(n) per candidate.
* O3: still return a provably optimal value (identical to the exhaustive result on every tested instance).

## C. Redesign: "grow the subset package by package and cut off hopeless branches"
Changes:
1. **Search tree instead of flat enumeration:** decide package 0, then 1, ... (include / exclude). A node = a partial decision. Running weight and value are carried down (reuse of previously computed information, O(1) per node).
2. **Feasibility cut-off (V1):** if running weight > W, no extension can be feasible (weights are positive), so the whole subtree (up to 2^(n-k) subsets) is skipped.
3. **Optimistic bound cut-off (V2):** pre-sort packages by value/weight ratio (preprocessing, O(n log n)). At a node, estimate the best possible value reachable by filling the remaining capacity with remaining packages in ratio order, allowing the last one to be taken fractionally. This is a relaxation, so it can never be lower than the true best of the subtree. If floor(bound) <= best value found so far, the subtree cannot improve the answer and is skipped.
4. Extra memory: O(n) recursion depth and the sorted index array. Trade-off: each node now costs more (bound computation O(n)), the benefit depends on the instance (weak pruning when value is nearly proportional to weight), and the order of exploration matters (include-first, best-ratio-first finds a good solution early).

```
Explore(k, weight, value)                      // k = next package in ratio order
  nodes++
  if value > best then best <- value
  if k = n then return
  // V2 only: optimistic bound
  if floor(Bound(k, W - weight, value)) <= best then pruned++ ; return
  if weight + w[k] <= W then Explore(k+1, weight + w[k], value + v[k])   // include
  Explore(k+1, weight, value)                                            // exclude

Bound(k, room, value)
  for t <- k to n-1
      if w[t] <= room then room <- room - w[t] ; value <- value + v[t]
      else return value + v[t] * room / w[t]         // fractional piece, then stop
  return value
```
V1 = Explore without the Bound test (items in original order). V2 = Explore with ratio ordering and bound.

## D. Predictions (before implementation)
* Optimal values identical to Q6 on all instances.
* Nodes visited: V1 clearly below 2^n (feasibility cut only helps when the capacity is binding), V2 several orders of magnitude below 2^n at n = 20 on random instances (>= 95% fewer).
* The count of nodes for V2 should grow much more slowly with n than 2^n on random instances.
* Time improvement will be smaller than node-count improvement because each V2 node costs more; for very small n (<= 10) V2 may be no faster than plain exhaustive search because of sorting/bound overhead.
* On adversarial "strongly correlated" instances (value = weight + constant) pruning will be much weaker; V2 may still visit a large share of the tree.
* Performance measure expected to improve: nodes visited/candidates examined first, then execution time.

## E. Validation plan
Same instances (same seeds) for n = 10, 14, 18, 20, 22: Exhaustive vs V1 vs V2 -> candidates/nodes, time, optimum agreement. Then V2 alone for n = 30, 40, 50, 60 (random and strongly-correlated families), with a node cap for hard cases.
