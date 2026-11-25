from graph_colouring import colour_graph, is_valid_colouring


def path_edges(count, start=0):
    return [(start + i, start + i + 1) for i in range(count - 1)]


def clique_edges(first, size):
    edges = []
    for i in range(first, first + size):
        for j in range(i + 1, first + size):
            edges.append((i, j))
    return edges


def make_graph_a(n):
    path_length = n - 4
    edges = path_edges(path_length)
    base = path_length
    edges += [(base, base + 1), (base, base + 2), (base + 1, base + 2), (base + 1, base + 3), (base + 2, base + 3)]
    edges.append((path_length - 1, base))
    return edges


def make_graph_b(n):
    path_length = n - 4
    edges = path_edges(path_length)
    edges += clique_edges(path_length, 4)
    return edges


def show(title, n, edges, m):
    print(title)
    print("    vertices=" + str(n) + "  conflicts=" + str(len(edges)) + "  m=" + str(m))


def run_both(n, edges, m):
    f1, c1, s1, o1 = colour_graph(n, edges, m, "input")
    f2, c2, s2, o2 = colour_graph(n, edges, m, "heuristic")
    return (f1, c1, s1), (f2, c2, s2)


N = 14
M = 3
graph_a = make_graph_a(N)
graph_b = make_graph_b(N)

print("B2 ADVERSARIAL INPUT - same size, very different search")
print("=" * 78)
show("Graph A: path of 10 services + a 4-service 'diamond' joined at one end", N, graph_a, M)
show("Graph B: path of 10 services + a separate K4 (4 mutually conflicting services)", N, graph_b, M)
print()
print("PREDICTION (written before running)")
print("  1. Graph B will need far more search than Graph A.")
print("  2. Graph A: almost no unsuccessful branches; each service has a free colour.")
print("  3. Graph B: failures arise only at the LAST four services (the K4), because the")
print("     K4 needs 4 colours but m = 3. They appear only after the path is fully coloured.")
print("  4. Pruning is early for Graph A (no dead ends) but LATE for Graph B: the conflict")
print("     is hidden behind 10 free path decisions, so every path colouring is tried.")
print()

(fa, ca, sa), (fa2, ca2, sa2) = run_both(N, graph_a, M)
(fb, cb, sb), (fb2, cb2, sb2) = run_both(N, graph_b, M)

print("RESULTS (Version 1, input order)")
print("    " + "measure".ljust(24) + "Graph A".rjust(12) + "Graph B".rjust(12) + "B / A".rjust(10))
for label, key in [("Search nodes", "nodes"), ("Candidate assignments", "attempts"),
                   ("Rejected branches", "rejected"), ("Backtracks", "backtracks"), ("Max depth", "max_depth")]:
    ratio = "-"
    if sa[key] > 0:
        ratio = str(round(sb[key] / sa[key], 1)) + "x"
    print("    " + label.ljust(24) + str(sa[key]).rjust(12) + str(sb[key]).rjust(12) + ratio.rjust(10))
print("    answer: Graph A = " + ("colourable" if fa else "not colourable") +
      " | Graph B = " + ("colourable" if fb else "not colourable"))
if fa:
    print("    Graph A colouring valid: " + str(is_valid_colouring(N, graph_a, M, ca)))
print()

print("EXTRA: Graph B with Version 2 ordering (most-connected-to-placed first)")
print("    nodes=" + str(sb2["nodes"]) + " backtracks=" + str(sb2["backtracks"]) +
      " rejected=" + str(sb2["rejected"]) + " max_depth=" + str(sb2["max_depth"]))
print()

print("GROWTH: same family, increasing size, m = 3 (Version 1)")
print("    " + "n".rjust(4) + "A nodes".rjust(12) + "B nodes".rjust(14) + "B backtracks".rjust(16) + "B nodes / previous".rjust(22))
previous = None
for n in [8, 10, 12, 14, 16, 18]:
    ga = make_graph_a(n)
    gb = make_graph_b(n)
    ra, rb = run_both(n, ga, M)[0], run_both(n, gb, M)[0]
    growth = "-"
    if previous is not None:
        growth = str(round(rb[2]["nodes"] / previous, 2)) + "x"
    previous = rb[2]["nodes"]
    print("    " + str(n).rjust(4) + str(ra[2]["nodes"]).rjust(12) + str(rb[2]["nodes"]).rjust(14) +
          str(rb[2]["backtracks"]).rjust(16) + growth.rjust(22))
