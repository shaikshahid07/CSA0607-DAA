"""Task 6 - Energy-aware scheduling = Weighted Interval Scheduling (DP + binary search)."""
import bisect
import itertools
import random
import time


def weighted_interval(jobs, verbose=True):
    """jobs: list of (id, start, finish, value). Returns (best, selected_ids)."""
    jobs = sorted(jobs, key=lambda j: j[2])          # sort by finish time
    n = len(jobs)
    finishes = [j[2] for j in jobs]
    # p[i] = number of jobs (1-based count) compatible and finishing <= start of job i
    p = [0] * (n + 1)
    for i in range(1, n + 1):
        p[i] = bisect.bisect_right(finishes, jobs[i - 1][1], 0, i - 1)
    OPT = [0] * (n + 1)
    take = [False] * (n + 1)
    for i in range(1, n + 1):
        incl = jobs[i - 1][3] + OPT[p[i]]
        excl = OPT[i - 1]
        if incl > excl:
            OPT[i] = incl
            take[i] = True
        else:
            OPT[i] = excl
        if verbose:
            print(f"  i={i} {jobs[i-1][0]} [{jobs[i-1][1]},{jobs[i-1][2]}) v={jobs[i-1][3]}: "
                  f"p={p[i]}  include={incl}  exclude={excl}  OPT[{i}]={OPT[i]}")
    sel = []
    i = n
    while i > 0:
        if take[i]:
            sel.append(jobs[i - 1][0])
            i = p[i]
        else:
            i -= 1
    sel.reverse()
    return OPT[n], sel


def brute(jobs):
    best = 0
    for r in range(len(jobs) + 1):
        for sub in itertools.combinations(jobs, r):
            s = sorted(sub, key=lambda j: j[1])
            if all(s[k][2] <= s[k + 1][1] for k in range(len(s) - 1)):
                best = max(best, sum(j[3] for j in s))
    return best


# --- greedy alternatives, used only to show they fail ---
def greedy(jobs, key):
    chosen = []
    for j in sorted(jobs, key=key):
        if all(j[2] <= c[1] or j[1] >= c[2] for c in chosen):
            chosen.append(j)
    return sum(j[3] for j in chosen), [j[0] for j in chosen]


def main():
    print("=== TASK 6: Energy-aware job scheduling ===")
    jobs = [("J1", 1, 3, 20), ("J2", 2, 5, 50), ("J3", 4, 6, 30), ("J4", 6, 8, 40),
            ("J5", 5, 9, 60), ("J6", 8, 10, 30), ("J7", 9, 11, 50), ("J8", 11, 13, 40)]
    print("\n[Given dataset: DP trace]")
    best, sel = weighted_interval(jobs)
    print("  SELECTED JOBS =", sel, " MAX TOTAL ENERGY SAVING =", best)
    print("  Brute-force optimum =", brute(jobs))

    print("\n[Greedy alternatives on the given dataset]")
    print("  Earliest finish :", greedy(jobs, key=lambda j: (j[2], -j[3])))
    print("  Highest value   :", greedy(jobs, key=lambda j: -j[3]))
    print("  Shortest job    :", greedy(jobs, key=lambda j: j[2] - j[1]))

    print("\n[Adversarial set (9 jobs) built to break greedy rules]")
    adv = [("K1", 0, 2, 5), ("K2", 1, 9, 100), ("K3", 2, 4, 5), ("K4", 4, 6, 5),
           ("K5", 6, 8, 5), ("A1", 20, 30, 100), ("A2", 20, 23, 40),
           ("A3", 23, 26, 40), ("A4", 26, 30, 40)]
    print("  Earliest finish :", greedy(adv, key=lambda j: (j[2], -j[3])))
    print("  Highest value   :", greedy(adv, key=lambda j: -j[3]))
    print("  Shortest job    :", greedy(adv, key=lambda j: j[2] - j[1]))
    print("  DP trace:")
    b, s = weighted_interval(adv, verbose=True)
    print("  DP result:", b, s, "| brute force:", brute(adv))

    print("\n[Boundary tests]")
    print("  No jobs        :", weighted_interval([], verbose=False))
    print("  One job        :", weighted_interval([("X", 1, 2, 5)], verbose=False))
    print("  Touching jobs  :", weighted_interval([("X", 1, 2, 5), ("Y", 2, 3, 5)], verbose=False))
    print("  Identical times:", weighted_interval([("X", 1, 4, 5), ("Y", 1, 4, 9)], verbose=False))
    print("  Zero-value job :", weighted_interval([("X", 1, 2, 0), ("Y", 2, 3, 0)], verbose=False))

    print("\n[Random validation against brute force, 300 cases]")
    random.seed(7)
    ok = 0
    for _ in range(300):
        m = random.randint(1, 9)
        js = []
        for k in range(m):
            s0 = random.randint(0, 15)
            js.append((f"R{k}", s0, s0 + random.randint(1, 6), random.randint(1, 50)))
        if weighted_interval(js, verbose=False)[0] == brute(js):
            ok += 1
    print(f"  Matches: {ok}/300")

    print("\n[Performance: DP (O(n log n)) vs brute force (O(2^n))]")
    for n in (10, 14, 18, 20):
        js = []
        for k in range(n):
            s0 = random.randint(0, 40)
            js.append((f"R{k}", s0, s0 + random.randint(1, 6), random.randint(1, 50)))
        t0 = time.perf_counter()
        weighted_interval(js, verbose=False)
        t1 = time.perf_counter()
        brute(js)
        t2 = time.perf_counter()
        print(f"  n={n:>2}: DP={1000*(t1-t0):8.3f} ms   brute force={1000*(t2-t1):10.3f} ms")
    js = [(f"R{k}", random.randint(0, 10**6), 0, random.randint(1, 100)) for k in range(100000)]
    js = [(a, s0, s0 + random.randint(1, 50), v) for a, s0, _, v in js]
    t0 = time.perf_counter()
    weighted_interval(js, verbose=False)
    print(f"  n=100000: DP={1000*(time.perf_counter()-t0):8.1f} ms")


if __name__ == "__main__":
    main()
