# Q3 – Brute-Force String Matching (Pseudocode + Predictions)

```
BruteForceMatch(T[0..n-1], P[0..m-1])
  comparisons <- 0
  for i <- 0 to n-m                      // every alignment of P under T
      j <- 0
      while j < m
          comparisons++                  // one character comparison
          if T[i+j] != P[j] then break
          j <- j+1
      if j = m then return i, comparisons   // first match
  return NOT_FOUND, comparisons
```
Logic: slide the pattern one position at a time; at each alignment compare left to right and abandon the alignment at the first mismatch. After a mismatch nothing learned is kept, so characters of T are re-compared at the next alignment.

Exact cost model: between (n-m+1) comparisons (every alignment fails on its 1st character) and m(n-m+1) (every alignment matches m-1 characters first).

## Test conditions
* **A (low work):** T = "abcdefghij" repeated to n = 10,000; P = "ZERO#ALRT" (m = 9, first character never occurs in T).
* **B (engineered high work):** T = "A" x 10,000; P = "A" x 49 + "B" (m = 50).
* **C (own choice, realistic log):** synthetic authentication log lines, with the target signature "AUTH FAILED user=root" occurring only in the very last line, while all earlier lines share the long prefix "AUTH FAILED user=" (partial matches).
* Extras: D = pattern found at the very start; E = scaling of A and B for n = 1,000 ... 32,000; F = effect of m on B.

## Predictions (before execution)
* A: no alignment can pass the first character, so comparisons = n-m+1 = 9,992.
* B: each of the n-m+1 = 9,951 alignments matches 49 characters and fails on the 50th, so comparisons = 9,951 x 50 = 497,550 (about 50 times more than A for the same n).
* C: the long common prefix makes many alignments run about 17 characters before failing; I expect the count to be somewhere between 1.1n and 1.5n (clearly above A, far below B).
* D: m comparisons only.
* Same n, same algorithm, work differs by ~50x, so input size n alone cannot describe the cost; the repeated-prefix structure of text and pattern does.
