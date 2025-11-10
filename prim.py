import heapq


def prim(vertices, adjacency_list, start=None):
    if not vertices:
        return [], 0

    if start is None:
        start = vertices[0]

    visited = set()
    mst_edges = []
    total_weight = 0

    min_heap = []

    def add_edges(vertex):
        visited.add(vertex)
        for neighbor, weight in adjacency_list.get(vertex, []):
            if neighbor not in visited:
                heapq.heappush(min_heap, (weight, vertex, neighbor))
                
    add_edges(start)

    while min_heap and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(min_heap)
        if v in visited:
            continue
        mst_edges.append((u, v, weight))
        total_weight += weight
        add_edges(v)

    return mst_edges, total_weight
