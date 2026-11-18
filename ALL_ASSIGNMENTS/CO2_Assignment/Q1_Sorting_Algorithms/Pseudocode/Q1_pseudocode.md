# Q1 – Sorting Under Different Data Conditions (Pseudocode + Predictions)

Problem: sort customer orders by dispatch priority score (ascending; lowest score = dispatched first).
Counted measures (primary evidence): **key comparisons**, **data movements** (swaps for Selection/Bubble, element shifts for Insertion).

## 1. Selection Sort
```
SelectionSort(A[0..n-1])
  for i <- 0 to n-2
      minIdx <- i
      for j <- i+1 to n-1
          comparisons++
          if A[j] < A[minIdx] then minIdx <- j
      if minIdx != i then
          swap A[i], A[minIdx] ; movements++
```
Logic: each pass scans the whole unsorted suffix to find its minimum and places it at position i. The scan never stops early, so comparisons do not depend on the data.

## 2. Bubble Sort (with early-exit flag)
```
BubbleSort(A[0..n-1])
  for pass <- 0 to n-2
      swapped <- false
      for j <- 0 to n-2-pass
          comparisons++
          if A[j] > A[j+1] then swap A[j], A[j+1] ; movements++ ; swapped <- true
      if swapped = false then exit      // already sorted
```
Logic: adjacent exchanges; one pass carries the largest remaining element to the end. Each swap removes exactly one inversion. A small element can move left by only ONE position per pass.

## 3. Insertion Sort
```
InsertionSort(A[0..n-1])
  for i <- 1 to n-1
      key <- A[i] ; j <- i-1
      while j >= 0
          comparisons++
          if A[j] > key then A[j+1] <- A[j] ; movements++ ; j <- j-1
          else break
      A[j+1] <- key
```
Logic: grow a sorted prefix; shift larger elements one place right and drop the key into the gap. Work = n-1 + number of inversions.

## 4. Test datasets (designed before running)
| ID | Dataset | Purpose |
|----|---------|---------|
| D1 | Random permutation of n scores | typical average case |
| D2 | Nearly sorted: first 95% already in priority order, newest 5% (random scores) appended at the end | exactly the fulfilment-centre scenario |
| D3 | Edge case (own): strictly reverse-sorted | worst case, maximum inversions n(n-1)/2 |
| extra | Already sorted; all-equal scores | sanity / duplicates behaviour |

## 5. Predictions (written BEFORE execution, n = 1000 headline)
Let I = number of inversions.
* Selection: comparisons = n(n-1)/2 = 499,500 on EVERY dataset (no early exit); swaps at most n-1 (about n-1 for random, about n/2 for reverse).
* Bubble: swaps = I; comparisons close to n(n-1)/2 for D1 and D3 (about 495k for random, exactly 499,500 for reverse). For D2 I expect it to stay expensive (several hundred thousand comparisons) because each late small element crawls left one position per pass, so about as many passes as the largest displacement are needed.
* Insertion: comparisons about I + n - 1, shifts = I. D1: I about 249,750 -> about 250k. D2: I about 50 x 475 + 50x49/4 about 24.4k -> about 25k comparisons (around 20 times fewer than Selection). D3: I = 499,500 -> 499,500 comparisons and shifts.
* Sorted input: Bubble and Insertion about n-1 = 999 comparisons, 0 movements; Selection still 499,500.
* Recommendation hypothesis: Insertion Sort for the 95%-sorted workload.
