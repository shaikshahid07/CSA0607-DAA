"""
Module 1 - Nightly Order Consolidation (KartIQ)
Stable Merge Sort on (timestamp, order_id) records.

Run:  python3 merge_sort.py
Student: Shaik Shahid (192424311)  |  CSA06 CO3 Case Study
"""
import math
import random
import time

comparisons = 0  # global counter of key comparisons


def merge(arr, aux, lo, mid, hi, trace=None):
    """Combine step: merge arr[lo..mid] and arr[mid+1..hi]; stable (<= takes left)."""
    global comparisons
    left = arr[lo:mid + 1]
    right = arr[mid + 1:hi + 1]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i][0] <= right[j][0]:          # '<=' keeps equal keys in arrival order
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]; i += 1; k += 1
    while j < len(right):
        arr[k] = right[j]; j += 1; k += 1
    if trace is not None:
        trace.append((left, right, arr[lo:hi + 1]))


def merge_sort(arr, aux, lo, hi, depth=0, trace=None):
    """Divide -> conquer -> combine."""
    if lo >= hi:                                # base case: 0 or 1 element
        return
    mid = (lo + hi) // 2                        # DIVIDE
    if trace is not None:
        trace.append(("divide", depth, arr[lo:hi + 1], arr[lo:mid + 1], arr[mid + 1:hi + 1]))
    merge_sort(arr, aux, lo, mid, depth + 1, trace)      # CONQUER left
    merge_sort(arr, aux, mid + 1, hi, depth + 1, trace)  # CONQUER right
    merge(arr, aux, lo, mid, hi, trace)                  # COMBINE


def sort_orders(orders, trace=None):
    data = list(orders)
    merge_sort(data, [None] * len(data), 0, len(data) - 1, 0, trace)
    return data


def fmt(lst):
    return "[" + ", ".join(f"({t},{o})" for t, o in lst) + "]"


def demo_trace():
    global comparisons
    orders = [(105, "O1"), (102, "O2"), (105, "O3"), (101, "O4"), (102, "O5"), (103, "O6")]
    print("=" * 70)
    print("MODULE 1 - MERGE SORT TRACE (sample orders)")
    print("=" * 70)
    print("Input  :", fmt(orders))
    trace = []
    comparisons = 0
    result = sort_orders(orders, trace)
    step = 0
    for item in trace:
        if item[0] == "divide":
            _, depth, whole, l, r = item
            print(f"{'  ' * depth}DIVIDE  {fmt(whole)} -> {fmt(l)} | {fmt(r)}")
        else:
            step += 1
            l, r, out = item
            print(f"MERGE #{step}: {fmt(l)} + {fmt(r)} -> {fmt(out)}")
    print("Output :", fmt(result))
    print("Comparisons used:", comparisons)

    # Stability check
    print("\nSTABILITY CHECK (equal timestamps keep arrival order)")
    for ts in sorted({t for t, _ in orders}):
        before = [o for t, o in orders if t == ts]
        after = [o for t, o in result if t == ts]
        print(f"  timestamp {ts}: arrival {before} -> sorted {after}  "
              f"{'OK' if before == after else 'VIOLATED'}")
    assert [t for t, _ in result] == sorted(t for t, _ in orders)
    return result


def theory():
    print("\n" + "=" * 70)
    print("COMPARISON ESTIMATES FOR 10,000,000 ORDERS")
    print("=" * 70)
    n = 10_000_000
    lg = math.log2(n)
    c = math.ceil(lg)
    approx = n * lg
    worst = n * c - 2 ** c + 1
    best = (n * lg) / 2
    print(f"log2(n)                      = {lg:.4f}  (ceil = {c})")
    print(f"n*log2(n)                    = {approx:,.0f}")
    print(f"Worst case  n*ceil(lg n) - 2^ceil(lg n) + 1 = {worst:,}")
    print(f"Best case  ~ (n/2) lg n      = {best:,.0f}")
    print(f"Order records: 16 bytes each -> data = {n * 16 / 1e6:.0f} MB; "
          f"auxiliary buffer = {n * 16 / 1e6:.0f} MB; total ~ {2 * n * 16 / 1e6:.0f} MB")


def verify_recurrence():
    """Measure comparisons for n = 2^k and compare with n lg n - n + 1 (worst case)."""
    global comparisons
    print("\n" + "=" * 70)
    print("RECURRENCE CHECK: measured comparisons vs  n lg n - n + 1")
    print("=" * 70)
    print(f"{'n':>8} {'measured(random)':>18} {'formula n lg n-n+1':>20}")
    for k in range(3, 15, 2):
        n = 2 ** k
        data = [(random.randint(0, 10 ** 6), i) for i in range(n)]
        comparisons = 0
        sort_orders(data)
        print(f"{n:>8} {comparisons:>18,} {n * k - n + 1:>20,}")


def external_merge_demo():
    """Tiny simulation of external merge sort: sort chunks (runs) then k-way merge with a heap."""
    import heapq
    print("\n" + "=" * 70)
    print("EXTERNAL MERGE SORT DEMO (data larger than 'RAM')")
    print("=" * 70)
    random.seed(7)
    n, ram_capacity = 40, 10
    data = [(random.randint(100, 140), f"O{i + 1}") for i in range(n)]
    runs = []
    for s in range(0, n, ram_capacity):                      # pass 1: sort chunks that fit in RAM
        runs.append(sort_orders(data[s:s + ram_capacity]))
    print(f"{n} orders, RAM holds {ram_capacity} -> {len(runs)} sorted runs written to disk")
    # pass 2: k-way merge; heap key (timestamp, run_index) keeps stability across runs
    heap = [(run[0][0], ri, 0) for ri, run in enumerate(runs)]
    heapq.heapify(heap)
    out = []
    while heap:
        ts, ri, pos = heapq.heappop(heap)
        out.append(runs[ri][pos])
        if pos + 1 < len(runs[ri]):
            heapq.heappush(heap, (runs[ri][pos + 1][0], ri, pos + 1))
    ok = [t for t, _ in out] == sorted(t for t, _ in data)
    stable = out == sorted(data, key=lambda x: x[0])        # Python sort is stable -> reference
    print("Merged output sorted:", ok, "| stable vs reference:", stable)
    n_big = 10_000_000
    ram_orders = 1_000_000
    k = math.ceil(n_big / ram_orders)
    print(f"For 10,000,000 orders with 1,000,000 fitting in RAM: {k} runs, one {k}-way merge pass,"
          f" heap of {k} entries -> O(n log k) = {n_big * math.log2(k):,.0f} comparisons")


def timing_experiment(out_csv=None):
    global comparisons
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
    rows = []
    for n in sizes:
        data = [(random.randint(0, 10 ** 6), i) for i in range(n)]
        comparisons = 0
        t0 = time.perf_counter()
        sort_orders(data)
        dt = time.perf_counter() - t0
        rows.append((n, comparisons, dt))
    if out_csv:
        with open(out_csv, "w") as f:
            f.write("n,comparisons,seconds\n")
            for r in rows:
                f.write(f"{r[0]},{r[1]},{r[2]:.6f}\n")
    return rows


if __name__ == "__main__":
    random.seed(1)
    demo_trace()
    theory()
    verify_recurrence()
    external_merge_demo()
    print("\nTIMING (random data)")
    for n, c, t in timing_experiment("../../Supporting_Files/datasets/merge_sort_timing.csv"):
        print(f"n={n:>6}  comparisons={c:>10,}  time={t:.4f}s")
