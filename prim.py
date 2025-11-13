import heapq


def primMST(vertices, adj_list, start_v=None):
    if not vertices:
        return [], 0

    if start_v is None:
        start_v  = vertices[0]

    mst_vertices = set()
    mst_edges = []
    mst_weight = 0
    pq = []

    mst_vertices.add(start_v)
    for next, weight in adj_list.get(start_v, []):
        heapq.heappush(pq, (weight, start_v, next))

    while pq:
        weight, u, v = heapq.heappop(pq)
        if v in mst_vertices:
            continue
        
        mst_vertices.add(v)
        mst_edges.append((u, v, weight))
        mst_weight += weight
        
        for next, weight in adj_list.get(v, []):
            if next not in mst_vertices:
                heapq.heappush(pq, (weight, v, next))
                
        if len(mst_vertices)==len(vertices):
            break

    return mst_edges, mst_weight
