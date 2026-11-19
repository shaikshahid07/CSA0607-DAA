"""Task 6 - Energy-aware job scheduling = Weighted Interval Scheduling, solved by Dynamic Programming.
Author: Shaik Shahid | Reg No: 192424311 | CSA0607 Design and Analysis of Algorithms
"""
import bisect
import itertools
import random

JOBS = [("J1", 1, 3, 20), ("J2", 2, 5, 50), ("J3", 4, 6, 30), ("J4", 6, 8, 40),
        ("J5", 5, 9, 60), ("J6", 8, 10, 30), ("J7", 9, 11, 50), ("J8", 11, 13, 40)]


def schedule(jobs, verbose=False):
    """jobs: list of (id, start, finish, value). Returns (best value, chosen ids)."""
    J = sorted(jobs, key=lambda j: (j[2], j[1]))              # SORT by finish time
    n = len(J)
    finishes = [j[2] for j in J]
    p = [0] * (n + 1)                                         # p[j] = last job compatible with job j
    for j in range(1, n + 1):
        p[j] = bisect.bisect_right(finishes, J[j - 1][1], 0, j - 1)   # finish <= start
    OPT = [0] * (n + 1)
    take = [False] * (n + 1)
    for j in range(1, n + 1):
        incl = J[j - 1][3] + OPT[p[j]]
        excl = OPT[j - 1]
        if incl > excl:
            OPT[j], take[j] = incl, True
        else:
            OPT[j] = excl
        if verbose:
            print(f"  j={j} {J[j-1][0]} [{J[j-1][1]},{J[j-1][2]}] v={J[j-1][3]:<3} p={p[j]}  "
                  f"include={J[j-1][3]}+OPT[{p[j]}]={incl:<4} exclude=OPT[{j-1}]={excl:<4} -> OPT[{j}]={OPT[j]} "
                  f"({'INCLUDE' if take[j] else 'EXCLUDE'})")
    chosen, j = [], n
    while j > 0:
        if take[j]:
            chosen.append(J[j - 1][0])
            j = p[j]
        else:
            j -= 1
    chosen.reverse()
    return OPT[n], chosen


def brute_force(jobs):
    best = 0
    for r in range(len(jobs) + 1):
        for sub in itertools.combinations(jobs, r):
            ordered = sorted(sub, key=lambda j: j[1])
            if all(ordered[i][2] <= ordered[i + 1][1] for i in range(len(ordered) - 1)):
                best = max(best, sum(j[3] for j in sub))
    return best


def greedy(jobs, key):
    """Generic greedy: scan jobs in key order, accept if compatible with all accepted jobs."""
    acc = []
    for j in sorted(jobs, key=key):
        if all(j[2] <= a[1] or a[2] <= j[1] for a in acc):
            acc.append(j)
    return sum(a[3] for a in acc), sorted(a[0] for a in acc)


STRATEGIES = {
    "earliest finish": lambda j: (j[2], j[1]),
    "highest value": lambda j: (-j[3], j[2]),
    "shortest duration": lambda j: (j[2] - j[1], j[2]),
}


def compare(title, jobs):
    print(f"--- {title} ---")
    print("Jobs:", jobs)
    for name, key in STRATEGIES.items():
        v, ids = greedy(jobs, key)
        print(f"  greedy by {name:<18}: value={v:<4} jobs={ids}")
    v, ids = schedule(jobs)
    print(f"  DP (weighted intervals)       : value={v:<4} jobs={ids}")
    print(f"  Exhaustive optimum            : {brute_force(jobs)}")
    assert v == brute_force(jobs)


if __name__ == "__main__":
    print("=== Given dataset: DP trace (jobs sorted by finish time) ===")
    best, chosen = schedule(JOBS, verbose=True)
    print("Selected jobs:", chosen, "| Maximum total energy-saving value:", best)
    assert best == 200 and chosen == ["J2", "J5", "J7", "J8"] == ["J2", "J5", "J7", "J8"]
    assert best == brute_force(JOBS)

    print("\n=== Greedy strategies on the given dataset ===")
    compare("Given dataset", JOBS)

    print("\n=== Adversarial datasets (Stage 6) ===")
    adv1 = [("K1", 1, 2, 5), ("K2", 1, 10, 100), ("K3", 2, 4, 5), ("K4", 4, 6, 5), ("K5", 6, 10, 5)]
    adv2 = [("M1", 1, 10, 50), ("M2", 1, 3, 20), ("M3", 3, 6, 20), ("M4", 6, 10, 20), ("M5", 2, 8, 15)]
    compare("Adversarial set A (many small compatible jobs vs one valuable long job)", adv1)
    print()
    compare("Adversarial set B (one tempting high-value long job vs three smaller compatible jobs)", adv2)

    print("\n=== Boundary tests ===")
    print("Touching jobs [1,3] and [3,5] both selectable:", schedule([("X", 1, 3, 10), ("Y", 3, 5, 10)]))
    print("Identical intervals, different values       :", schedule([("X", 1, 4, 10), ("Y", 1, 4, 25)]))
    print("Single job                                  :", schedule([("S", 2, 7, 9)]))
    print("Fully overlapping jobs                      :", schedule([("A", 1, 9, 5), ("B", 2, 8, 7), ("C", 3, 7, 6)]))

    print("\n=== Random validation against exhaustive search (400 instances) ===")
    random.seed(21)
    for _ in range(400):
        n = random.randint(1, 9)
        js = []
        for i in range(n):
            s = random.randint(1, 12)
            js.append((f"R{i}", s, s + random.randint(1, 6), random.randint(1, 60)))
        v, ids = schedule(js)
        assert v == brute_force(js)
        sel = sorted([j for j in js if j[0] in ids], key=lambda j: j[1])
        assert all(sel[i][2] <= sel[i + 1][1] for i in range(len(sel) - 1)) and sum(j[3] for j in sel) == v
    print("All 400 instances: DP value equals the exhaustive optimum and the reported set is feasible.")
