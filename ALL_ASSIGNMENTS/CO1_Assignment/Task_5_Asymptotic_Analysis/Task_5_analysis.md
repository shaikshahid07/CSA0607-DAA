# Task 5 - Perform Asymptotic Analysis (3 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

Definitions used: f(n) = O(g(n)) if f(n) <= c g(n) for all n >= n0; f(n) = Omega(g(n)) if f(n) >= c g(n) for all n >= n0; f(n) = Theta(g(n)) if both hold.

**Table 5.1  Asymptotic summary**

| Algorithm | Best case | Average case | Worst case | Preprocessing | Overall (q searches) |
|---|---|---|---|---|---|
| Linear | Theta(1) | Theta(n) | Theta(n) | none | Theta(q n) |
| Binary search | Theta(1) | Theta(log n) | Theta(log n) | Theta(n log n) | Theta(n log n + q log n) |
| Hash table | Theta(1) | Theta(1) expected | O(n); practically O(1) | Theta(n) | Theta(n + q) expected |

Justification of the main bounds. Linear search: C_avg = (n+1)/2 satisfies n/2 <= (n+1)/2 <= n for n >= 1, so C_avg = Theta(n) with c1 = 1/2, c2 = 1, n0 = 1. Since the worst case is exactly n, the algorithm is O(n) overall and Omega(1) in the best case; it is therefore not Theta of a single function over all inputs, but Theta(n) for the average and worst case. Binary search: C_worst = floor(log2 n) + 1, and log2 n <= floor(log2 n) + 1 <= 2 log2 n for n >= 2, so it is Theta(log n). Hash lookup: the expected cost 1 + alpha/2 with alpha fixed at about 0.67 is bounded above and below by constants, so it is Theta(1) in expectation.

Order of growth. log n = O(n) but n is not O(log n), because lim_{n->infinity} (log2 n)/n = 0 (L'Hopital: (1/(n ln 2)) / 1 -> 0). So the chain of growth rates is: 1 << log n << n << n log n.

**Table 5.2  Predicted growth for the four database sizes**

| Records n | Linear (avg comparisons) | Binary (worst probes) | Hash (expected) | Sorting cost n log2 n |
|---|---|---|---|---|
| 1,000 | 500 | 10 | about 1.3 | 9,966 |
| 10,000 | 5,000 | 14 | about 1.3 | 132,877 |
| 100,000 | 50,000 | 17 | about 1.3 | 1,660,964 |
| 1,000,000 | 500,000 | 20 | about 1.3 | 19,931,569 |

### Meaning for the university application

When the database grows by a factor of 1,000 (1,000 to 1,000,000 records), linear search does 1,000 times more work per query, binary search does only about twice as much (10 to 20 probes), and the hash table does the same amount of work. A search that is imperceptible at 1,000 records (about 17 microseconds measured) takes about 20 milliseconds at 10^6 records, and a front desk handling thousands of requests would notice this. The logarithmic and constant behaviours remain practical at any size the university might plausibly reach: doubling the database costs binary search one more probe, and the hash table nothing. The price is the preprocessing, which grows as n log n for binary search and as n for hashing, and it is paid only when the data changes.
