"""Q1 - Selection, Bubble and Insertion sort under different data conditions.
Counts key comparisons and data movements (swaps / shifts). Run:  python q1_sorting.py
"""
import random, time, json, csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def selection_sort(a):
    a = a[:]; n = len(a); comps = moves = 0
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]; moves += 1
    return a, comps, moves


def bubble_sort(a):
    a = a[:]; n = len(a); comps = moves = 0
    for p in range(n - 1):
        swapped = False
        for j in range(n - 1 - p):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]; moves += 1; swapped = True
        if not swapped:
            break
    return a, comps, moves


def insertion_sort(a):
    a = a[:]; n = len(a); comps = moves = 0
    for i in range(1, n):
        key = a[i]; j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]; moves += 1; j -= 1
            else:
                break
        a[j + 1] = key
    return a, comps, moves


ALGOS = {"Selection": selection_sort, "Bubble": bubble_sort, "Insertion": insertion_sort}


def inversions(a):
    # O(n^2) is fine for n<=2000; used only to relate moves to inversions
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def make_datasets(n, seed=42):
    rnd = random.Random(seed)
    scores = rnd.sample(range(1, 10 * n), n)
    d1 = scores[:]                                   # D1 random
    k = n // 20                                      # 5% new orders
    old = sorted(scores[: n - k]); new = scores[n - k:]
    d2 = old + new                                   # D2 95% already in order, new batch at the end
    d3 = sorted(scores, reverse=True)                # D3 reverse sorted (edge/worst)
    return {"D1 Random": d1, "D2 Nearly sorted (95%)": d2, "D3 Reverse sorted": d3,
            "Extra: Already sorted": sorted(scores), "Extra: All equal": [7] * n}


def run(n):
    rows = []
    for dname, data in make_datasets(n).items():
        inv = inversions(data)
        for aname, f in ALGOS.items():
            t0 = time.perf_counter(); out, c, m = f(data); t = time.perf_counter() - t0
            assert out == sorted(data)
            rows.append(dict(n=n, dataset=dname, algorithm=aname, inversions=inv,
                             comparisons=c, movements=m, time_ms=round(t * 1000, 3)))
    return rows


if __name__ == "__main__":
    N = 1000
    print(f"=== Q1: sorting comparison, n = {N} ===")
    rows = run(N)
    print(f"{'Dataset':<26}{'Algorithm':<11}{'Inversions':>11}{'Comparisons':>13}{'Movements':>11}{'Time(ms)':>10}")
    for r in rows:
        print(f"{r['dataset']:<26}{r['algorithm']:<11}{r['inversions']:>11}{r['comparisons']:>13}{r['movements']:>11}{r['time_ms']:>10}")
    print("\nTheory reference (n=%d): n(n-1)/2 = %d" % (N, N * (N - 1) // 2))

    # scaling on the 95%-sorted workload
    scale = []
    for n in (250, 500, 1000, 2000):
        for r in run(n):
            if r["dataset"].startswith("D2"):
                scale.append(r)
    print("\n=== Scaling on D2 (95% already sorted, 5% new batch appended) ===")
    print(f"{'n':>6}{'Algorithm':>11}{'Comparisons':>13}{'Movements':>11}{'Time(ms)':>10}")
    for r in scale:
        print(f"{r['n']:>6}{r['algorithm']:>11}{r['comparisons']:>13}{r['movements']:>11}{r['time_ms']:>10}")

    # sensitivity: fraction of new orders appended
    print("\n=== Sensitivity: size of the new batch (n=1000) ===")
    print(f"{'new %':>6}{'Selection':>11}{'Bubble':>9}{'Insertion':>11}   (comparisons)")
    sens = []
    for pct in (0, 1, 5, 10, 25, 50, 100):
        rnd = random.Random(5); n = 1000; k = n * pct // 100
        sc = rnd.sample(range(1, 10 * n), n)
        data = sorted(sc[: n - k]) + sc[n - k:]
        cs = {nm: f(data)[1] for nm, f in ALGOS.items()}
        sens.append((pct, cs))
        print(f"{pct:>6}{cs['Selection']:>11}{cs['Bubble']:>9}{cs['Insertion']:>11}")

    with open(os.path.join(RES, "q1_raw.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows + scale)
    json.dump({"rows": rows, "scale": scale, "sens": sens}, open(os.path.join(RES, "q1_raw.json"), "w"), indent=1)

    # graphs
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ds = ["D1 Random", "D2 Nearly sorted (95%)", "D3 Reverse sorted"]
    for i, aname in enumerate(ALGOS):
        ax[0].bar([x + i * 0.27 for x in range(3)],
                  [next(r["comparisons"] for r in rows if r["dataset"] == d and r["algorithm"] == aname) for d in ds],
                  0.27, label=aname)
    ax[0].set_xticks([0.27, 1.27, 2.27]); ax[0].set_xticklabels(["Random", "95% sorted", "Reverse"])
    ax[0].set_ylabel("Comparisons"); ax[0].set_title(f"Comparisons by dataset (n={N})"); ax[0].legend()
    for aname in ALGOS:
        ax[1].plot([r["n"] for r in scale if r["algorithm"] == aname],
                   [r["comparisons"] for r in scale if r["algorithm"] == aname], "o-", label=aname)
    ax[1].set_yscale("log"); ax[1].set_xlabel("n"); ax[1].set_ylabel("Comparisons (log)")
    ax[1].set_title("Scaling on 95%-sorted input"); ax[1].legend()
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q1_graphs.png"), dpi=130)
