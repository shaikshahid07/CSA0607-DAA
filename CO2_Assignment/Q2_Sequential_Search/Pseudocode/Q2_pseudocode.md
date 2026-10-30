# Q2 – Sequential Search for Tool Tracking (Pseudocode + Predictions)

Record = (ToolID, TechnicianID, IssueTime, WorkBay). The list is in issue order (unsorted by ToolID).

```
SequentialSearch(L[0..n-1], key)
  comparisons <- 0
  for i <- 0 to n-1
      comparisons++
      if L[i].ToolID = key then return (i, L[i], comparisons)    // successful
  return (NOT_FOUND, comparisons)                                   // unsuccessful: n comparisons
```
Logic: examine records one by one from the front until the Tool ID matches; stop at the first match. Tool IDs are unique among currently issued tools.

## Experiments
1. Successful search at position first, 25%, middle, 75%, last (list sizes n = 100, 1,000, 10,000, 100,000).
2. Unsuccessful search (tool already returned) for the same sizes.
3. Average over 1,000 random successful lookups per size.
4. Timing: measured cost per comparison (ns), used to convert comparisons into latency and CPU load for a request-rate model.
5. Operating boundary: latency budget per request and CPU-share budget for different request rates, for one hangar vs 20 facilities. Reference design measured: hash index keyed by Tool ID.

## Predictions (before execution)
* Successful at position p (1-based) costs exactly p comparisons; first = 1, last = n, middle about n/2.
* Unsuccessful always costs exactly n comparisons (worst case).
* Mean successful cost = (n+1)/2.
* Pure-Python cost per comparison about 50-150 ns, so a full scan of 100,000 records is about 5-15 ms.
* One hangar (hundreds of records, a few requests per minute): sequential search is fine. For 20 facilities the per-request time stays small in isolation, but the total scan work grows with (records x request rate); I expect the boundary to be driven by the request RATE (hundreds of requests per second) rather than the dataset size alone, and I expect an indexed structure to become the better choice well before then.
