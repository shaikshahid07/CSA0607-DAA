# Task 2 - Identify the Basic Operation (2 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

The basic operation is the operation executed most often in the innermost part of the algorithm and therefore the one whose count determines the running time up to a constant factor. In all three algorithms it is a key comparison, but each lives in a different place and grows in a different way.

**Table 2.1  Basic operations**

| Algorithm | Basic operation | Where it occurs | Count as n grows |
|---|---|---|---|
| Linear search | Comparison A[i] = K | Body of the for loop | Grows in direct proportion to n (average (n+1)/2, worst n) |
| Binary search | Comparison of K with A[mid] | Once per call, after computing mid | Grows by 1 each time n doubles: floor(log2 n) + 1 in the worst case |
| Hash table | Comparison x = K inside the chain of bucket T[h] | Loop over the chain of one bucket | Independent of n: depends only on load factor alpha = n/m |

### Linear search

The loop body does an index increment, a bound check and one comparison with the key. The comparison is executed in every iteration, and the number of iterations is exactly the number of records examined, so the comparison count is a direct measure of the work done. Other statements (increment, bound check) execute the same number of times as the comparison, so they only change the constant factor. If the database doubles, the expected number of comparisons doubles.

### Binary search

Each call computes mid (constant work), compares K with A[mid], and makes at most one recursive call. The number of comparisons therefore equals the number of calls, which equals the depth of the recursion. Because the range halves in every call, doubling n adds only one extra call. In the implementation one probe is counted as one comparison (the three-way decision equal / less / greater is one basic step).

### Hash table lookup

Computing h(K) = K mod m is a single arithmetic operation executed once per search and does not depend on n. The part that can vary is the scan of the chain, whose length is the number of records that collided with K. The key comparison inside this scan is the operation that depends on the data, so it is chosen as the basic operation. Because m is proportional to n, the average chain length stays near alpha = 0.67 as n grows, and the comparison count stays nearly constant.

### Preprocessing operations

For binary search the basic operation of the sort is the comparison of two registration numbers (about n log2 n of them). For the hash table it is one insertion (hash computation plus append), executed n times. Linear search has no preprocessing.
