# Task 12 - Day-4 Design Challenge: Re-evaluate and Adapt the Design (8 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

Changed requirement: 50,000 search requests per hour (about 13.9 per second, 1,200,000 per day) on 1,000,000 records, with new records added only once per day. Decision: REDESIGN - keep the sorted array only as a secondary structure and use a hash table as the primary lookup index, rebuilt once per day. Measured values are those of Task 9.

### A. Impact Analysis (2 marks)

- What changed: the problem was previously one-off lookups on a growing database with no stated rate; it is now a sustained, known load of 1.2 million lookups per day on a database that changes only once per day.
- Assumptions affected: (1) 'the cost of one search matters' becomes 'the total cost of 1.2 million searches matters'; (2) 'preprocessing is an overhead to be avoided' becomes 'preprocessing is paid once per day and shared by 1.2 million searches'; (3) 'the data keeps changing, so keep it easy to update' is replaced by 'the data is static for 24 hours'.
- Why search frequency matters: a per-search cost is multiplied by 50,000 every hour. A cost that is negligible once becomes large: at 20.6 ms per search, linear search would occupy a processor for 1,028 s of every 3,600 s (29% of a core), with no headroom for bursts.
- Why rare updates matter: because the data is static between updates, any preprocessing (sorting or building a table) is done once and amortised over the day: 0.32 s of sorting or 0.97 s of hash building is spread over 1,200,000 searches, i.e. 0.27 and 0.81 microseconds per search. The usual weakness of hash tables and sorted arrays, expensive updates, no longer matters.

### B. Evaluation of the Original Design (2 marks)

**Table 12.1  Daily workload on 1,000,000 records (measured per-search times x 1.2 million searches)**

| Measure at n = 10^6, 50,000 searches/hour | Linear | Binary + sort (original) | Hash table |
|---|---|---|---|
| Time per search | 20.6 ms | 2.82 us | 0.12 us |
| CPU time per hour of traffic | 1,028 s (29% of a core) | 0.14 s (0.0039%) | 0.006 s (0.00016%) |
| Daily preprocessing | none | 0.32 s | 0.97 s |
| Total CPU time per day | 24,666 s | 3.71 s | 1.11 s |
| Comparisons per day (theory) | about 6 x 10^11 | about 4.3 x 10^7 | about 4.1 x 10^6 |

Expected behaviour of the original design: binary search easily sustains the load. It uses 0.14 s of processor time per hour, so it is not a bottleneck, and its preprocessing cost is acceptable because the 0.32 s sort is done once a day. The original design is therefore adequate in the sense of meeting the requirement, but another approach does better overall: the hash table needs 1.11 s per day against 3.71 s, about 3.3 times less, and its theoretical operation count is roughly 10 times lower. Linear search is clearly unsuitable (it would consume 6.9 hours of CPU time per day).

The measured cross-over also needs to be stated honestly. Because the hash build is more expensive here than the sort, sort-plus-binary search is cheaper while fewer than about 239,329 searches are served per build (Figure 9.5). At 50,000 searches per hour that point is reached after about 4.8 hours, so over a whole day (1.2 million searches) the hash table is the cheaper design.

### C. Adaptation or Redesign (2 marks)

Decision: redesign around a hash index.

- Revised strategy: once per day, after the new records are loaded, build a hash table (h(K) = K mod m, m prime near 1.5n, separate chaining) over all 1,000,000+ registration numbers. All 50,000 hourly searches use this table. The sorted array may be kept as a secondary structure (rebuilt by merging the day's sorted new records into the old sorted array in Theta(n + b) instead of re-sorting) for ordered or range queries and as a fallback.
- What changed: the primary search moves from comparison-based halving (Theta(log n)) to address calculation (Theta(1) expected); preprocessing moves from Theta(n log n) to Theta(n); about 50% more memory is used.
- Effect on complexity: per-search cost falls from Theta(log n) (about 19 comparisons) to Theta(1) expected (about 1.1-1.3 comparisons). Daily cost falls from Theta(n log n + 1.2 x 10^6 log n) to Theta(n + 1.2 x 10^6). Worst case becomes Theta(n) only if the hash function is defeated; prime table size and the measured maximum chain of 4-7 make this negligible.
- Retained from the original design: the sorted array and binary search remain the correct choice if the search rate were low or the data changed continuously.

### D. Evidence-Based Defence (2 marks)

- Mathematical analysis: Theta(n + q) for hashing against Theta(n log n + q log n) for the original design. With n = 10^6 and q = 1.2 x 10^6, that is about 4.1 x 10^6 against about 4.3 x 10^7 basic operations.
- Experiment: 0.12 us per lookup against 2.82 us (24 times faster); about 1.1-1.4 comparisons against 19.4 on average; daily CPU time 1.11 s against 3.71 s.
- Search frequency: 50,000 per hour is high enough to amortise the 0.97 s build (break-even about 4.8 hours of traffic); it also leaves massive headroom for bursts and growth: even at 100 times the load (5 million requests per hour) the hash table would use under one second of CPU time per hour.
- Preprocessing: 0.97 s once per day is trivial next to 86,400 s, and fits naturally in the nightly update window since records are added only once a day.
- Trade-offs and honesty: the hash table costs about 50% more memory, is not ordered, and has a theoretical Theta(n) worst case. The experiment also shows that binary search would be sufficient for this workload (0.14 s of CPU per hour); the redesign is justified by lower total cost per day, headroom and constant-time scaling as the database grows, not because the original design fails. If ordered queries were required, the retained sorted array would serve them.
