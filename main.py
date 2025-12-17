#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from GraphLibrary import (
    read_graph_from_file,
    degree,
    find_connected_components,
    bfs_traversal,
    kruskal_mst,
    visualize_graph
)

def main():
    print("ДЕМОНСТРАЦИЯ GraphLibrary")
    
    # 1. Загружаем граф из файла
    graph_file = os.path.join(os.path.dirname(__file__), 'test_data', 'demo_graph.txt')
    print(f"[1] Загрузка графа из {graph_file}")
    graph = read_graph_from_file(graph_file)

    if not graph:
        print(" Файл не найден или пустой!")
        return

    # 2. Базовая информация
    print(f"[2] Информация о графе:")
    print(f"   Всего вершин: {len(graph)}")
    edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2
    print(f"   Всего рёбер: {edge_count}")
    print("   Структура:")
    for v in sorted(graph):
        print(f"     {v} → {graph[v]}")

    # 3. Степени вершин
    print(f"\n[3] Степени вершин:")
    for v in sorted(graph):
        print(f"   deg({v}) = {degree(graph, v)}")

    # 4. Компоненты связности
    components = find_connected_components(graph)
    print(f"\n[4] Компоненты связности ({len(components)}):")
    for i, comp in enumerate(components, 1):
        print(f"   Компонента {i}: {', '.join(comp)}")

    # 5. Обход в ширину (BFS)
    start = sorted(graph.keys())[0]  # берём первую по алфавиту
    bfs_order = bfs_traversal(graph, start)
    print(f"\n[5] BFS из вершины '{start}':")
    print(f"   Порядок обхода: {' → '.join(bfs_order)}")

    # 6. Минимальное остовное дерево (Краскал)
    mst, weight = kruskal_mst(graph)
    print(f"\n[6] Минимальное остовное дерево:")
    print(f"   Общий вес: {weight}")
    print("   Рёбра MST:")
    for v in sorted(mst):
        if mst[v]:
            print(f"     {v} → {sorted(mst[v])}")

    # 7. Визуализация
    print(f"\n[7] Визуализация графа...")
    visualize_graph(graph, title="Исходный граф")
    visualize_graph(mst, title="Минимальное остовное дерево")

    print(" Библиотека работает корректно!")



if __name__ == "__main__":
    main()