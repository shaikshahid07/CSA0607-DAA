# Task 4 - Analyse Best, Average and Worst-Case Behaviour (4 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

### Linear search

Best case: the key is the first record. The first comparison succeeds and the loop exits, so C = 1 = Theta(1). Average case: the key is equally likely to be at any of the n positions, so on average half the array is scanned: C = (n+1)/2; if the key may also be absent the average rises towards n. Worst case: the key is the last record or is absent, so every record is compared: C = n. The differences arise only from where the key sits relative to the start of the unsorted array, because nothing about the data lets the algorithm skip any record.

### Binary search

Best case: the key sits exactly at the first mid position, so one probe suffices: C = 1. Average case: keys are equally likely to be anywhere; half of all keys are in the deepest level of the decision tree, a quarter in the next, and so on, so the expected depth is about log2 n - 1. Worst case: the key is absent or is found only when the range has shrunk to one element, giving floor(log2 n) + 1 probes. The count is bounded by the height of the halving process, so even the worst case is only a few more probes than the average. The array must be sorted; without that the elimination step is invalid.

### Hash table

Best case: the key's bucket holds only that key: C = 1 (or C = 0 for an absent key whose bucket is empty). Average case: with load factor alpha = 0.67 the expected number of comparisons is 1 + alpha/2 = 1.33 for present keys and alpha = 0.67 for absent keys. Worst case: all n keys collide into one bucket, which turns the lookup into a linear scan, C = n = Theta(n). This happens only with a poor hash function or adversarial keys; it is the reason hashing has a good expected, but weaker guaranteed, bound.

**Table 4.1  Operation counts by case (derived)**

| Case | Linear (comparisons) | Binary (comparisons) | Hash (comparisons) |
|---|---|---|---|
| Best | 1 (key first) | 1 (key at first mid) | 1 (alone in bucket) |
| Average (key present) | (n+1)/2 | about log2 n - 1 | about 1 + alpha/2 = 1.33 |
| Worst | n (last or absent) | floor(log2 n) + 1 | n (all collide); practically 4-7 |

### Measured behaviour at n = 1,000,000

**Table 4.2  Measured comparison counts at n = 1,000,000 (first/middle/last refer to the unsorted storage order)**

| Query | Linear | Binary (recursive) | Hash |
|---|---|---|---|
| First record | 1 | 20 | 1 |
| Middle record | 500,001 | 20 | 1 |
| Last record | 1,000,000 | 19 | 1 |
| Absent key | 1,000,000 | 19 | 1 |
| Average of 15 random present keys | 530,497.1 | 19.4 | 1.1 |

The measurements agree with the analysis: linear search needs 1 comparison for the first record and 10^6 for the last or an absent key; binary search needs 19-20 probes whatever the key, which shows how little best and worst differ; the hash table needs about one comparison in all cases.
