import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- 1. DEFINICIÓN DE LOS 75 NODOS Y ARISTAS ---
# Datos extraídos de la Tabla de Nodos y Aristas del examen
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
    """Dibuja el grafo completo en gris claro como base."""
    plt.clf()
    plt.title(title, fontsize=14, fontweight='bold', color='darkblue')
    # Dibujar nodos y aristas
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=350, font_size=8, edge_color='gainsboro')
    
    # Dibujar los pesos de las aristas (incluyendo los negativos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.pause(0.5)

def animate_bellman_ford_path(G, pos, path, title):
    """Anima la ruta encontrada reduciendo la velocidad arista por arista."""
    plt.title(title, fontsize=14, fontweight='bold', color='navy')
    
    # Resaltar los nodos de la ruta encontrada en cyan
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='cyan', node_size=400)
    
    # Generar la lista de aristas que componen la ruta
    path_edges = list(zip(path, path[1:]))
    
    # Animación: Dibujar arista por arista con un retraso (pausa)
    for edge in path_edges:
        # Se usa color azul para distinguir Bellman-Ford de Dijkstra
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='blue', width=3.0)
        plt.pause(0.8)  # Retardo para ver el armado paso a paso
    
    plt.show(block=True)

# --- 3. LÓGICA PRINCIPAL ---
def main():
    # Ocultar la ventana raíz de Tkinter
    root = tk.Tk()
    root.withdraw() 
    
    # Construir el grafo dirigido
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges_data)
    
    # Calcular las posiciones de los nodos (Layout)
    # Ignoramos el peso visualmente para que scipy/kamada_kawai no falle por los negativos
    pos = nx.kamada_kawai_layout(G, weight=None)

    try:
        # Solicitud de nodos por teclado mediante Interfaz Gráfica
        start_node = simpledialog.askinteger("Bellman-Ford", "Introduzca el nodo de ORIGEN (Ej: 33):")
        end_node = simpledialog.askinteger("Bellman-Ford", "Introduzca el nodo de DESTINO (Ej: 51):")
        
        # Validaciones de entrada
        if start_node is None or end_node is None:
            messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")
            return
            
        if start_node not in G.nodes or end_node not in G.nodes:
            messagebox.showerror("Error", "Los nodos ingresados no existen en el grafo de 75 nodos.")
            return

        # Activar el modo interactivo de Matplotlib para la animación
        plt.ion()
        plt.figure(figsize=(12, 8))
        
        # Ejecución del algoritmo Bellman-Ford usando los pesos reales (soporta negativos)
        path = nx.bellman_ford_path(G, start_node, end_node, weight='weight')
        
        # Iniciar las funciones gráficas
        draw_base_graph(G, pos, f"Grafo Completo - Buscando ruta de {start_node} a {end_node}...")
        animate_bellman_ford_path(G, pos, path, f"Algoritmo Bellman-Ford: Ruta final ({start_node} → {end_node})")
        
    except nx.NetworkXUnbounded:
        # Excepción específica de Bellman-Ford si detecta un bucle infinito de pesos negativos
        messagebox.showerror("Ciclo Negativo", "El algoritmo falló porque detectó un ciclo de peso negativo en el grafo.")
    except nx.NetworkXNoPath:
        # Excepción si los nodos no están conectados
        messagebox.showwarning("Sin Ruta", f"No existe un camino posible entre el nodo {start_node} y el nodo {end_node}.")
    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    main()