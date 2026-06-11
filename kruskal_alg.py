import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- 1. DEFINICIÓN DE LOS 75 NODOS Y ARISTAS ---
edges_data = [
    (1, 2, 3), (1, 3, 2), (2, 4, 5), (2, 5, 1), (3, 6, 4), (3, 7, 3), (4, 8, -1),
    (4, 9, 2), (5, 10, 7), (5, 11, 3), (6, 12, 1), (6, 13, 4), (7, 14, 6), (7, 15, 3),
    (8, 16, 2), (9, 17, 1), (10, 18, 3), (10, 19, 2), (11, 20, 4), (12, 21, -2), 
    (13, 22, 3), (13, 23, 5), (14, 24, 1), (14, 25, -3), (15, 26, 2), (15, 27, 4), 
    (16, 28, 1), (17, 29, 5), (17, 30, 2), (18, 31, 3), (19, 32, -1), (20, 33, 6), 
    (20, 34, 2), (21, 35, 4), (22, 36, 1), (23, 37, 3), (24, 38, 2), (25, 39, 5), 
    (26, 40, -3), (27, 41, 4), (28, 42, 1), (29, 43, 2), (30, 44, 4), (31, 45, 3), 
    (32, 46, 5), (33, 47, 6), (34, 48, 2), (35, 49, 1), (36, 50, 3), (37, 51, 4), 
    (38, 52, -2), (39, 53, 5), (40, 54, 1), (41, 55, 3), (42, 56, 2), (43, 57, 6), 
    (44, 58, -1), (45, 59, 4), (46, 60, 3), (47, 61, 2), (48, 62, 5), (49, 63, -2), 
    (50, 64, 3), (51, 65, 4), (52, 66, 2), (53, 67, 1), (54, 68, -3), (55, 69, 5), 
    (56, 70, 4), (57, 71, -1), (58, 72, 3), (59, 73, 6), (60, 74, 2), (61, 75, 4),
    (62, 2, 5), (63, 3, 3), (64, 4, 4), (65, 5, 1), (66, 6, 2), (67, 7, 4),
    (68, 8, 3), (69, 9, 5), (70, 10, 6), (71, 10, 2), (72, 11, 1), (73, 12, 3),
    (74, 1, 3), (62, 3, 5), (63, 5, 3), (64, 6, 4), (65, 7, 1), (66, 8, 2),
    (67, 9, 4), (68, 23, 3), (69, 24, 5), (70, 25, 6), (71, 32, 2), (72, 22, 1),
    (73, 4, 3), (74, 44, 3), (75, 4, 3), (75, 5, 4)
]

# --- 2. FUNCIONES GRÁFICAS Y DE ANIMACIÓN ---
def draw_base_graph(G, pos, title):
    """Dibuja el grafo base completo en gris claro."""
    plt.clf()
    plt.title(title, fontsize=14, fontweight='bold', color='darkgreen')
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=350, font_size=8, edge_color='gainsboro')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.pause(0.5)

def animate_kruskal(G, pos, start_node, end_node):
    """Ejecuta la animación de Kruskal (Armado del árbol y luego la ruta)."""
    # 1. Obtener las aristas del Árbol de Expansión Mínima ordenadas por Kruskal
    mst_edges = list(nx.minimum_spanning_edges(G, algorithm='kruskal', data=False))
    
    # Crear un grafo vacío que representará nuestro nuevo árbol (MST)
    mst_graph = nx.Graph()
    mst_graph.add_nodes_from(G.nodes)
    
    plt.title("Algoritmo Kruskal: Armando Árbol de Expansión Mínima (MST)...", fontsize=14, fontweight='bold', color='green')
    
    # Animación Fase 1: Armado del árbol arista por arista
    for u, v in mst_edges:
        mst_graph.add_edge(u, v)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='green', width=2.5)
        plt.pause(0.2) # Pausa rápida para las 74 aristas del árbol
        
    plt.pause(1.0) # Pausa dramática antes de buscar la ruta

    # Animación Fase 2: Buscar y dibujar la ruta dentro del nuevo árbol
    try:
        plt.title(f"Kruskal MST: Ruta encontrada de {start_node} a {end_node}", fontsize=14, fontweight='bold', color='purple')
        
        # Calculamos la ruta EXCLUSIVAMENTE usando las aristas del árbol recién creado
        path = nx.shortest_path(mst_graph, start_node, end_node)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='thistle', node_size=400)
        
        path_edges = list(zip(path, path[1:]))
        for edge in path_edges:
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='purple', width=3.5)
            plt.pause(0.8) # Pausa lenta para ver el recorrido de la ruta final
            
        plt.show(block=True)
        
    except nx.NetworkXNoPath:
        messagebox.showwarning("Sin Ruta", f"El Árbol de Expansión Mínima no pudo conectar el nodo {start_node} con el {end_node}.")

# --- 3. LÓGICA PRINCIPAL ---
def main():
    root = tk.Tk()
    root.withdraw()
    
    # Kruskal trabaja con Grafos No Dirigidos (nx.Graph en lugar de nx.DiGraph)
    G = nx.Graph()
    G.add_weighted_edges_from(edges_data)
    
    pos = nx.kamada_kawai_layout(G, weight=None)

    try:
        start_node = simpledialog.askinteger("Kruskal", "Introduzca el nodo de ORIGEN (Ej: 33):")
        end_node = simpledialog.askinteger("Kruskal", "Introduzca el nodo de DESTINO (Ej: 51):")
        
        if start_node is None or end_node is None:
            messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")
            return
            
        if start_node not in G.nodes or end_node not in G.nodes:
            messagebox.showerror("Error", "Los nodos ingresados no existen en el grafo.")
            return

        plt.ion()
        plt.figure(figsize=(12, 8))
        
        draw_base_graph(G, pos, "Grafo Base Preparado para Kruskal")
        
        # Llamamos a la función de animación que contiene toda la lógica de Kruskal
        animate_kruskal(G, pos, start_node, end_node)
        
    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    main()