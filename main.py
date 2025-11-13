import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from kruskal import kruskalMST
from prim import primMST
import time


class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Input")
        self.root.geometry("900x600")

        self.G = nx.Graph()
        self.adj_list = {}
        self.edges = []

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Vertex:").grid(row=0, column=0, padx=5)
        self.vertex_entry = tk.Entry(input_frame, width=10)
        self.vertex_entry.grid(row=0, column=1, padx=5)
        tk.Button(input_frame, text="Add Vertex", command=self.add_vertex).grid(row=0, column=2, padx=5)
        
        tk.Label(input_frame, text="Edge (u v w):").grid(row=1, column=0, padx=5)
        self.edge_entry = tk.Entry(input_frame, width=12)
        self.edge_entry.grid(row=1, column=1, padx=5)
        tk.Button(input_frame, text="Add Edge", command=self.add_edge).grid(row=1, column=2, padx=5)

        tk.Button(input_frame, text="Clear Graph", command=self.clear_graph, fg="red").grid(row=2, column=0, columnspan=3, pady=10)
        
        mst_frame = tk.Frame(root)
        mst_frame.pack(pady=5)

        tk.Label(mst_frame, text="MST Algorithm:").grid(row=0, column=0, padx=5)
        self.alg_choice = ttk.Combobox(mst_frame, values=["Kruskal", "Prim"], width=10, state="readonly")
        self.alg_choice.set("Kruskal")
        self.alg_choice.grid(row=0, column=1, padx=5)

        tk.Button(mst_frame, text="Compute MST", bg="lightgreen", command=self.compute_mst).grid(row=0, column=2, padx=5)
        
        display_frame = tk.Frame(root)
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(5.5, 4.5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=display_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        pos = nx.spring_layout(self.G)
        nx.draw(
            self.G, pos, ax=self.ax,
            with_labels=True, node_color='skyblue',
            node_size=300, font_size=8, font_weight='bold'
        )

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(
            self.G,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            font_color='red',
            label_pos=0.5,
            ax=self.ax
        )
        
        self.ax.set_title("Graph Visualization", fontsize=8)
        self.ax.axis("off")
        self.canvas.draw()

    def add_vertex(self):
        vertex = self.vertex_entry.get().strip()
        if not vertex:
            messagebox.showwarning("Input Error", "Please enter a vertex name.")
            return
        if vertex in self.G.nodes:
            messagebox.showinfo("Duplicate Vertex", f"Vertex '{vertex}' already exists.")
        else:
            self.G.add_node(vertex)
            self.adj_list[vertex] = []
            self.draw_graph()
        self.vertex_entry.delete(0, tk.END)

    def add_edge(self):
        edge_input = self.edge_entry.get().strip().split()
        if len(edge_input) != 3:
            messagebox.showwarning("Input Error", "Please enter edge as: u v w (e.g., A B 5).")
            return

        u, v, w_str = edge_input
        
        try:
            w = float(w_str)
        except ValueError:
            messagebox.showerror("Input Error", "Weight must be a number.")
            return


        if u not in self.G.nodes or v not in self.G.nodes:
            messagebox.showerror(
                "Invalid Edge",
                f"Both vertices must exist before adding an edge.\nMissing: {', '.join([x for x in [u, v] if x not in self.G.nodes])}"
            )
            return
        
        if self.G.has_edge(u, v):
            messagebox.showinfo("Duplicate Edge", f"Edge '{u}-{v}' already exists.")
            return

        self.G.add_edge(u, v, weight=w)
        self.adj_list[u].append((v, w))
        self.adj_list[v].append((u, w))
        self.edges.append((u, v, w))
        
        self.draw_graph()
        self.edge_entry.delete(0, tk.END)
        
    def compute_mst(self):
        if not self.edges:
            messagebox.showinfo("Empty Graph", "No edges in graph.")
            return
        
        if not nx.is_connected(self.G):
            messagebox.showerror(
                "Disconnected Graph",
                "A Minimum Spanning Tree can only be formed from a connected graph."
            )
            return

        algo = self.alg_choice.get()
        try:
            start = time.time()
            if algo == "Kruskal":
                mst_edges, total = kruskalMST(list(self.adj_list.keys()), self.edges)
            else: 
                mst_edges, total = primMST(list(self.adj_list.keys()), self.adj_list)
            end = time.time()
            elapsed = (end - start) * 1000
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.show_mst_window(mst_edges, total, algo, elapsed)
        
    def show_mst_window(self, mst_edges, total_weight, algorithm, elapsed_time):
        win = tk.Toplevel(self.root)
        win.title(f"{algorithm} MST Result")
        win.geometry("600x400")

        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        G_mst = nx.Graph()
        for u, v, w in mst_edges:
            G_mst.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G_mst, seed=42)
        nx.draw(
            G_mst, pos, ax=ax,
            with_labels=True,
            node_color="lightgreen",
            node_size=300,
            font_weight="bold"
        )

        edge_labels = nx.get_edge_attributes(G_mst, "weight")
        nx.draw_networkx_edge_labels(G_mst, pos, edge_labels=edge_labels, font_color="blue", ax=ax)

        ax.set_title(f"{algorithm} MST (Total Weight = {total_weight})", fontsize=8)
        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
        time_frame = tk.Frame(win)
        time_frame.pack(pady=10)

        tk.Label(time_frame, text=f"Execution Time: {elapsed_time:.4f} ms", font=("Arial", 10), fg="darkblue").pack()

    def clear_graph(self):
        self.G.clear()
        self.adj_list.clear()
        self.edges.clear()
        self.draw_graph()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
