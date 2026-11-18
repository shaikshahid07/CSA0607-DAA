# Task 10 - Compare Theory with Experimental Behaviour (4 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

### Operation counts agree closely with theory

**Table 10.1  Measured and predicted average comparisons**

| n | Linear: measured / theory (n/2) | Binary: measured / theory (log2 n - 1) | Hash: measured / theory (1.33) |
|---|---|---|---|
| 1,000 | 509 / 500 | 8.9 / 9.0 | 1.33 / 1.33 |
| 10,000 | 5,103 / 5,000 | 12.5 / 12.3 | 1.37 / 1.33 |
| 100,000 | 46,930 / 50,000 | 15.9 / 15.6 | 1.32 / 1.33 |
| 1,000,000 | 530,497 / 500,000 | 19.4 / 18.9 | 1.13 / 1.33 |

Linear search comparisons follow n/2 almost exactly (differences come from the small random sample of keys). Binary search comparisons rise by about 3.4-3.6 for every tenfold increase in n, which equals log2 10 = 3.32, as predicted. Hash lookups stay near 1.1-1.4 comparisons at every size, consistent with 1 + alpha/2 = 1.33, and the longest chain observed never exceeded 7, so the uniform-hashing assumption is sound for these keys.

### Growth of running time

Linear search: when n grows tenfold the average time grows by factors of 11.5, 11.1 and 9.5, close to the predicted 10, confirming Theta(n). At n = 10^6 the average search is 20.6 ms, i.e. about 39 ns per comparison in this interpreter. Binary search: time per search changes by only a few microseconds over a 1,000-fold increase in n, and the hash lookup stays near 0.1-0.2 microseconds throughout; both are flat compared with the linear curve (Figure 9.1).

Preprocessing: sorting time grows by factors of 16.3, 14.1 and 14.6 per tenfold increase in n, against the predicted n log n ratios of 13.3, 12.5 and 12.0: the Theta(n log n) behaviour is confirmed. Hash building grows by 10.2, 28.9 and 17.2, which is the theoretical 10 for the smallest step but noticeably higher for the larger sizes.

### Which algorithm scales better

By search time, hash table > binary search >> linear search. At n = 10^6, a hash lookup takes 0.12 microseconds, a binary search 2.82 microseconds and a linear scan 20.6 milliseconds, which is about 7,279 times slower than binary search. Including preprocessing, the scaling order depends on the number of searches (Figure 9.5, Task 12).

### Differences between prediction and observation, and why

- Binary search time is not perfectly monotonic (it is lower at n = 10^6 than at n = 10^5). For large n only a few random keys (15) were timed, repeated 200 times, so the same few memory locations stay in the CPU cache; at n = 10^5 more distinct keys were used. Timings of microsecond-level operations are also sensitive to timer resolution and system noise. The comparison counts, which are exact, are not affected and confirm log n growth.
- Hash build time grows faster than linearly (29x and 17x for the last two tenfold steps). The theory counts operations, but the real cost per insertion rises with n because the table of 1.5 million buckets no longer fits in the CPU cache, and each insertion creates a Python list object. This is a memory-hierarchy effect, not a change of complexity class. The table also shows that a pure-Python chained table pays a high constant factor.
- Recursive binary search is slower than the iterative loop by a factor of 1.13-1.33, because every recursive call costs a function call (frame creation, argument passing). The asymptotic class is the same, which supports treating iteration and recursion as one strategy.
- Sorting is faster in practice than the n log2 n comparison count suggests because Python's built-in sorted() runs in compiled code, whereas the hash build and the searches are interpreted Python. This is why the predicted break-even of about 40 searches for sort-versus-linear is found experimentally at about 16 searches.
- Absolute times depend on the machine and the interpreter. Only growth trends and ratios should be compared with theory.
