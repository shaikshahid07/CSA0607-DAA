# Task 3 - Derive the Time-Complexity Function Mathematically (6 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

Input size: n = number of records in the database. C(n) denotes the number of times the basic operation is executed in one search. Running time T(n) = c * C(n) + c0, where c is the cost of one basic step (including its loop overhead) and c0 is constant set-up cost. The key is assumed to be present at each position with equal probability 1/n when the average successful case is derived.

### A. Linear search

If the key is at position i (1-based), the loop performs exactly i comparisons. Hence:

```text
Successful search at position i:   C(i) = i
```

```text
Average (successful) = (1/n) * SUM_{i=1..n} i = (1/n) * n(n+1)/2 = (n+1)/2
```

```text
Unsuccessful search: all n records are examined, C(n) = n
```

```text
Worst case: C_worst(n) = n    (key at last position or absent)
```

If a fraction p of the queries are for existing records, C_avg = p(n+1)/2 + (1-p)n. In every case C(n) is a linear function of n, so T(n) = a n + b, with a > 0. Preprocessing cost = 0. Total cost of q searches: q(n+1)/2 on average, q n in the worst case. For n = 1,000,000 the average is about 500,000 comparisons per search.

### B. Binary search with sorting

Searching. After the j-th probe the remaining range holds at most floor(n / 2^j) elements. The search must stop when the range is empty:

```text
floor(n / 2^j) = 0   <=>   2^j > n   <=>   j >= floor(log2 n) + 1
```

```text
C_worst(n) = floor(log2 n) + 1
```

Average successful case. Take n = 2^k - 1. The probes form a balanced decision tree with 2^(j-1) elements found at probe number j. Then:

```text
SUM_{j=1..k} j * 2^(j-1) = (k-1) * 2^k + 1        (check k = 3: 1 + 4 + 12 = 17 = 2*8 + 1)
```

```text
C_avg(n) = [(k-1) 2^k + 1] / (2^k - 1)  ~  k - 1 = log2(n+1) - 1
```

For n = 1,000,000 this gives 20 probes in the worst case and about 19 on average (measured 19.4 from 15 sample keys). Hence T_search(n) = c * log2 n + c0.

Preprocessing. Sorting by merge sort satisfies S(n) = 2 S(n/2) + (n - 1) comparisons, S(1) = 0, whose solution is S(n) ~ n log2 n (Master Theorem, case 2: a = 2, b = 2, f(n) = Theta(n) = Theta(n^(log_2 2))). For n = 1,000,000: n log2 n = 1,000,000 x 19.93 = about 1.99 x 10^7 comparisons.

```text
T_total(n, q) = n log2 n + q log2 n   =   Theta(n log n + q log n)
```

### C. Hash table with chaining

Table size m ~ 1.5 n, so the load factor is alpha = n / m ~ 0.67. Assuming the hash function spreads keys uniformly (simple uniform hashing), the chain in a bucket has expected length alpha.

```text
Unsuccessful search: scans a whole chain,   C = alpha  = 0.67 comparisons on average
```

```text
Successful search: C ~ 1 + alpha/2 = 1.33 comparisons on average
```

```text
T_search = c1 (hash computation) + c2 * C = Theta(1 + alpha) = Theta(1), independent of n
```

Worst case: all keys fall in one bucket, C = n, giving Theta(n); with a prime m and registration numbers that behave randomly modulo m this is practically impossible (measured longest chain: 4, 7, 6, 4 for the four sizes).

Preprocessing. Building needs n insertions of cost O(1) each plus allocation of m = 1.5 n buckets:

```text
T_build(n) = n c_ins + m c_alloc = Theta(n)        T_total(n, q) = Theta(n + q)
```

### Combined cost of preprocessing and searching (n = 1,000,000)

**Table 3.1  Theoretical operation counts at n = 10^6**

| Algorithm | Preprocessing (operations) | Per search (average) | Total for q searches |
|---|---|---|---|
| Linear | 0 | about 5.0 x 10^5 comparisons | 5.0 x 10^5 q |
| Binary + sort | about 2.0 x 10^7 comparisons | about 19 comparisons | 2.0 x 10^7 + 19 q |
| Hash table | about 1.0 x 10^6 insertions + 1.5 x 10^6 bucket allocations | about 1.1-1.3 comparisons | about 2.5 x 10^6 + 1.3 q |

Break-even (theory). Sorting pays for itself against linear search when n log2 n + q log2 n < q n / 2, i.e. q > n log2 n / (n/2 - log2 n), which is about 2 log2 n = 40 searches for n = 10^6. The hash table pays for its build earlier still in operation count, since its preprocessing is Theta(n) instead of Theta(n log n). These predictions are compared with measurements in Task 10.
