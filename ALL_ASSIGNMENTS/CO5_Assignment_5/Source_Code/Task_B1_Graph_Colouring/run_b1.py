from graph_colouring import colour_graph, is_valid_colouring


def cycle(n):
    return [(i, (i + 1) % n) for i in range(n)]


def complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def path(n):
    return [(i, i + 1) for i in range(n - 1)]


def petersen():
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return outer + spokes + inner


def groetzsch():
    edges = [(i, (i + 1) % 5) for i in range(5)]
    for i in range(5):
        edges.append((5 + i, (i + 1) % 5))
        edges.append((5 + i, (i + 4) % 5))
        edges.append((5 + i, 10))
    return edges


def clique_last_graph():
    edges = path(10)
    for i in range(10, 14):
        for j in range(i + 1, 14):
            edges.append((i, j))
    return edges


def clique_first_graph():
    edges = complete(4)
    for i in range(4, 13):
        edges.append((i, i + 1))
    return edges


def random_graph(n, edge_count, seed):
    state = seed
    edges = []
    seen = set()
    while len(edges) < edge_count:
        state = (state * 1103515245 + 12345) % 2147483648
        u = (state // 65536) % n
        state = (state * 1103515245 + 12345) % 2147483648
        v = (state // 65536) % n
        if u != v and (min(u, v), max(u, v)) not in seen:
            seen.add((min(u, v), max(u, v)))
            edges.append((u, v))
    return edges


A15_EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)]

tests = [
    ("T1", "Colourable graph: triangle with a tail (5 vertices)", 5, A15_EDGES, 3, True,
     "checks a normal successful search and a valid final colouring"),
    ("T2", "Colourable graph: odd cycle C5 with 3 colours", 5, cycle(5), 3, True,
     "checks an odd cycle needs the third group on its closing service"),
    ("T3", "Not colourable: triangle with a tail using only 2 colours", 5, A15_EDGES, 2, False,
     "checks that failure is reported after every option is exhausted"),
    ("T4", "Not colourable: complete graph K4 with 3 colours", 4, complete(4), 3, False,
     "checks the smallest dense conflict (4 mutual conflicts, 3 groups)"),
    ("T5", "Not colourable: odd cycle C5 with 2 colours", 5, cycle(5), 2, False,
     "checks that odd cycles are rejected when m = 2"),
    ("T6", "Colourable: even cycle C6 with 2 colours", 6, cycle(6), 2, True,
     "checks a bipartite graph is accepted with m = 2"),
    ("T7", "Boundary: single service, 1 group", 1, [], 1, True,
     "smallest non-empty input"),
    ("T8", "Boundary: 6 services with no conflicts, 1 group", 6, [], 1, True,
     "no edges means one group is enough"),
    ("T9", "Boundary: K5 with exactly 5 groups (m = n)", 5, complete(5), 5, True,
     "m equals the chromatic number, the tightest successful case"),
    ("T10", "Boundary: K5 with 4 groups (m = n - 1)", 5, complete(5), 4, False,
     "one group too few must fail"),
    ("T11", "Boundary: empty graph (0 services)", 0, [], 2, True,
     "nothing to assign, trivially successful"),
    ("T12", "Boundary: 3 services but 0 groups", 3, [], 0, False,
     "no colour exists, must fail immediately"),
]

print("B1.1 VALIDATION TESTS (Version 1: input order)")
print("=" * 78)
passed = 0
for tid, title, n, edges, m, expected, purpose in tests:
    found, colour, stats, order = colour_graph(n, edges, m, "input")
    valid = True
    if found:
        valid = is_valid_colouring(n, edges, m, colour)
    ok = (found == expected) and valid
    if ok:
        passed += 1
    print(tid + "  " + title)
    print("    verifies : " + purpose)
    print("    n=" + str(n) + "  m=" + str(m) + "  conflicts=" + str(len(edges)))
    print("    expected : " + ("COLOURABLE" if expected else "NOT COLOURABLE") +
          "   actual : " + ("COLOURABLE" if found else "NOT COLOURABLE") +
          "   -> " + ("PASS" if ok else "FAIL"))
    if found:
        print("    colouring: " + str(colour))
    print("    nodes=" + str(stats["nodes"]) + " attempts=" + str(stats["attempts"]) +
          " rejected=" + str(stats["rejected"]) + " backtracks=" + str(stats["backtracks"]) +
          " max_depth=" + str(stats["max_depth"]))
print("-" * 78)
print("Tests passed: " + str(passed) + " / " + str(len(tests)))
print()

graphs = [
    ("G1 Triangle+tail, m=2", 5, A15_EDGES, 2),
    ("G2 Petersen graph, m=3", 10, petersen(), 3),
    ("G3 Groetzsch graph, m=3", 11, groetzsch(), 3),
    ("G4 Path(10)+K4 last, m=3", 14, clique_last_graph(), 3),
    ("G5 K4 first + path(10), m=3", 14, clique_first_graph(), 3),
    ("G6 Random 14v/30e seed 7, m=3", 14, random_graph(14, 30, 7), 3),
    ("G7 Random 16v/40e seed 11, m=3", 16, random_graph(16, 40, 11), 3),
]

print("B1.3 / B1.4 SEARCH ORDER COMPARISON")
print("Version 1 = input order | Version 2 = most-connected-to-placed first")
print("=" * 78)
total1 = 0
total2 = 0
for name, n, edges, m in graphs:
    f1, c1, s1, o1 = colour_graph(n, edges, m, "input")
    f2, c2, s2, o2 = colour_graph(n, edges, m, "heuristic")
    total1 += s1["nodes"]
    total2 += s2["nodes"]
    print(name + "  (answer: " + ("colourable" if f1 else "not colourable") + ")")
    if f1 != f2:
        print("    WARNING: versions disagree")
    print("    " + "measure".ljust(24) + "Version 1".rjust(12) + "Version 2".rjust(12))
    print("    " + "Search nodes".ljust(24) + str(s1["nodes"]).rjust(12) + str(s2["nodes"]).rjust(12))
    print("    " + "Candidate assignments".ljust(24) + str(s1["attempts"]).rjust(12) + str(s2["attempts"]).rjust(12))
    print("    " + "Rejected branches".ljust(24) + str(s1["rejected"]).rjust(12) + str(s2["rejected"]).rjust(12))
    print("    " + "Backtracks".ljust(24) + str(s1["backtracks"]).rjust(12) + str(s2["backtracks"]).rjust(12))
    print("    " + "Max depth".ljust(24) + str(s1["max_depth"]).rjust(12) + str(s2["max_depth"]).rjust(12))
print("-" * 78)
print("Total search nodes over all graphs: Version 1 = " + str(total1) + ", Version 2 = " + str(total2))
