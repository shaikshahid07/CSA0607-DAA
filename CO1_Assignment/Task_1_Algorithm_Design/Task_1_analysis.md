# Task 1 - Design the Algorithm (5 Marks)

Shaik Shahid | Reg. No. 192424311 | CSA0607 Design and Analysis of Algorithms

Problem. Given a collection of n student records, each identified by a unique 9-digit registration number (for example 192424311), decide whether a given registration number K exists and return the position of its record. The records are stored in memory as an array in the order in which they were created, so the array is not sorted. The database grows from 1,000 to 1,000,000+ records.

Three algorithmic strategies that are genuinely different in design technique, preprocessing and cost behaviour were selected.

**Table 1.1  Summary of the three selected approaches**

| Approach | Design strategy | Form | Preprocessing | Data structure |
|---|---|---|---|---|
| A. Linear search | Brute force | Iterative | None | Unsorted array |
| B. Binary search | Decrease and conquer (by half) | Recursive | Sort: Theta(n log n) | Sorted array |
| C. Hash table lookup | Transform and conquer (space-time trade-off) | Iterative | Build table: Theta(n) | Table of m buckets with chaining |

### Approach A - Linear search (iterative, brute force)

Basic idea: examine the records one after another from the first position until the key is found or the end is reached. No assumption is made about the order of the data.

```text
ALGORITHM LinearSearch(A[0..n-1], K)
    // A: registration numbers in stored (unsorted) order, K: key
    for i <- 0 to n-1 do
        if A[i] = K then            // basic operation
            return i
    return -1                       // not found
```

![Figure 1.1  Flowchart of linear search](flowchart_linear_search.png)

*Figure 1.1  Flowchart of linear search*

Justification: it is the natural baseline. It needs no preprocessing, so it is the best choice for a very small database or for a one-off query, and it gives a reference against which the benefit of preprocessing can be measured.

### Approach B - Binary search (recursive, decrease and conquer)

Basic idea: if the registration numbers are sorted, compare K with the middle element. A match ends the search; otherwise the half that cannot contain K is discarded and the same procedure is applied to the remaining half. Each call reduces the problem size by a factor of two. Preprocessing: the records must first be sorted, and this cost is included in all later analysis. An iterative loop version of the same strategy was also coded, but only to compare implementation overhead; it is not counted as a separate approach.

```text
ALGORITHM BinarySearch(A[low..high], K)       // A sorted ascending
    if low > high then return -1                // base case: empty range
    mid <- floor((low + high) / 2)
    if A[mid] = K then return mid               // basic operation (one probe)
    else if K < A[mid] then
        return BinarySearch(A, K, low, mid - 1)  // left half
    else
        return BinarySearch(A, K, mid + 1, high) // right half

PREPROCESSING: A <- Sort(records)   // merge sort / Timsort, Theta(n log n)
First call: BinarySearch(A, K, 0, n-1)
```

![Figure 1.2  Flowchart of recursive binary search](flowchart_binary_search_recursive.png)

*Figure 1.2  Flowchart of recursive binary search*

Justification: registration numbers are totally ordered integers, so sorting is possible, and the logarithmic search time is the classic remedy for large databases. It is the only approach in the set that is recursive, and its recurrence is analysed in Tasks 6 and 7.

### Approach C - Hash table with chaining (iterative, transform and conquer)

Basic idea: instead of comparing keys repeatedly, compute where a key must be stored. A hash function h(K) = K mod m maps the registration number directly to one of m buckets (m is a prime near 1.5n, giving a load factor of about 0.67). Records that collide are chained in the same bucket. A search computes h(K) and scans only that short chain. Preprocessing: all n records are inserted once to build the table.

```text
ALGORITHM BuildHashTable(records[0..n-1])
    m <- smallest prime >= 1.5 n + 1
    T[0..m-1] <- empty lists
    for each k in records do
        append k to T[k mod m]              // n insertions

ALGORITHM HashSearch(T, m, K)
    h <- K mod m
    for each x in T[h] do
        if x = K then return FOUND          // basic operation
    return NOT FOUND
```

![Figure 1.3  Flowchart of hash table build and lookup](flowchart_hash_lookup.png)

*Figure 1.3  Flowchart of hash table build and lookup*

Justification: the problem is exact-match lookup by a unique key, which is exactly what hashing is designed for. It trades extra memory (about 1.5 slots per record) and a build cost for an expected constant search time, which becomes important when the number of searches is large (Task 12).

Diversity of the set: A uses no structure, B imposes order (sorting), C imposes address calculation (hashing). Iterative forms are A and C, the recursive form is B, so every requirement of the brief is met.
