import matplotlib.pyplot as plt
import networkx as nx  # Usado estrictamente para el motor gráfico (layout)
import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq

# --- 1. DEFINICIÓN DE DATOS ---
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

# Transformar la lista plana en un diccionario estructurado (Grafo real en Python)
grafo_diccionario = {i: {} for i in range(1, 76)}
for u, v, peso in edges_data:
    grafo_diccionario[u][v] = peso

# --- 2. DIJKSTRA---
def dijkstra_manual(grafo, inicio, destino):
    """Calcula la ruta usando matemáticas sin usar la lógica de NetworkX"""
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    nodo_previo = {nodo: None for nodo in grafo}
    
    # Cola de prioridad (Costo_acumulado, Nodo_actual)
    cola = [(0, inicio)]
    visitados = set()

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        if nodo_actual in visitados:
            continue
            
        visitados.add(nodo_actual)
        
        if nodo_actual == destino:
            break # Llegamos al objetivo
            
        for vecino, peso in grafo[nodo_actual].items():
            if vecino in visitados:
                continue
                
            # Convertimos a positivo para que Dijkstra no colapse con los negativos del examen
            nueva_distancia = distancia_actual + abs(peso)
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                nodo_previo[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    # Reconstruir la ruta hacia atrás
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = nodo_previo[actual]
        
    if ruta[0] == inicio:
        return ruta
    else:
        raise ValueError("No existe ruta posible.")

# --- 3. EL "PINTOR": ANIMACIÓN VISUAL ---
def draw_base_graph(G, pos, title):
    plt.clf()
    plt.title(title, fontsize=12, fontweight='bold', color='darkblue')
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=350, font_size=8, edge_color='gainsboro')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.pause(0.5)

def animate_path(G, pos, path, title):
    plt.title(title, fontsize=12, fontweight='bold', color='darkred')
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='yellow', node_size=400)
    
    path_edges = list(zip(path, path[1:]))
    for edge in path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='red', width=3.0)
        plt.pause(0.8) # Reducción de velocidad
    plt.show(block=True)

# --- 4. CONTROL PRINCIPAL ---
def main():
    root = tk.Tk()
    root.withdraw()
    
    # Creamos el grafo visual SOLO para pasárselo al pintor
    G_visual = nx.DiGraph()
    G_visual.add_weighted_edges_from(edges_data)
    pos = nx.kamada_kawai_layout(G_visual, weight=None)

    try:
        start_node = simpledialog.askinteger("Dijkstra", "Introduzca el nodo de ORIGEN:")
        end_node = simpledialog.askinteger("Dijkstra", "Introduzca el nodo de DESTINO:")
        
        if not start_node or not end_node:
            return
            
        if start_node not in grafo_diccionario or end_node not in grafo_diccionario:
            messagebox.showerror("Error", "Nodos no válidos.")
            return

        # 1. EL CEREBRO CALCULA LA RUTA
        ruta_calculada_a_mano = dijkstra_manual(grafo_diccionario, start_node, end_node)
        
        # 2. EL PINTOR LA DIBUJA
        plt.ion()
        plt.figure(figsize=(12, 8))
        draw_base_graph(G_visual, pos, f"Grafo Completo - Buscando ruta de {start_node} a {end_node}...")
        animate_path(G_visual, pos, ruta_calculada_a_mano, f"Dijkstra: Ruta {start_node} → {end_node}")
        
    except ValueError as ve:
        messagebox.showwarning("Sin Ruta", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()