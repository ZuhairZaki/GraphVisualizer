import time
import matplotlib.pyplot as plt
from GraphGenerator import generate_connected_graph
from kruskal import kruskalMST
from prim import primMST

def compare_mst_times(sparse=True):
    vertex_counts = list(range(10,510,10))
    if sparse:
        edge_density = 0.1
        plt_title = "Execution Time Comparison (Sparse Graphs)"
        filename = "SparseGraphComparison.png"
    else:
        edge_density = 0.8
        plt_title = "Execution Time Comparison (Dense Graphs)"
        filename = "DenseGraphComparison.png"

    kruskal_times = []
    prim_times = []

    for num_vertices in vertex_counts:
        vertices, edges, adj_list = generate_connected_graph(num_vertices=num_vertices, edge_density=edge_density)

        start = time.perf_counter()
        kruskalMST(vertices=vertices,edges=edges)
        kruskal_times.append((time.perf_counter() - start)*1000)

        start = time.perf_counter()
        primMST(vertices=vertices,adj_list=adj_list)
        prim_times.append((time.perf_counter() - start)*1000)

    plt.figure(figsize=(8, 5))
    plt.plot(vertex_counts, kruskal_times, marker='.', label="Kruskal")
    plt.plot(vertex_counts, prim_times, marker='.', label="Prim")
    plt.title(plt_title)
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (milliseconds)")
    plt.legend()
    plt.savefig(filename)
    plt.close()


if __name__=="__main__":
    compare_mst_times()
    compare_mst_times(sparse=False)
