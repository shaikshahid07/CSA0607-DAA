"""
SentinelOps SOC Alert-Triage Module  --  OPTIMISED PRODUCTION VERSION
CSA06 Design and Analysis of Algorithms | CO2 Debugging and Optimisation Task

Workload this module is tuned for: about 50,000 alerts and batches of 8,000
login events per day.  Every optimisation keeps the output identical to
corrected_module.py (this is checked by test_harness.py).

Summary of the optimisations
----------------------------
sort_alerts          insertion sort O(n^2)      ->  Timsort via sorted()      O(n log n), O(n) if nearly sorted
is_blocked           sequential search O(n)     ->  hash set lookup           O(1) average per query
find_signature       brute force, redundant     ->  brute force with no waste, plus Horspool and
                     checks removed                 str.find() for comparison
closest_logins       O(n^2) with sqrt, i != j   ->  i < j, squared distances, sorted-axis pruning,
                                                    plus a divide-and-conquer version O(n log n)

Optional argument  stats  (a dict) is used by the experiments to count basic
operations; it is ignored when it is None, so normal use is not slowed down.
"""
import math


# --------------------------------------------------------------------------
# 1. Sorting alerts
# --------------------------------------------------------------------------
def sort_alerts(alerts):
    """Return the alerts sorted by severity, highest first.

    Alerts with equal severity keep their arrival order, because Python's sort
    is stable and reverse=True preserves the original order of equal elements.

    Args:
        alerts: list of (alert_id, severity) tuples.
    Returns:
        A new sorted list (the input list is not modified).
    Complexity: O(n log n) worst case, O(n) when the data is already
    (nearly) in order, because Timsort detects existing runs.
    """
    return sorted(alerts, key=lambda alert: alert[1], reverse=True)


def insertion_sort_alerts(alerts, stats=None):
    """Corrected insertion sort, kept as a reference and for the comparison experiments.

    Sorts IN PLACE by severity (highest first, stable) and returns the list.
    If stats is a dict, stats['comparisons'] receives the number of severity
    comparisons made and stats['shifts'] the number of element moves.
    """
    comparisons = shifts = 0
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0:
            comparisons += 1                     # one severity comparison
            if alerts[j][1] < key[1]:
                alerts[j + 1] = alerts[j]        # shift the smaller severity one place right
                shifts += 1
                j -= 1
            else:
                break
        alerts[j + 1] = key
    if stats is not None:
        stats["comparisons"], stats["shifts"] = comparisons, shifts
    return alerts


class _CountingKey:
    """Wrapper that counts how many times Python's sort compares two severities."""
    count = 0
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        _CountingKey.count += 1
        return self.v < other.v


def sort_alerts_counted(alerts, stats):
    """Same result as sort_alerts(), but records stats['comparisons'] (used in experiments)."""
    _CountingKey.count = 0
    result = sorted(alerts, key=lambda a: _CountingKey(a[1]), reverse=True)
    stats["comparisons"] = _CountingKey.count
    return result


# --------------------------------------------------------------------------
# 2. Blocklist lookups
# --------------------------------------------------------------------------
def build_blocklist(blocklist):
    """Build the lookup index ONCE (O(n)); reuse it for every query."""
    return frozenset(blocklist)


def is_blocked(blocklist_index, ip):
    """True if ip is on the blocklist.

    blocklist_index should come from build_blocklist(); a plain list also works
    (same answer) but then each lookup is a slow O(n) sequential search.
    Complexity: O(1) average per lookup with the hash-set index.
    """
    return ip in blocklist_index


def is_blocked_sequential(blocklist, ip, stats=None):
    """Corrected sequential search, kept for the comparison experiment.

    If stats is a dict, stats['comparisons'] receives the number of equality tests.
    """
    comparisons = 0
    found = False
    for item in blocklist:
        comparisons += 1
        if item == ip:
            found = True
            break
    if stats is not None:
        stats["comparisons"] = comparisons
    return found


# --------------------------------------------------------------------------
# 3. Signature search (all occurrences, overlaps included)
# --------------------------------------------------------------------------
def find_signature(log, pattern, stats=None):
    """Brute-force string matching with no redundant work.

    Redundancy removed compared with the original:
      * only the n - m + 1 alignments that can actually fit are tried;
      * a window is rejected at its FIRST mismatching character (early exit);
      * there is no extra test after the inner loop (for/else instead).
    If stats is a dict, stats['comparisons'] receives the character comparisons.
    Returns the list of start positions ([] for an empty pattern or one longer than the log).
    """
    n, m = len(log), len(pattern)
    hits = []
    comparisons = 0
    if m == 0 or m > n:
        if stats is not None:
            stats["comparisons"] = 0
        return hits
    for i in range(n - m + 1):
        for j in range(m):
            comparisons += 1
            if log[i + j] != pattern[j]:
                break
        else:
            hits.append(i)
    if stats is not None:
        stats["comparisons"] = comparisons
    return hits


def find_signature_horspool(log, pattern, stats=None):
    """Horspool's algorithm: compares the window right-to-left and skips ahead using a shift table.

    Same output as find_signature(); on average far fewer comparisons for longer patterns.
    """
    n, m = len(log), len(pattern)
    hits = []
    comparisons = 0
    if m == 0 or m > n:
        if stats is not None:
            stats["comparisons"] = 0
        return hits
    shift = {}                                   # distance from the last occurrence to the pattern end
    for k in range(m - 1):
        shift[pattern[k]] = m - 1 - k
    i = 0
    while i <= n - m:
        k = m - 1
        while k >= 0:
            comparisons += 1
            if log[i + k] != pattern[k]:
                break
            k -= 1
        if k < 0:
            hits.append(i)
        i += shift.get(log[i + m - 1], m)        # skip based on the window's LAST character
    if stats is not None:
        stats["comparisons"] = comparisons
    return hits


