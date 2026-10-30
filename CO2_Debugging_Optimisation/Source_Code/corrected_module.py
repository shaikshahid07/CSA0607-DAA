"""
SentinelOps SOC Alert-Triage Module  --  CORRECTED VERSION (debugged, not rewritten)
CSA06 Design and Analysis of Algorithms | CO2 Debugging and Optimisation Task

The structure of the original code is kept exactly as it was (same function
names, same algorithms: insertion sort, sequential search, brute-force string
matching and brute-force closest pair).  Only the faulty lines were changed.
Every change is marked with a comment of the form   # FIX Dn   where Dn is the
defect number used in the report:

    D1, D2  sort_alerts       D3, D4  is_blocked
    D5, D6  find_signature    D7, D8, D9  closest_logins
"""
import math


def sort_alerts(alerts):
    """Insertion sort by severity, highest first; equal severities keep arrival order."""
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:    # FIX D1: was  j > 0  (index 0 never compared)
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key                        # FIX D2: was  alerts[j] = key  (wrong slot)
    return alerts


def is_blocked(blocklist, ip):
    """Sequential search: True if ip is on the blocklist, otherwise False."""
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return True                            # FIX D3: was  return False  (match reported as not-blocked)
        # FIX D4: the  else: return False  branch was removed - it ended the search
        #         after the very first element.  "Not found" is decided only after the loop.
    return False                                   # FIX D4: verdict after all elements were checked
                                                   #         (also makes an empty blocklist return False, not None)


def find_signature(log, pattern):
    """Brute-force string matching: every start position of pattern in log (overlaps included)."""
    n, m = len(log), len(pattern)
    hits = []
    if m == 0:                                     # boundary rule: an empty signature matches nothing
        return hits
    for i in range(n - m + 1):                     # FIX D5: was  range(n - m)  (last alignment skipped)
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        else:                                      # FIX D6: was  if j == m - 1  (also true after a break
            hits.append(i)                         #         at the last character -> false hit)
    return hits


def closest_logins(events):
    """Brute-force closest pair of login locations. Returns ((i, j), distance) with i < j."""
    if len(events) < 2:                            # boundary rule: no pair exists
        return None, None
    min_dist = math.inf                            # FIX D7: was  0  (nothing can be smaller than 0)
    pair = None
    for i in range(len(events)):
        for j in range(i + 1, len(events)):        # FIX D9: was  range(len(events))  (self-pairs and repeats)
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d < min_dist:                       # FIX D8: was  d > min_dist  (searched the FARTHEST pair)
                min_dist = d
                pair = (i, j)
    return pair, min_dist


if __name__ == "__main__":
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    print("=== CORRECTED MODULE : OUTPUT ===")
    print("sort_alerts      :", sort_alerts(list(alerts)))
    for q in queries:
        print(f"is_blocked({q!r:>12}) :", is_blocked(blocklist, q))
    print("find_signature   :", find_signature(log, pattern))
    print("closest_logins   :", closest_logins(events))
