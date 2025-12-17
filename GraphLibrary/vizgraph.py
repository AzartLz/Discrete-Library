import matplotlib.pyplot as plt
import numpy as np

def visualize_graph(graph, title="Граф"):
    """Рисует граф только с помощью matplotlib (исправленная версия)"""
    if not graph:
        print("Граф пуст!")
        return
    
    # Собираем ВСЕ вершины: и ключи, и все соседи
    all_vertices = set(graph.keys())
    for neighbors in graph.values():
        all_vertices.update(neighbors)
    
    if not all_vertices:
        return
    
    vertices = sorted(all_vertices)               # сортируем для детерминизма
    n = len(vertices)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Расположение вершин по кругу
    pos = {v: (np.cos(2*np.pi*i/n), np.sin(2*np.pi*i/n)) 
           for i, v in enumerate(vertices)}
    
    # Рисуем ребра
    edges_drawn = set()
    for v in vertices:
        if v not in graph:
            continue
        for u in graph[v]:
            edge_key = tuple(sorted([v, u]))
            if edge_key not in edges_drawn:
                x1, y1 = pos[v]
                x2, y2 = pos[u]                  # теперь u точно есть в pos!
                ax.plot([x1, x2], [y1, y2], 'gray', linewidth=2, alpha=0.7, zorder=1)
                edges_drawn.add(edge_key)
    
    # Рисуем вершины
    for v in vertices:
        x, y = pos[v]
        circle = plt.Circle((x, y), 0.12, facecolor='lightblue', 
                           edgecolor='black', linewidth=2, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(v), ha='center', va='center', 
               fontsize=14, fontweight='bold', zorder=3)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.show()