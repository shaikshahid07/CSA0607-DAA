"""Task 5 - Dijkstra (greedy), Bellman-Ford (repeated relaxation) and Floyd-Warshall (DP) on one graph.
Author: Shaik Shahid | Reg No: 192424311 | CSA0607 Design and Analysis of Algorithms
"""
import random

INF = float("inf")
V = ["A", "B", "C", "D", "E"]
EDGES = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 6), ("C", "D", 1), ("D", "E", 3), ("C", "E", 8)]


def fmt(x):
    return "INF" if x == INF else f"{x:g}"


def path_to(pred, t):
    p = []
    while t is not None:
        p.append(t)
        t = pred[t]
    return "->".join(reversed(p))


def dijkstra(vertices, edges, src, trace=False, allow_reopen=False):
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    done = {v: False for v in vertices}
    dist[src] = 0
    for _ in vertices:
        cand = [v for v in vertices if not done[v] and dist[v] < INF]
        if not cand:
            break
        u = min(cand, key=lambda v: dist[v])                 # EXTRACT_MIN
        done[u] = True
        if trace:
            print(f"  select {u} (dist={fmt(dist[u])}) -> finalised")
        for a, b, w in edges:
            if a == u and (not done[b] or allow_reopen) and dist[u] + w < dist[b]:
                if trace:
                    print(f"     relax {a}->{b} (w={w}): {fmt(dist[b])} -> {fmt(dist[u] + w)}, pred[{b}]={a}")
                dist[b] = dist[u] + w
                pred[b] = a
    return dist, pred


def bellman_ford(vertices, edges, src, trace=False):
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[src] = 0
    n = len(vertices)
    for rnd in range(1, n):
        changed = False
        for a, b, w in edges:
            if dist[a] < INF and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                pred[b] = a
                changed = True
        if trace:
            print(f"  after pass {rnd}: " + ", ".join(f"{v}={fmt(dist[v])}" for v in vertices))
        if not changed:
            break
    neg_cycle = any(dist[a] < INF and dist[a] + w < dist[b] for a, b, w in edges)   # n-th pass test
    return dist, pred, neg_cycle


def floyd(vertices, edges, trace=False):
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    D = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        D[idx[a]][idx[b]] = min(D[idx[a]][idx[b]], w)
    mats = [[r[:] for r in D]]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
        mats.append([r[:] for r in D])
    return mats


def print_matrix(M, vertices, title):
    print(title)
    print("      " + "".join(f"{v:>5}" for v in vertices))
    for i, v in enumerate(vertices):
        print(f"  {v:<4}" + "".join(f"{fmt(x):>5}" for x in M[i]))


if __name__ == "__main__":
    print("=== 5.1 Dijkstra on the given graph (source A) ===")
    dist, pred = dijkstra(V, EDGES, "A", trace=True)
    for v in V:
        print(f"  dist[{v}] = {fmt(dist[v])}   path: {path_to(pred, v)}")
    assert dist == {"A": 0, "B": 4, "C": 6, "D": 7, "E": 10}

    print("\n=== 5.2 Bellman-Ford on the given graph (source A) ===")
    d2, p2, nc = bellman_ford(V, EDGES, "A", trace=True)
    print("  distances:", {v: fmt(d2[v]) for v in V}, "| negative cycle:", nc)
    assert d2 == dist and not nc

    print("\n=== Extra graph 1: negative edge (no negative cycle) ===")
    V1 = ["A", "B", "C", "D"]
    E1 = [("A", "B", 4), ("A", "C", 5), ("C", "B", -3), ("B", "D", 1)]
    print("  edges:", E1)
    dd, _ = dijkstra(V1, E1, "A")
    print("  Dijkstra (greedy, final-on-extract):", {v: fmt(dd[v]) for v in V1}, " <-- WRONG for B and D")
    bd, bp, bn = bellman_ford(V1, E1, "A", trace=True)
    print("  Bellman-Ford:", {v: fmt(bd[v]) for v in V1}, "| negative cycle:", bn)
    assert bd == {"A": 0, "B": 2, "C": 5, "D": 3} and not bn and dd["D"] == 5

    print("\n=== Extra graph 2: reachable negative cycle B->C->B ===")
    V2 = ["A", "B", "C", "D"]
    E2 = [("A", "B", 1), ("B", "C", -2), ("C", "B", 1), ("C", "D", 2)]
    print("  edges:", E2, "(cycle weight = -2 + 1 = -1)")
    cd, cp, cn = bellman_ford(V2, E2, "A", trace=True)
    print("  Negative cycle detected on the extra pass:", cn)
    assert cn

    print("\n=== 5.3 Floyd-Warshall on the given graph ===")
    mats = floyd(V, EDGES)
    for k, M in enumerate(mats):
        title = "D(0) = direct edges" if k == 0 else f"D({k}) = intermediate vertices allowed up to {V[k-1]}"
        print_matrix(M, V, title)
    for s in V:
        dj, _ = dijkstra(V, EDGES, s)
        for j, t in enumerate(V):
            assert mats[-1][V.index(s)][j] == dj[t]
    print("\nFloyd rows match Dijkstra from every source.")

    print("\n=== Random validation: Dijkstra vs Bellman-Ford vs Floyd (200 non-negative graphs) ===")
    random.seed(3)
    for _ in range(200):
        vs = list("ABCDEF")
        es = [(a, b, random.randint(1, 9)) for a in vs for b in vs if a != b and random.random() < 0.35]
        for s in vs[:2]:
            a1, _ = dijkstra(vs, es, s)
            a2, _, _ = bellman_ford(vs, es, s)
            a3 = floyd(vs, es)[-1][vs.index(s)]
            assert all(a1[v] == a2[v] == a3[vs.index(v)] for v in vs)
    print("All three algorithms agree on all 400 source/graph combinations.")
