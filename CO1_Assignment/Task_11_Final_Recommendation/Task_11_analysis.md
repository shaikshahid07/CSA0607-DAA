# Task 11 - Recommend and Defend the Final Design (4 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

Recommendation (for the original scenario): binary search on a sorted array of registration numbers.

### Why it is the most appropriate for the stated scenario

The scenario fixes no search rate and speaks of a database that grows. Under those conditions the design must be efficient for both very few and very many queries, simple to maintain, and predictable in the worst case. The evidence is as follows.

**Table 11.1  Evidence for the recommendation**

| Criterion | Linear | Binary + sort | Hash |
|---|---|---|---|
| Worst-case search (theory) | Theta(n) | Theta(log n) | Theta(n), expected Theta(1) |
| Search at n = 10^6 (measured) | 20.6 ms | 2.82 us | 0.12 us |
| Preprocessing at n = 10^6 (measured) | none | 0.3210 s | 0.9690 s |
| Searches needed to repay preprocessing vs linear | - | about 16 | about 47 |
| Memory | n slots | n slots | about 1.5 n slots plus chain overhead |
| Guaranteed worst case | yes (n) | yes (log n) | no (n possible) |
| Ordered output / range queries | no | yes | no |

- Theoretical efficiency: Theta(log n) per search with Theta(n log n) preprocessing; recursion depth at most 20 for a million records.
- Experimental performance: 2.82 microseconds per search at 10^6 records, about 7,279 times faster than linear search, with 19-20 comparisons in every case.
- Preprocessing cost: 0.3210 s to sort 10^6 records, repaid after about 16 searches. It is the cheapest preprocessing of the two that need any, and for a database that grows the sorted order can be kept by merging new records.
- Compared with the hash table: binary search is slower per lookup, but its preprocessing is about three times cheaper in the measurements, it uses less memory, it has a guaranteed worst case that does not depend on the quality of a hash function, and it supports ordered operations such as listing registration numbers in a range. Compared with linear search: there is no case, beyond the first dozen queries, in which linear search is competitive.
- Trade-offs and limitations: the array must stay sorted, so inserting a single record into the middle costs Theta(n) unless records are added in batches; the hash table's expected constant time is better when the lookups are very frequent (see Task 12).

Practicality as the database grows: at 10^6 records binary search needs 20 probes; at 10^9 records it would need only 30. The structure therefore remains practical far beyond the sizes tested, while linear search, extrapolating the measured 20 ms at 10^6 records, would take about 20 seconds per query at 10^9 records.
