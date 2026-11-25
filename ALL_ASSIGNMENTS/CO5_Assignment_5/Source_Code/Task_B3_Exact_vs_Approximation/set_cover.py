from itertools import combinations
from math import comb
import time


def next_random(state):
    return (state * 1103515245 + 12345) % 2147483648


def make_instance(zones, centres, seed, percent):
    state = seed
    sets = []
    for j in range(centres):
        chosen = set()
        for z in range(1, zones + 1):
            state = next_random(state)
            if (state // 65536) % 100 < percent:
                chosen.add(z)
        sets.append(chosen)
    for z in range(1, zones + 1):
        covered = False
        for s in sets:
            if z in s:
                covered = True
        if not covered:
            state = next_random(state)
            sets[(state // 65536) % centres].add(z)
    return set(range(1, zones + 1)), sets


def exact_cover(universe, sets, stats):
    stats["combinations"] = 0
    for size in range(1, len(sets) + 1):
        for combo in combinations(range(len(sets)), size):
            stats["combinations"] += 1
            covered = set()
            for j in combo:
                covered = covered | sets[j]
            if covered == universe:
                return list(combo)
    return None


def greedy_cover(universe, sets, stats, verbose=False):
    stats["evaluations"] = 0
    stats["rounds"] = 0
    uncovered = set(universe)
    selected = []
    while len(uncovered) > 0:
        best = -1
        best_gain = 0
        for j in range(len(sets)):
            gain = len(sets[j] & uncovered)
            stats["evaluations"] += 1
            if verbose:
                print("        C" + str(j + 1) + " would newly cover " + str(gain) + " zone(s)")
            if gain > best_gain:
                best_gain = gain
                best = j
        if best_gain == 0:
            return None
        selected.append(best)
        uncovered = uncovered - sets[best]
        stats["rounds"] += 1
        if verbose:
            print("      -> choose C" + str(best + 1) + " (gain " + str(best_gain) + "), uncovered now " + str(sorted(uncovered)))
    return selected


def label(indexes):
    return "{" + ", ".join("C" + str(j + 1) for j in indexes) + "}"


def is_cover(universe, sets, chosen):
    covered = set()
    for j in chosen:
        covered = covered | sets[j]
    return covered == universe


print("B3 EXACT vs APPROXIMATE - emergency service set cover")
print("=" * 78)

print("B3.1 CORRECTNESS ON SMALL INSTANCES")
instances = []
u1 = set(range(1, 9))
s1 = [{1, 2, 3}, {4, 5, 6}, {7, 8}, {1, 4, 7}, {2, 5, 8}, {3, 6}]
instances.append(("1 (hand-made, 8 zones, 6 centres)", u1, s1))
u2, s2 = make_instance(12, 8, 5, 30)
instances.append(("2 (random seed 5, 12 zones, 8 centres)", u2, s2))
u3, s3 = make_instance(15, 10, 21, 25)
instances.append(("3 (random seed 21, 15 zones, 10 centres)", u3, s3))
print("    " + "Instance".ljust(44) + "Exact".rjust(6) + "Greedy".rjust(8) + "Same?".rjust(7))
for name, u, s in instances:
    e_stats = {}
    g_stats = {}
    e = exact_cover(u, s, e_stats)
    g = greedy_cover(u, s, g_stats)
    same = "YES" if len(e) == len(g) else "NO"
    print("    " + name.ljust(44) + str(len(e)).rjust(6) + str(len(g)).rjust(8) + same.rjust(7))
    print("        exact  = " + label(e) + "  (" + str(e_stats["combinations"]) + " combinations examined)")
    print("        greedy = " + label(g) + "  (" + str(g_stats["evaluations"]) + " gain evaluations)")
    print("        both valid covers: " + str(is_cover(u, s, e) and is_cover(u, s, g)))

differ = 0
worst_gap = 0
trials = 300
for seed in range(1, trials + 1):
    u, s = make_instance(14, 10, seed * 7 + 3, 25)
    e = exact_cover(u, s, {})
    g = greedy_cover(u, s, {})
    if len(g) > len(e):
        differ += 1
        if len(g) - len(e) > worst_gap:
            worst_gap = len(g) - len(e)
print("    Extra check: " + str(trials) + " random instances (14 zones, 10 centres):")
print("        greedy matched the optimum in " + str(trials - differ) + ", was worse in " + str(differ) +
      " (largest gap = " + str(worst_gap) + " centre)")
print()

print("B3.2 COUNTEREXAMPLE FOR GREEDY")
uc = set(range(1, 7))
sc = [{1, 2, 4, 5}, {1, 2, 3}, {4, 5, 6}]
for j in range(3):
    print("    C" + str(j + 1) + " covers " + str(sorted(sc[j])))
print("    Greedy trace:")
gs = {}
gc = greedy_cover(uc, sc, gs, verbose=True)
es = {}
ec = exact_cover(uc, sc, es)
print("    GreedyCoverSize = " + str(len(gc)) + " " + label(gc))
print("    OptimalCoverSize = " + str(len(ec)) + " " + label(ec))
print("    GreedyCoverSize > OptimalCoverSize : " + str(len(gc) > len(ec)))
print()

print("B3.3 INCREASING THE PROBLEM SIZE (random instances, ~15% coverage per centre)")
print("    " + "zones x centres".ljust(16) + "total 2^m".rjust(12) + "exact combos".rjust(14) + "greedy evals".rjust(14) +
      "exact".rjust(7) + "greedy".rjust(8) + "exact ms".rjust(10) + "greedy ms".rjust(11))
sizes = [(10, 8), (14, 12), (18, 16), (22, 20), (26, 24), (30, 27)]
for zones, centres in sizes:
    u, s = make_instance(zones, centres, zones * 13 + centres, 15)
    e_stats = {}
    g_stats = {}
    t0 = time.time()
    e = exact_cover(u, s, e_stats)
    t1 = time.time()
    g = greedy_cover(u, s, g_stats)
    t2 = time.time()
    print("    " + (str(zones) + " x " + str(centres)).ljust(16) + str(2 ** centres).rjust(12) +
          str(e_stats["combinations"]).rjust(14) + str(g_stats["evaluations"]).rjust(14) +
          str(len(e)).rjust(7) + str(len(g)).rjust(8) + str(round((t1 - t0) * 1000, 1)).rjust(10) +
          str(round((t2 - t1) * 1000, 2)).rjust(11))
print()
print("    Greedy only, much larger instances (exact search is not attempted):")
print("    " + "zones x centres".ljust(16) + "greedy evals".rjust(14) + "greedy cover".rjust(14) + "combos exact must rule out".rjust(34))
for zones, centres in [(200, 100), (500, 200), (1000, 400)]:
    u, s = make_instance(zones, centres, zones + centres, 5)
    g_stats = {}
    g = greedy_cover(u, s, g_stats)
    to_rule_out = 0
    for k in range(1, len(g)):
        to_rule_out += comb(centres, k)
    text = str(to_rule_out)
    if len(text) > 12:
        text = text[0] + "." + text[1:3] + "e+" + str(len(text) - 1)
    print("    " + (str(zones) + " x " + str(centres)).ljust(16) + str(g_stats["evaluations"]).rjust(14) +
          str(len(g)).rjust(14) + text.rjust(34))
