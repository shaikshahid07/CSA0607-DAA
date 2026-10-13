"""
CSA0607 - Design and Analysis of Algorithms
CO1 Assignment: Efficient Search Strategy for a Student Record System
Name: Shaik Shahid    Reg. No.: 192424311

Three distinct search strategies for a 9-digit registration number:
  1. Linear search            - iterative, brute force, no preprocessing
  2. Binary search            - recursive, decrease-and-conquer, needs sorting
                                (an iterative variant is included for comparison only)
  3. Hash table lookup        - transform-and-conquer / hashing, needs table build

Each algorithm has two forms:
  * a "counted" form returning (index_or_flag, comparisons) used for operation counts
  * a "plain" form without counters used for wall-clock timing
"""

# ---------------------------------------------------------------- 1. LINEAR
def linear_search(records, key):
    """Iterative sequential scan. Basic operation: records[i] == key."""
    for i in range(len(records)):
        if records[i] == key:
            return i
    return -1


def linear_search_counted(records, key):
    comparisons = 0
    for i in range(len(records)):
        comparisons += 1
        if records[i] == key:
            return i, comparisons
    return -1, comparisons


# ---------------------------------------------------------------- 2. BINARY
def binary_search_recursive(records, key, low, high):
    """Recursive binary search on a SORTED list. Basic operation: key vs records[mid]."""
    if low > high:                      # base case: empty sub-array
        return -1
    mid = (low + high) // 2
    if records[mid] == key:
        return mid
    if key < records[mid]:
        return binary_search_recursive(records, key, low, mid - 1)
    return binary_search_recursive(records, key, mid + 1, high)


def binary_search_recursive_counted(records, key, low, high, counter):
    """counter is a one-element list holding the number of key comparisons.
    Each probe is counted once (three-way comparison: equal / less / greater)."""
    if low > high:
        return -1
    mid = (low + high) // 2
    counter[0] += 1
    if records[mid] == key:
        return mid
    if key < records[mid]:
        return binary_search_recursive_counted(records, key, low, mid - 1, counter)
    return binary_search_recursive_counted(records, key, mid + 1, high, counter)


def binary_search_iterative(records, key):
    """Iterative variant (same strategy as above, kept only for implementation comparison)."""
    low, high = 0, len(records) - 1
    while low <= high:
        mid = (low + high) // 2
        if records[mid] == key:
            return mid
        if key < records[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def sort_records(records):
    """Preprocessing for binary search: O(n log n) comparison sort."""
    return sorted(records)


# ---------------------------------------------------------------- 3. HASH
class HashTable:
    """Hash table with separate chaining.
    h(k) = k mod m, m = a prime close to 1.5 n  (load factor about 0.67)."""

    @staticmethod
    def _next_prime(x):
        def is_prime(v):
            if v < 2:
                return False
            if v % 2 == 0:
                return v == 2
            d = 3
            while d * d <= v:
                if v % d == 0:
                    return False
                d += 2
            return True
        while not is_prime(x):
            x += 1
        return x

    def __init__(self, records):
        n = len(records)
        self.m = self._next_prime(int(1.5 * n) + 1)
        self.table = [None] * self.m
        for k in records:               # preprocessing: n insertions, O(n) expected
            h = k % self.m
            if self.table[h] is None:
                self.table[h] = [k]
            else:
                self.table[h].append(k)

    def search(self, key):
        bucket = self.table[key % self.m]
        if bucket is None:
            return False
        for k in bucket:
            if k == key:
                return True
        return False

    def search_counted(self, key):
        bucket = self.table[key % self.m]
        comparisons = 0
        if bucket is None:
            return False, comparisons
        for k in bucket:
            comparisons += 1
            if k == key:
                return True, comparisons
        return False, comparisons
