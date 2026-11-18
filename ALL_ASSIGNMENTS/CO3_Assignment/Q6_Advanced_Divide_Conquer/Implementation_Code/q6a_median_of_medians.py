import random
import time

random.seed(2026)

count = 0

def insertion_median(group):
    global count
    g = list(group)
    for i in range(1, len(g)):
        key = g[i]
        j = i - 1
        while j >= 0:
            count += 1
            if g[j] > key:
                g[j + 1] = g[j]
                j -= 1
            else:
                break
        g[j + 1] = key
    return g[len(g) // 2]

def mom_select(a, k):
    global count
    if len(a) <= 5:
        return sorted(a)[k - 1]
    medians = []
    for i in range(0, len(a), 5):
        medians.append(insertion_median(a[i:i + 5]))
    pivot = mom_select(medians, (len(medians) + 1) // 2)
    low = []
    equal = []
    high = []
    for x in a:
        count += 1
        if x < pivot:
            low.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            high.append(x)
    if k <= len(low):
        return mom_select(low, k)
    if k <= len(low) + len(equal):
        return pivot
    return mom_select(high, k - len(low) - len(equal))

def quickselect(a, k, mode):
    global count
    steps = 0
    worst_split = 0
    while True:
        if len(a) == 1:
            return a[0], steps
        if mode == "first":
            pivot = a[0]
        elif mode == "last":
            pivot = a[-1]
        else:
            pivot = random.choice(a)
        low = []
        equal = []
        high = []
        for x in a:
            count += 1
            if x < pivot:
                low.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                high.append(x)
        steps += 1
        if k <= len(low):
            a = low
        elif k <= len(low) + len(equal):
            return pivot, steps
        else:
            k = k - len(low) - len(equal)
            a = high

print("=" * 72)
print("Q6 (A) : MEDIAN OF MEDIANS VS QUICKSELECT  (k-th smallest element)")
print("=" * 72)

demo = [12, 3, 5, 7, 4, 19, 26, 1, 15, 9, 21, 8, 30, 2, 17]
print("Demo list :", demo)
print("Sorted    :", sorted(demo))
for k in [1, 4, 8, 15]:
    print("k = %-3d  median-of-medians = %-3d  sorted[k-1] = %d" % (k, mom_select(demo, k), sorted(demo)[k - 1]))
print()

print("Experiment 1 : correctness on 300 random lists with random k")
bad = 0
for i in range(300):
    n = random.randint(1, 400)
    data = [random.randint(1, 100) for j in range(n)]
    k = random.randint(1, n)
    if mom_select(data, k) != sorted(data)[k - 1]:
        bad += 1
print("Wrong answers :", bad)
print()

print("Experiment 2 : grouping strategy and pivot for a list of 25 numbers")
data = random.sample(range(1, 100), 25)
print("List    :", data)
groups = []
for i in range(0, 25, 5):
    groups.append(sorted(data[i:i + 5]))
medians = [g[2] for g in groups]
print("Groups (each sorted) :")
for g in groups:
    print("   ", g, " median =", g[2])
print("Medians :", medians, " median of medians (pivot) =", sorted(medians)[2])
pivot = sorted(medians)[2]
smaller = len([x for x in data if x < pivot])
print("Elements smaller than pivot :", smaller, " larger :", len([x for x in data if x > pivot]))
print("Guarantee : at least 3n/10 = 7.5 elements on each side")
print()

print("Experiment 3 : comparisons on SORTED input, finding the median (k = n/2)")
print("%-8s %-14s %-14s %-14s %-14s" % ("n", "QS first", "QS random", "Median-of-med", "n^2/2"))
rows = []
for n in [500, 1000, 2000, 4000, 8000]:
    data = list(range(1, n + 1))
    k = n // 2
    count = 0
    r1, s1 = quickselect(data, k, "first")
    c_first = count
    count = 0
    r2, s2 = quickselect(data, k, "random")
    c_rand = count
    count = 0
    r3 = mom_select(data, k)
    c_mom = count
    print("%-8d %-14d %-14d %-14d %-14d  %s" % (n, c_first, c_rand, c_mom, n * n // 2, r1 == r2 == r3 == k))
    rows.append((n, c_first, c_rand, c_mom))
print()

print("Experiment 4 : steps (partition rounds) on sorted input, n = 8000, k = n/2")
data = list(range(1, 8001))
for mode in ["first", "last", "random"]:
    r, steps = quickselect(data, 4000, mode)
    print("%-8s pivot : %d rounds" % (mode, steps))
print()

print("Experiment 5 : randomised pivot is not perfect - 500 runs, n = 4000, sorted input, k = n/2")
data = list(range(1, 4001))
results = []
for i in range(500):
    count = 0
    quickselect(data, 2000, "random")
    results.append(count)
results.sort()
print("Best    :", results[0])
print("Average :", round(sum(results) / len(results)))
print("Median  :", results[len(results) // 2])
print("Worst   :", results[-1])
print("Linear guarantee of median-of-medians (cost, fixed every time) :", end=" ")
count = 0
mom_select(data, 2000)
print(count)
print("Deterministic first-pivot cost (n^2/2 = 8,000,000)            :", end=" ")
count = 0
quickselect(data, 2000, "first")
print(count)
print()

print("Experiment 6 : random data, timing in seconds (k = n/2, average of 5 runs)")
print("%-8s %-14s %-14s %-14s" % ("n", "QS random", "Median-of-med", "sorted()"))
for n in [1000, 10000, 50000, 100000]:
    t1 = 0
    t2 = 0
    t3 = 0
    for r in range(5):
        data = random.sample(range(10 * n), n)
        start = time.perf_counter()
        quickselect(data, n // 2, "random")
        t1 += time.perf_counter() - start
        start = time.perf_counter()
        mom_select(data, n // 2)
        t2 += time.perf_counter() - start
        start = time.perf_counter()
        sorted(data)[n // 2 - 1]
        t3 += time.perf_counter() - start
    print("%-8d %-14.5f %-14.5f %-14.5f" % (n, t1 / 5, t2 / 5, t3 / 5))
