"""Task 5 - Dijkstra, Bellman-Ford and Floyd-Warshall on the same graph."""
import heapq
import random
import time

INF = float("inf")
EDGES = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 6),
         ("C", "D", 1), ("D", "E", 3), ("C", "E", 8)]
V = ["A", "B", "C", "D", "E"]


def dijkstra(vertices, edges, src, verbose=True):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        if w < 0:
            raise ValueError("Dijkstra requires non-negative weights")
        adj[u].append((v, w))
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[src] = 0
    done = set()
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        if verbose:
            print(f"  Select {u} (dist={d}); finalised={sorted(done)}")
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))
                if verbose:
                    print(f"     relax {u}->{v} (w={w}): dist[{v}]={dist[v]}, pred[{v}]={u}")
    return dist, pred


def path_to(pred, t):
    p = []
    while t is not None:
        p.append(t)
        t = pred[t]
    return "->".join(reversed(p))


def bellman_ford(vertices, edges, src, verbose=True):
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[src] = 0
    for rnd in range(1, len(vertices)):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                changed = True
        if verbose:
            print(f"  Round {rnd}: {dist}")
        if not changed:
            break
    neg_cycle = any(dist[u] != INF and dist[u] + w < dist[v] for u, v, w in edges)
    return dist, pred, neg_cycle


def floyd_warshall(vertices, edges, verbose=True):
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    for u, v, w in edges:
        D[idx[u]][idx[v]] = min(D[idx[u]][idx[v]], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
        if verbose:
            print(f"  After allowing intermediate vertex up to {vertices[k]}:")
            show(D, vertices)
    return D


def show(D, vertices):
    print("       " + " ".join(f"{v:>4}" for v in vertices))
    for i, v in enumerate(vertices):
        print(f"    {v}  " + " ".join(f"{'INF' if x == INF else x:>4}" for x in D[i]))


def main():
    print("=== TASK 5: Shortest paths ===")
    print("\n[5.1 Dijkstra from A]")
    dist, pred = dijkstra(V, EDGES, "A")
    for v in V:
        print(f"  dist[{v}]={dist[v]}  path {path_to(pred, v)}")

    print("\n[5.2 Bellman-Ford from A on the same graph]")
    d2, p2, neg = bellman_ford(V, EDGES, "A")
    print("  Final:", d2, "| negative cycle reachable:", neg)

    print("\n[5.2 Negative edge, no cycle: A->B 4, A->C 5, C->B -3]")
    e = [("A", "B", 4), ("A", "C", 5), ("C", "B", -3)]
    vv = ["A", "B", "C"]
    print("  Bellman-Ford:", bellman_ford(vv, e, "A", verbose=False)[:1])
    try:
        dijkstra(vv, e, "A", verbose=False)
    except ValueError as ex:
        print("  Dijkstra rejects:", ex)
    # show what unguarded greedy would give
    print("  (Unguarded greedy would finalise B at 4, but true shortest is 2 via C.)")

    print("\n[5.2 Negative cycle: A->B 1, B->C -2, C->B 1]")
    e = [("A", "B", 1), ("B", "C", -2), ("C", "B", 1)]
    print("  Bellman-Ford detects negative cycle:",
          bellman_ford(vv, e, "A", verbose=False)[2])

    print("\n[5.3 Floyd-Warshall, all pairs]")
    D = floyd_warshall(V, EDGES, verbose=True)
    print("  FINAL all-pairs matrix:")
    show(D, V)

    print("\n[Boundary: single vertex]")
    print("  Dijkstra:", dijkstra(["A"], [], "A", verbose=False)[0])
    print("[Boundary: unreachable vertex]")
    print("  Dijkstra:", dijkstra(["A", "B"], [], "A", verbose=False)[0])

    print("\n[Performance on random graphs (non-negative weights)]")
    random.seed(11)
    for n in (40, 80, 120):
        vs = list(range(n))
        es = [(random.randrange(n), random.randrange(n), random.randint(1, 20)) for _ in range(4 * n)]
        es = [(u, v, w) for u, v, w in es if u != v]
        t0 = time.perf_counter()
        d1, _ = dijkstra(vs, es, 0, verbose=False)
        t1 = time.perf_counter()
        d2, _, _ = bellman_ford(vs, es, 0, verbose=False)
        t2 = time.perf_counter()
        D = floyd_warshall(vs, es, verbose=False)
        t3 = time.perf_counter()
        same = all(d1[v] == d2[v] == D[0][v] for v in vs)
        print(f"  V={n:>3}, E={len(es):>3}: Dijkstra={1000*(t1-t0):8.3f} ms  "
              f"Bellman-Ford={1000*(t2-t1):8.3f} ms  Floyd={1000*(t3-t2):9.3f} ms  agree={same}")


if __name__ == "__main__":
    main()
