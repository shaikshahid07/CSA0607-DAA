"""Task 2 - Job Sequencing with Deadlines (greedy by profit)."""
import itertools
import random
import time


def job_sequencing(jobs, verbose=True):
    """jobs: list of (id, deadline, profit). Returns (schedule, total)."""
    max_d = max(d for _, d, _ in jobs)
    slot = [None] * (max_d + 1)  # slots 1..max_d
    order = sorted(jobs, key=lambda j: j[2], reverse=True)
    if verbose:
        print("  Order by profit:", [(j[0], j[2]) for j in order])
    total = 0
    for jid, d, p in order:
        placed = False
        for t in range(min(d, max_d), 0, -1):   # latest free slot <= deadline
            if slot[t] is None:
                slot[t] = jid
                total += p
                placed = True
                if verbose:
                    print(f"  Job {jid} (d={d}, p={p}) -> slot {t}; profit={total}; "
                          f"slots={slot[1:]}")
                break
        if not placed and verbose:
            print(f"  Job {jid} (d={d}, p={p}) rejected: no free slot <= {d}")
    return slot[1:], total


def brute_force(jobs):
    best = 0
    n = len(jobs)
    for r in range(n + 1):
        for subset in itertools.combinations(jobs, r):
            ok = True
            by_d = sorted(subset, key=lambda j: j[1])
            for i, (_, d, _) in enumerate(by_d, start=1):
                if i > d:
                    ok = False
                    break
            if ok:
                best = max(best, sum(j[2] for j in subset))
    return best


def main():
    print("=== TASK 2: Job Sequencing with Deadlines ===")
    given = [("A", 2, 80), ("B", 1, 35), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
    print("\n[Given instance]")
    sched, total = job_sequencing(given)
    print("  FINAL SCHEDULE:", sched, " TOTAL PROFIT =", total)
    print("  Brute-force optimum =", brute_force(given))

    print("\n[Modified instance: B profit 35 -> 90]")
    mod = [("A", 2, 80), ("B", 1, 90), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
    sched, total = job_sequencing(mod)
    print("  FINAL SCHEDULE:", sched, " TOTAL PROFIT =", total)
    print("  Brute-force optimum =", brute_force(mod))

    print("\n[Boundary: single job]")
    sched, total = job_sequencing([("X", 1, 10)])
    print("  FINAL SCHEDULE:", sched, " TOTAL PROFIT =", total)

    print("\n[Boundary: all deadlines = 1]")
    sched, total = job_sequencing([("X", 1, 10), ("Y", 1, 50), ("Z", 1, 30)])
    print("  FINAL SCHEDULE:", sched, " TOTAL PROFIT =", total)

    print("\n[Boundary: deadline larger than job count]")
    jobs = [("X", 10, 10), ("Y", 10, 50)]
    sched, total = job_sequencing(jobs)
    print("  Schedule has", len(sched), "slots; TOTAL PROFIT =", total)

    print("\n[Performance: greedy vs brute force]")
    random.seed(3)
    for n in (8, 12, 16):
        js = [(f"J{i}", random.randint(1, n), random.randint(1, 100)) for i in range(n)]
        t0 = time.perf_counter()
        g = job_sequencing(js, verbose=False)[1]
        t1 = time.perf_counter()
        b = brute_force(js)
        t2 = time.perf_counter()
        print(f"  n={n:>2}: greedy={1000*(t1-t0):8.3f} ms (profit {g})  "
              f"brute force={1000*(t2-t1):10.1f} ms (profit {b})  match={g == b}")
    js = [(f"J{i}", random.randint(1, 2000), random.randint(1, 100)) for i in range(2000)]
    t0 = time.perf_counter()
    job_sequencing(js, verbose=False)
    print(f"  n=2000 greedy only: {1000*(time.perf_counter()-t0):.2f} ms")

    print("\n[Random validation against brute force, 200 cases]")
    ok = 0
    for _ in range(200):
        m = random.randint(1, 9)
        js = [(f"J{i}", random.randint(1, 6), random.randint(1, 60)) for i in range(m)]
        if job_sequencing(js, verbose=False)[1] == brute_force(js):
            ok += 1
    print(f"  Matches: {ok}/200")


if __name__ == "__main__":
    main()
