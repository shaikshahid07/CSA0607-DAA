"""Task 3 - 0/1 Knapsack by Dynamic Programming with item reconstruction.
Author: Shaik Shahid | Reg No: 192424311 | CSA0607 Design and Analysis of Algorithms
"""
import itertools
import random


def knapsack(items, W):
    """items: list of (id, weight, value). Returns (DP table, best value, chosen ids)."""
    n = len(items)
    DP = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, wi, vi = items[i - 1]
        for w in range(0, W + 1):
            DP[i][w] = DP[i - 1][w]                            # exclude item i
            if wi <= w and DP[i - 1][w - wi] + vi > DP[i][w]:  # include item i
                DP[i][w] = DP[i - 1][w - wi] + vi
    chosen = []
    w = W
    for i in range(n, 0, -1):                                  # reconstruction
        if DP[i][w] != DP[i - 1][w]:
            chosen.append(items[i - 1][0])
            w -= items[i - 1][1]
    chosen.reverse()
    return DP, DP[n][W], chosen


def brute_force(items, W):
    best = 0
    for r in range(len(items) + 1):
        for sub in itertools.combinations(items, r):
            if sum(s[1] for s in sub) <= W:
                best = max(best, sum(s[2] for s in sub))
    return best


def print_table(DP, items, W):
    print("DP table: rows i = 0..n (items considered), columns w = 0..W")
    print(" " * 12 + "".join(f"w={w:<3}" for w in range(W + 1)))
    for i, row in enumerate(DP):
        label = "i=0 (none)" if i == 0 else f"i={i} ({items[i-1][0]})"
        print(f"{label:<12}" + "".join(f"{v:<4}" for v in row))


if __name__ == "__main__":
    items = [("P", 2, 12), ("Q", 3, 20), ("R", 4, 25), ("S", 5, 30)]
    W = 7
    DP, best, chosen = knapsack(items, W)
    print_table(DP, items, W)
    print("\nOptimum value :", best)
    print("Items chosen  :", chosen, "| total weight =", sum(i[1] for i in items if i[0] in chosen))
    assert best == 45 == brute_force(items, W)

    print("\n=== Edge cases ===")
    print("Capacity 0            :", knapsack(items, 0)[1:])
    print("Capacity 1 (none fit) :", knapsack(items, 1)[1:])
    print("Capacity 14 (all fit) :", knapsack(items, 14)[1:])

    print("\n=== Random validation against brute force (300 instances) ===")
    random.seed(11)
    for _ in range(300):
        n = random.randint(1, 7)
        its = [(f"I{i}", random.randint(1, 8), random.randint(1, 40)) for i in range(n)]
        cap = random.randint(0, 20)
        _, val, ch = knapsack(its, cap)
        assert val == brute_force(its, cap)
        assert sum(i[2] for i in its if i[0] in ch) == val and sum(i[1] for i in its if i[0] in ch) <= cap
    print("All 300 random instances matched; reconstructed sets are feasible and optimal.")