def find_signature_builtin(log, pattern):
    """Same output using the C-implemented str.find() in a loop (fastest in practice)."""
    hits = []
    if not pattern or len(pattern) > len(log):
        return hits
    i = log.find(pattern)
    while i != -1:
        hits.append(i)
        i = log.find(pattern, i + 1)             # i + 1 so overlapping matches are found too
    return hits


# --------------------------------------------------------------------------
# 4. Closest pair of login locations
# --------------------------------------------------------------------------
def closest_logins_bruteforce(events, stats=None):
    """Corrected brute force (every pair i < j, with square roots) - the 'before' baseline."""
    count = 0
    if len(events) < 2:
        if stats is not None:
            stats["distance_computations"] = 0
        return None, None
    min_dist = math.inf
    pair = None
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            count += 1
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d < min_dist:
                min_dist = d
                pair = (i, j)
    if stats is not None:
        stats["distance_computations"] = count
    return pair, min_dist


def closest_logins(events, stats=None):
    """Optimised brute force. Returns ((i, j), distance) with i < j, or (None, None) if < 2 events.

    Optimisations (output identical to the corrected brute force):
      1. only pairs with i < j are examined: no self-pairs, no repeated pairs;
      2. squared distances are compared, so math.sqrt is called only ONCE at the end;
      3. pruning: points are sorted along the axis with the larger spread; for each
         point the scan to the right stops as soon as the gap along that axis alone
         already exceeds the best distance found (no later point can be closer);
      4. ties are broken exactly like the plain brute force (smallest (i, j) wins).
    """
    n = len(events)
    if n < 2:
        if stats is not None:
            stats["distance_computations"] = 0
        return None, None
    xs = [e[0] for e in events]
    ys = [e[1] for e in events]
    axis = 0 if (max(xs) - min(xs)) >= (max(ys) - min(ys)) else 1
    order = sorted(range(n), key=lambda k: events[k][axis])
    best = math.inf                                # best SQUARED distance so far
    best_pair = None
    count = 0
    for a in range(n):
        ia = order[a]
        xa, ya = events[ia][0], events[ia][1]
        va = events[ia][axis]
        for b in range(a + 1, n):
            ib = order[b]
            gap = events[ib][axis] - va
            if gap * gap > best:                   # prune: the rest are even farther along the axis
                break
            dx = xa - events[ib][0]
            dy = ya - events[ib][1]
            d2 = dx * dx + dy * dy
            count += 1
            cand = (ia, ib) if ia < ib else (ib, ia)
            if d2 < best or (d2 == best and cand < best_pair):
                best, best_pair = d2, cand
    if stats is not None:
        stats["distance_computations"] = count
    return best_pair, math.sqrt(best)


def closest_logins_dc(events, stats=None):
    """Divide-and-conquer closest pair, O(n log n). Same output as closest_logins().

    Split by x, solve both halves, then check only the narrow vertical strip around
    the dividing line: each strip point needs to be compared with at most a few
    neighbours in y-order.
    """
    n = len(events)
    counter = [0]
    if n < 2:
        if stats is not None:
            stats["distance_computations"] = 0
        return None, None
    pts = [(events[k][0], events[k][1], k) for k in range(n)]
    px = sorted(pts)                               # sorted by x (then y, index)
    py = sorted(pts, key=lambda p: (p[1], p[0], p[2]))

    def d2_of(p, q):
        counter[0] += 1
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    def cand_of(p, q):
        return (p[2], q[2]) if p[2] < q[2] else (q[2], p[2])

    def better(a, b):                              # (d2, pair) tuples: smaller wins, ties -> smaller pair
        return a if a <= b else b

    def solve(px, py):
        size = len(px)
        if size <= 3:                              # base case: brute force
            best = (math.inf, None)
            for i in range(size):
                for j in range(i + 1, size):
                    best = better(best, (d2_of(px[i], px[j]), cand_of(px[i], px[j])))
            return best
        mid = size // 2
        mid_x = px[mid][0]
        left_ids = {p[2] for p in px[:mid]}
        pyl = [p for p in py if p[2] in left_ids]
        pyr = [p for p in py if p[2] not in left_ids]
        best = better(solve(px[:mid], pyl), solve(px[mid:], pyr))
        strip = [p for p in py if (p[0] - mid_x) ** 2 <= best[0]]
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) ** 2 > best[0]:
                    break                          # farther apart in y than the best distance
                best = better(best, (d2_of(strip[i], strip[j]), cand_of(strip[i], strip[j])))
        return best

    best_d2, best_pair = solve(px, py)
    if stats is not None:
        stats["distance_computations"] = counter[0]
    return best_pair, math.sqrt(best_d2)


if __name__ == "__main__":
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    print("=== OPTIMISED MODULE : OUTPUT ===")
    print("sort_alerts          :", sort_alerts(alerts))
    index = build_blocklist(blocklist)
    for q in queries:
        print(f"is_blocked({q!r:>12}) :", is_blocked(index, q))
    print("find_signature       :", find_signature(log, pattern))
    print("find_signature_horspool:", find_signature_horspool(log, pattern))
    print("find_signature_builtin :", find_signature_builtin(log, pattern))
    print("closest_logins       :", closest_logins(events))
    print("closest_logins_dc    :", closest_logins_dc(events))
