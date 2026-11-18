"""
SentinelOps SOC Alert-Triage Module  --  ORIGINAL (BUGGY) VERSION
CSA06 Design and Analysis of Algorithms | CO2 Debugging and Optimisation Task

This file is the junior developer's code EXACTLY as given in the question paper.
The only addition is the demo at the bottom, which runs the module on the
given test data so the actual (wrong) outputs can be recorded.
DO NOT use this file in production - it contains nine defects.
"""
import math


def sort_alerts(alerts):            # insertion sort by severity, highest first
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j > 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j] = key
    return alerts


def is_blocked(blocklist, ip):      # sequential search
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return False
        else:
            return False


def find_signature(log, pattern):   # brute-force string matching, all occurrences
    n, m = len(log), len(pattern)
    hits = []
    for i in range(n - m):
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        if j == m - 1:
            hits.append(i)
    return hits


def closest_logins(events):         # brute-force closest pair of login locations
    min_dist = 0
    pair = None
    for i in range(len(events)):
        for j in range(len(events)):
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d > min_dist:
                min_dist = d
                pair = (i, j)
    return pair, min_dist


if __name__ == "__main__":
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    print("=== ORIGINAL MODULE : ACTUAL OUTPUT ===")
    print("sort_alerts      :", sort_alerts(list(alerts)))
    for q in queries:
        print(f"is_blocked({q!r:>12}) :", is_blocked(blocklist, q))
    print("find_signature   :", find_signature(log, pattern))
    print("closest_logins   :", closest_logins(events))
