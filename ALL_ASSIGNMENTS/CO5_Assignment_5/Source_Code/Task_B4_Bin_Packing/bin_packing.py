import time


def next_random(state):
    return (state * 1103515245 + 12345) % 2147483648


def make_workloads(count, low, high, seed):
    state = seed
    sizes = []
    for i in range(count):
        state = next_random(state)
        sizes.append(low + (state // 65536) % (high - low + 1))
    return sizes


def first_fit_decreasing(sizes, capacity, stats):
    stats["comparisons"] = 0
    order = sorted(range(len(sizes)), key=lambda i: sizes[i], reverse=True)
    loads = []
    members = []
    for i in order:
        placed = False
        for b in range(len(loads)):
            stats["comparisons"] += 1
            if loads[b] + sizes[i] <= capacity:
                loads[b] += sizes[i]
                members[b].append(i)
                placed = True
                break
        if not placed:
            loads.append(sizes[i])
            members.append([i])
    return loads, members


def first_fit(sizes, capacity, stats):
    stats["comparisons"] = 0
    loads = []
    members = []
    for i in range(len(sizes)):
        placed = False
        for b in range(len(loads)):
            stats["comparisons"] += 1
            if loads[b] + sizes[i] <= capacity:
                loads[b] += sizes[i]
                members[b].append(i)
                placed = True
                break
        if not placed:
            loads.append(sizes[i])
            members.append([i])
    return loads, members


def exact_bins(sizes, capacity):
    items = sorted(range(len(sizes)), key=lambda i: sizes[i], reverse=True)
    best = [len(sizes), None]
    loads = []
    members = []

    def place(position):
        if len(loads) >= best[0]:
            return
        if position == len(items):
            best[0] = len(loads)
            best[1] = [list(m) for m in members]
            return
        i = items[position]
        for b in range(len(loads)):
            if loads[b] + sizes[i] <= capacity:
                loads[b] += sizes[i]
                members[b].append(i)
                place(position + 1)
                members[b].pop()
                loads[b] -= sizes[i]
        loads.append(sizes[i])
        members.append([i])
        place(position + 1)
        members.pop()
        loads.pop()

    place(0)
    return best[0], best[1]


def show_allocation(sizes, capacity, loads, members):
    print("    servers used: " + str(len(loads)))
    for b in range(len(loads)):
        parts = ", ".join("W" + str(i + 1) + "=" + str(sizes[i]) for i in members[b])
        print("    Server " + str(b + 1).rjust(2) + " | load " + str(loads[b]).rjust(3) + " | remaining " +
              str(capacity - loads[b]).rjust(3) + " | " + parts)


CAPACITY = 100

print("B4 BIN PACKING - assigning workloads to servers (capacity C = " + str(CAPACITY) + ")")
print("Rule used: First Fit Decreasing (sort by demand, largest first; place each workload")
print("on the first server that still has enough remaining capacity, else open a new server)")
print("=" * 78)

print("B4.1 ALLOCATION OUTPUT - 16 workloads")
sizes = make_workloads(16, 10, 70, 2026)
for start in range(0, len(sizes), 6):
    chunk = range(start, min(start + 6, len(sizes)))
    print("    demands: " + ", ".join("W" + str(i + 1) + "=" + str(sizes[i]) for i in chunk))
stats = {}
loads, members = first_fit_decreasing(sizes, CAPACITY, stats)
show_allocation(sizes, CAPACITY, loads, members)
lower = -(-sum(sizes) // CAPACITY)
print("    total demand = " + str(sum(sizes)) + "  ->  lower bound = ceil(" + str(sum(sizes)) + "/" + str(CAPACITY) + ") = " + str(lower) + " servers")
print("    placement comparisons: " + str(stats["comparisons"]))
checks_ok = True
for b in range(len(loads)):
    if loads[b] > CAPACITY:
        checks_ok = False
assigned = sorted(i for m in members for i in m)
print("    every server within capacity: " + str(checks_ok) + " | every workload placed once: " + str(assigned == list(range(len(sizes)))))
print()

print("B4.2 CHALLENGING THE STRATEGY - input where FFD is not optimal")
hard = [44, 46, 32, 31, 24, 22]
print("    demands: " + ", ".join("W" + str(i + 1) + "=" + str(hard[i]) for i in range(len(hard))))
hs = {}
hl, hm = first_fit_decreasing(hard, CAPACITY, hs)
print("    First Fit Decreasing:")
show_allocation(hard, CAPACITY, hl, hm)
best_count, best_members = exact_bins(hard, CAPACITY)
print("    Exact search (backtracking over all placements):")
best_loads = [sum(hard[i] for i in m) for m in best_members]
show_allocation(hard, CAPACITY, best_loads, best_members)
print("    FFD uses " + str(len(hl)) + " servers, optimum is " + str(best_count) + " -> FFD is not optimal")
print("    Why: FFD packs W2+W1 = 90 first, which leaves 10 free, too small for any other workload.")
print()

nonopt = 0
worst = 0.0
for seed in range(1, 501):
    small = make_workloads(9, 15, 60, seed * 3 + 1)
    l, m = first_fit_decreasing(small, CAPACITY, {})
    opt, _ = exact_bins(small, CAPACITY)
    if len(l) > opt:
        nonopt += 1
    if len(l) / opt > worst:
        worst = len(l) / opt
print("    Extra check: 500 random inputs of 9 workloads, FFD vs exact optimum")
print("        FFD optimal in " + str(500 - nonopt) + " cases, one server worse in " + str(nonopt) + " cases, worst ratio = " + str(round(worst, 2)))
print()

print("B4.3 EVIDENCE FOR THE DECISION NOTE - scale test")
print("    " + "workloads".rjust(10) + "FFD servers".rjust(13) + "lower bound".rjust(13) + "FFD/bound".rjust(11) +
      "FF servers".rjust(12) + "FFD comparisons".rjust(17) + "FFD ms".rjust(9))
for count in [1000, 2000, 5000, 10000]:
    big = make_workloads(count, 5, 60, count + 7)
    fs = {}
    t0 = time.time()
    bl, bm = first_fit_decreasing(big, CAPACITY, fs)
    t1 = time.time()
    ffs = {}
    fl, fm = first_fit(big, CAPACITY, ffs)
    bound = -(-sum(big) // CAPACITY)
    print("    " + str(count).rjust(10) + str(len(bl)).rjust(13) + str(bound).rjust(13) +
          str(round(len(bl) / bound, 3)).rjust(11) + str(len(fl)).rjust(12) +
          str(fs["comparisons"]).rjust(17) + str(round((t1 - t0) * 1000)).rjust(9))
print("    Orderings of just 30 workloads: 30! = " + str(__import__("math").factorial(30)))
