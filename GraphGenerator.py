import random

def generate_connected_graph(num_vertices, edge_density):
    if num_vertices < 2:
        raise ValueError("Graph must have at least 2 vertices")

    min_weight=1
    max_weight=100
    vertices = list(range(num_vertices))
    edges = []
    connected = {0}
    remaining = set(vertices) - connected

    while remaining:
        u = random.choice(list(connected))
        v = random.choice(list(remaining))
        w = random.randint(min_weight, max_weight)
        edges.append((u, v, w))
        connected.add(v)
        remaining.remove(v)

    possible_edges = [(u, v) for u in range(num_vertices) for v in range(u + 1, num_vertices)
                      if (u, v) not in [(a, b) if a < b else (b, a) for a, b, _ in edges]]

    extra_edges_count = int(edge_density * len(possible_edges))
    extra_edges = random.sample(possible_edges, extra_edges_count)

    for u, v in extra_edges:
        w = random.randint(min_weight, max_weight)
        edges.append((u, v, w))

    adj_list = {i: [] for i in range(num_vertices)}
    for u, v, w in edges:
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))

    return vertices, edges, adj_list