def build_adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def input_order(n, adj):
    return list(range(n))


def heuristic_order(n, adj):
    placed = []
    is_placed = [False] * n
    while len(placed) < n:
        best = -1
        best_links = -1
        best_degree = -1
        for v in range(n):
            if is_placed[v]:
                continue
            links = 0
            for u in adj[v]:
                if is_placed[u]:
                    links += 1
            degree = len(adj[v])
            if links > best_links or (links == best_links and degree > best_degree):
                best = v
                best_links = links
                best_degree = degree
        placed.append(best)
        is_placed[best] = True
    return placed


def is_safe(v, c, adj, colour):
    for u in adj[v]:
        if colour[u] == c:
            return False
    return True


def search(k, order, adj, m, colour, stats):
    stats["nodes"] += 1
    if k > stats["max_depth"]:
        stats["max_depth"] = k
    if k == len(order):
        return True
    v = order[k]
    for c in range(1, m + 1):
        stats["attempts"] += 1
        if is_safe(v, c, adj, colour):
            colour[v] = c
            if search(k + 1, order, adj, m, colour, stats):
                return True
            colour[v] = 0
            stats["backtracks"] += 1
        else:
            stats["rejected"] += 1
    return False


def colour_graph(n, edges, m, ordering="input"):
    adj = build_adjacency(n, edges)
    if ordering == "input":
        order = input_order(n, adj)
    else:
        order = heuristic_order(n, adj)
    colour = [0] * n
    stats = {"nodes": 0, "attempts": 0, "rejected": 0, "backtracks": 0, "max_depth": 0}
    found = search(0, order, adj, m, colour, stats)
    return found, colour, stats, order


def is_valid_colouring(n, edges, m, colour):
    if len(colour) != n:
        return False
    for v in range(n):
        if colour[v] < 1 or colour[v] > m:
            return False
    for u, v in edges:
        if colour[u] == colour[v]:
            return False
    return True


def trace_search(k, order, adj, m, colour, names, log):
    if k == len(order):
        log.append([len(log) + 1, k, "-", "-", "all services assigned", "ACCEPT", "SUCCESS - return TRUE"])
        return True
    v = order[k]
    for c in range(1, m + 1):
        clashes = [names[u] for u in adj[v] if colour[u] == c]
        if clashes:
            log.append([len(log) + 1, k + 1, names[v], c, "clash with " + ",".join(clashes), "REJECT", "try next colour"])
        else:
            log.append([len(log) + 1, k + 1, names[v], c, "no neighbour has colour " + str(c), "ACCEPT", "assign " + names[v] + "=" + str(c) + ", explore next"])
            colour[v] = c
            if trace_search(k + 1, order, adj, m, colour, names, log):
                return True
            colour[v] = 0
            log.append([len(log) + 1, k + 1, names[v], c, "subtree failed", "UNDO", "BACKTRACK: " + names[v] + " reset to 0"])
    log.append([len(log) + 1, k + 1, names[v], "-", "no colour left for " + names[v], "FAIL", "return FALSE to parent"])
    return False
