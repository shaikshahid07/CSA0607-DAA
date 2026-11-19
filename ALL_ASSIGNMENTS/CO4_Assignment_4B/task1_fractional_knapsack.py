"""Task 1 - Fractional Knapsack (greedy by value/weight ratio)."""
import random
import time


def load_vehicle(packages, capacity, verbose=True):
    """packages: list of (id, weight, value). Returns (total_value, plan)."""
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    for pid, w, v in packages:
        if w <= 0 or v < 0:
            raise ValueError(f"invalid package {pid}: weight must be > 0, value >= 0")
    # Greedy-choice rule: highest value per unit weight first
    order = sorted(packages, key=lambda p: p[2] / p[1], reverse=True)
    remaining = capacity
    total = 0.0
    plan = []  # (id, fraction, weight_taken, value_gained)
    if verbose:
        print("  Sorted by ratio:", [(p[0], round(p[2] / p[1], 3)) for p in order])
    for pid, w, v in order:
        if remaining <= 0:
            break
        if w <= remaining:
            frac = 1.0
        else:
            frac = remaining / w
        taken = frac * w
        gain = frac * v
        remaining -= taken
        total += gain
        plan.append((pid, frac, taken, gain))
        if verbose:
            print(f"  Take {pid}: fraction={frac:.3f}, weight={taken:.2f}, "
                  f"value={gain:.2f}, remaining capacity={remaining:.2f}")
    return total, plan


def main():
    print("=== TASK 1: Fractional Knapsack (LoadVehicle) ===")
    tests = {
        "Sample": ([("P1", 10, 60), ("P2", 20, 100), ("P3", 30, 120)], 50),
        "Boundary: capacity 0": ([("P1", 10, 60), ("P2", 20, 100)], 0),
        "Boundary: all fit": ([("P1", 5, 10), ("P2", 4, 40)], 100),
        "Single package, partial": ([("P1", 8, 80)], 3),
        "Equal ratios": ([("P1", 2, 4), ("P2", 3, 6), ("P3", 5, 10)], 6),
    }
    for name, (pk, cap) in tests.items():
        print(f"\n[{name}] capacity={cap}")
        total, plan = load_vehicle(pk, cap)
        print(f"  TOTAL VALUE = {total:.2f}")
    print("\n[Failure case: invalid weight]")
    try:
        load_vehicle([("X", 0, 10)], 5)
    except ValueError as e:
        print("  Rejected ->", e)

    print("\n[Performance: greedy O(n log n) on random inputs]")
    random.seed(1)
    for n in (1000, 10000, 100000):
        pk = [(f"P{i}", random.randint(1, 50), random.randint(1, 500)) for i in range(n)]
        t0 = time.perf_counter()
        total, _ = load_vehicle(pk, n * 5, verbose=False)
        print(f"  n={n:>6}: {1000*(time.perf_counter()-t0):9.2f} ms, total value={total:.1f}")


if __name__ == "__main__":
    main()
