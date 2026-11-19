"""Task 1 - Repaired load-vehicle algorithm (Fractional Knapsack, greedy by value/weight ratio).
Author: Shaik Shahid | Reg No: 192424311 | CSA0607 Design and Analysis of Algorithms
"""


def fractional_load(packages, capacity):
    """packages: list of (id, weight, value). Returns (fractions dict, total value, steps)."""
    n = len(packages)
    ratio = {}
    x = {}
    for pid, w, v in packages:
        ratio[pid] = v / w
        x[pid] = 0.0
    # SORT in descending order of value/weight ratio (ties broken by package id)
    order = sorted(packages, key=lambda p: (-ratio[p[0]], p[0]))
    remaining = capacity
    total = 0.0
    k = 0
    steps = []
    while k < n and remaining > 0:
        pid, w, v = order[k]
        if w <= remaining:
            x[pid] = 1.0
            remaining -= w
            total += v
            steps.append(f"take {pid} fully (ratio={ratio[pid]:.2f}) remaining={remaining} total={total:g}")
        else:
            x[pid] = remaining / w
            total += v * x[pid]
            steps.append(f"take {pid} fraction {x[pid]:.4f} (ratio={ratio[pid]:.2f}) remaining=0 total={total:g}")
            remaining = 0
        k += 1
    return x, total, steps


def run_case(title, packages, capacity):
    print(f"--- {title} ---")
    print("Packages (id, weight, value):", packages, "| Capacity:", capacity)
    x, total, steps = fractional_load(packages, capacity)
    for s in steps:
        print("  ", s)
    print("Fractions loaded :", {k: round(v, 4) for k, v in x.items()})
    print("Total value      :", round(total, 4))
    print()
    return total


if __name__ == "__main__":
    pk = [("P1", 10, 60), ("P2", 20, 100), ("P3", 30, 120)]
    assert abs(run_case("Test 1: standard instance", pk, 50) - 240) < 1e-9
    assert run_case("Test 2: capacity 0", pk, 0) == 0
    assert abs(run_case("Test 3: capacity larger than total weight", pk, 100) - 280) < 1e-9
    assert abs(run_case("Test 4: single package, partial", [("S", 8, 40)], 4) - 20) < 1e-9
    pk5 = [("A", 5, 10), ("B", 4, 10), ("C", 6, 12), ("D", 3, 9)]
    run_case("Test 5: four packages, capacity 10", pk5, 10)
    # Why the ratio rule matters: highest-value-first gives a worse result on Test 1
    best_value_first = 0
    cap = 50
    for pid, w, v in sorted(pk, key=lambda p: -p[2]):
        take = min(w, cap)
        best_value_first += v * take / w
        cap -= take
    print("Comparison - highest-value-first on Test 1 gives", best_value_first, "< 240 (ratio rule)")
