"""Task 2 - Job Sequencing with Deadlines (greedy: descending profit, latest free slot).
Author: Shaik Shahid | Reg No: 192424311 | CSA0607 Design and Analysis of Algorithms
"""
import itertools
import random


def job_sequencing(jobs, verbose=False):
    """jobs: list of (id, deadline, profit). Returns (slots list, total profit)."""
    order = sorted(jobs, key=lambda j: (-j[2], j[0]))        # SORT by descending profit
    D = min(max(j[1] for j in jobs), len(jobs))               # no more slots than jobs are useful
    slot = [None] * (D + 1)                                   # slot[1..D]
    total = 0
    for jid, d, p in order:
        t = min(d, D)
        while t >= 1 and slot[t] is not None:                 # latest free slot <= deadline
            t -= 1
        if t >= 1:
            slot[t] = jid
            total += p
            if verbose:
                print(f"  job {jid} (d={d}, p={p}) -> slot {t}; total={total}")
        elif verbose:
            print(f"  job {jid} (d={d}, p={p}) -> REJECTED (no free slot <= {d})")
    return slot[1:], total


def brute_force(jobs):
    """Try every subset and every ordering; return best feasible profit."""
    best = 0
    for r in range(len(jobs) + 1):
        for sub in itertools.combinations(jobs, r):
            for perm in itertools.permutations(sub):
                if all(pos + 1 <= j[1] for pos, j in enumerate(perm)):
                    best = max(best, sum(j[2] for j in perm))
    return best


if __name__ == "__main__":
    jobs = [("A", 2, 80), ("B", 1, 35), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
    print("=== Desk-check instance ===")
    s, t = job_sequencing(jobs, True)
    print("Final schedule (slot 1..D):", s, "| Total profit:", t)
    assert t == 180 == brute_force(jobs)

    print("\n=== Challenge: change B's profit from 35 to 70 ===")
    jobs2 = [("A", 2, 80), ("B", 1, 70), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
    s2, t2 = job_sequencing(jobs2, True)
    print("Final schedule (slot 1..D):", s2, "| Total profit:", t2)
    assert t2 == 190 == brute_force(jobs2)

    print("\n=== Edge cases ===")
    print("All deadlines = 1 :", job_sequencing([("X", 1, 5), ("Y", 1, 9), ("Z", 1, 7)]))
    print("Single job        :", job_sequencing([("S", 3, 10)]))
    print("Deadline > n      :", job_sequencing([("M", 9, 4), ("N", 9, 6)]))

    print("\n=== Random validation against brute force (300 instances) ===")
    random.seed(7)
    for _ in range(300):
        n = random.randint(1, 6)
        js = [(f"J{i}", random.randint(1, 5), random.randint(1, 50)) for i in range(n)]
        assert job_sequencing(js)[1] == brute_force(js), js
    print("All 300 random instances matched the exhaustive optimum.")
