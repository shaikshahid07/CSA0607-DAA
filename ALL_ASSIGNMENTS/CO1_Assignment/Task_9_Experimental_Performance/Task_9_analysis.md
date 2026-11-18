# Task 9 - Record Experimental Performance (3 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

All values are measured by run_experiments.py (raw data in results.csv). Times are per search in microseconds unless stated.

**Table 9.1  Average search time (microseconds), random present keys**

| n | Linear | Binary (recursive) | Binary (iterative) | Hash |
|---|---|---|---|---|
| 1,000 | 16.8 | 1.36 | 1.20 | 0.18 |
| 10,000 | 193.9 | 1.94 | 1.66 | 0.15 |
| 100,000 | 2,161 | 3.90 | 2.94 | 0.21 |
| 1,000,000 | 20,555 | 2.82 | 2.38 | 0.12 |

**Table 9.2  Worst-case search time (microseconds), absent key**

| n | Linear | Binary (recursive) | Binary (iterative) | Hash |
|---|---|---|---|---|
| 1,000 | 33.3 | 1.79 | 1.00 | 0.16 |
| 10,000 | 333.0 | 1.59 | 1.47 | 0.11 |
| 100,000 | 4,618 | 3.45 | 2.70 | 0.40 |
| 1,000,000 | 48,808 | 2.42 | 2.00 | 0.11 |

**Table 9.3  Key comparisons per search**

| n | Linear avg | Linear worst | Binary avg | Binary worst | Hash avg | Hash worst (absent) |
|---|---|---|---|---|---|---|
| 1,000 | 509.0 | 1,000 | 8.9 | 9 | 1.3 | 1 |
| 10,000 | 5,103.4 | 10,000 | 12.5 | 13 | 1.4 | 1 |
| 100,000 | 46,930.5 | 100,000 | 15.9 | 16 | 1.3 | 2 |
| 1,000,000 | 530,497.1 | 1,000,000 | 19.4 | 19 | 1.1 | 1 |

**Table 9.4  Preprocessing cost and hash table statistics**

| n | Sort time (s) | Hash build time (s) | Hash table size m | Longest chain | Mean chain (non-empty) |
|---|---|---|---|---|---|
| 1,000 | 0.0001 | 0.0002 | 1,511 | 4 | 1.37 |
| 10,000 | 0.0016 | 0.0019 | 15,013 | 7 | 1.38 |
| 100,000 | 0.0220 | 0.0564 | 150,001 | 6 | 1.36 |
| 1,000,000 | 0.3210 | 0.9690 | 1,500,007 | 4 | 1.28 |

![Figure 9.1  Average search time versus n (log-log axes)](../Report/Tables_and_Graphs/fig_avg_time_vs_n.png)

*Figure 9.1  Average search time versus n (log-log axes)*

![Figure 9.2  Worst-case (absent key) search time versus n](../Report/Tables_and_Graphs/fig_worst_time_vs_n.png)

*Figure 9.2  Worst-case (absent key) search time versus n*

![Figure 9.3  Average comparisons versus n, with theoretical curves n/2 and log2(n) - 1](../Report/Tables_and_Graphs/fig_comparisons_vs_n.png)

*Figure 9.3  Average comparisons versus n, with theoretical curves n/2 and log2(n) - 1*

![Figure 9.4  Preprocessing time versus n](../Report/Tables_and_Graphs/fig_preprocessing.png)

*Figure 9.4  Preprocessing time versus n*

![Figure 9.5  Total cost including preprocessing versus number of searches, n = 1,000,000](../Report/Tables_and_Graphs/fig_total_cost_1M.png)

*Figure 9.5  Total cost including preprocessing versus number of searches, n = 1,000,000*
