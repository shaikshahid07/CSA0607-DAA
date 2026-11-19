"""Task 3 - 0/1 Knapsack by Dynamic Programming with reconstruction."""
import random
import time


def knapsack(items, W, verbose=True):
    """items: list of (id, weight, value). Returns (best, chosen_ids, table)."""
    n = len(items)
    DP = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, wt, val = items[i - 1]
        for w in range(0, W + 1):
            if wt > w:
                DP[i][w] = DP[i - 1][w]
            else:
                DP[i][w] = max(DP[i - 1][w], DP[i - 1][w - wt] + val)
    # reconstruction
    chosen = []
    w = W
    for i in range(n, 0, -1):
        if DP[i][w] != DP[i - 1][w]:
            chosen.append(items[i - 1][0])
            w -= items[i - 1][1]
    chosen.reverse()
    if verbose:
        print("  DP table (rows = items considered, columns = capacity 0..%d):" % W)
        print("        " + " ".join(f"{c:>3}" for c in range(W + 1)))
        for i in range(n + 1):
            label = "none" if i == 0 else items[i - 1][0]
            print(f"  {label:>4}  " + " ".join(f"{DP[i][c]:>3}" for c in range(W + 1)))
    return DP[n][W], chosen, DP


def brute(items, W):
    best = 0
    for mask in range(1 << len(items)):
        wt = sum(items[i][1] for i in range(len(items)) if mask >> i & 1)
        if wt <= W:
            best = max(best, sum(items[i][2] for i in range(len(items)) if mask >> i & 1))
    return best


def main():
    print("=== TASK 3: 0/1 Knapsack (Dynamic Programming) ===")
    items = [("P", 2, 12), ("Q", 3, 20), ("R", 4, 25), ("S", 5, 30)]
    print("\n[Given instance] capacity = 7")
    best, chosen, _ = knapsack(items, 7)
    wt = sum(i[1] for i in items if i[0] in chosen)
    print(f"  OPTIMUM VALUE = {best}; ITEMS = {chosen}; total weight = {wt}")
    print("  Brute-force optimum =", brute(items, 7))

    print("\n[Boundary: capacity 0]")
    print("  ->", knapsack(items, 0, verbose=False)[:2])
    print("[Boundary: capacity smaller than every item (1)]")
    print("  ->", knapsack(items, 1, verbose=False)[:2])
    print("[Boundary: capacity large enough for all (14)]")
    print("  ->", knapsack(items, 14, verbose=False)[:2])
    print("[Boundary: no items]")
    print("  ->", knapsack([], 5, verbose=False)[:2])

    print("\n[Why greedy by ratio fails for 0/1 (comparison)]")
    t = [("A", 10, 60), ("B", 20, 100), ("C", 30, 120)]
    cap = 50
    order = sorted(t, key=lambda x: x[2] / x[1], reverse=True)
    rem, gv, gi = cap, 0, []
    for iid, wt, val in order:
        if wt <= rem:
            rem -= wt
            gv += val
            gi.append(iid)
    best, ch, _ = knapsack(t, cap, verbose=False)
    print("  items", t, "capacity", cap)
    print("  Ratio-greedy (no fractions):", gv, gi)
    print("  DP optimum                 :", best, ch)

    print("\n[Performance: DP vs brute force]")
    random.seed(5)
    for n in (10, 14, 16):
        it = [(f"I{i}", random.randint(1, 20), random.randint(1, 100)) for i in range(n)]
        W = 40
        t0 = time.perf_counter()
        d = knapsack(it, W, verbose=False)[0]
        t1 = time.perf_counter()
        b = brute(it, W)
        t2 = time.perf_counter()
        print(f"  n={n:>2}, W={W}: DP={1000*(t1-t0):8.3f} ms  brute force={1000*(t2-t1):10.1f} ms  match={d == b}")
    for n, W in ((100, 1000), (200, 2000)):
        it = [(f"I{i}", random.randint(1, 50), random.randint(1, 100)) for i in range(n)]
        t0 = time.perf_counter()
        knapsack(it, W, verbose=False)
        print(f"  n={n}, W={W}: DP only = {1000*(time.perf_counter()-t0):.1f} ms ({n*W} table cells)")

    print("\n[Random validation against brute force, 200 cases]")
    ok = 0
    for _ in range(200):
        m = random.randint(0, 10)
        it = [(f"I{i}", random.randint(1, 8), random.randint(0, 40)) for i in range(m)]
        Wr = random.randint(0, 25)
        if knapsack(it, Wr, verbose=False)[0] == brute(it, Wr):
            ok += 1
    print(f"  Matches: {ok}/200")


if __name__ == "__main__":
    main()
