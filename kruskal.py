from DSU import DisjointSet

def kruskalMST(vertices, edges):
    edges.sort(key=lambda e: e[2])

    ds = DisjointSet(vertices)
    mst_edges = []
    mst_weight = 0

    for u, v, w in edges:
        if ds.union(u, v):
            mst_edges.append((u, v, w))
            mst_weight += w

    return mst_edges, mst_weight