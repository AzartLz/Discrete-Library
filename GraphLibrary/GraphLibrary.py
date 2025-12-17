"""Библиотека для работы с графами xd"""
from typing import List, Dict, Optional
from collections import deque
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))
from inputgraph import read_graph_from_file, write_graph_to_file
from vizgraph import visualize_graph


# Program_Graph_Init.py
def init_graph(filename):
    """Загружает граф из файла и выводит информацию"""
    print("="*55)
    print("ПРОГРАММА: ИНИЦИАЛИЗАЦИЯ ГРАФА")
    print("="*55)
    graph = read_graph_from_file(filename)
    if not graph:
        return None
    print(f"\n[2] Информация о графе:")
    print(f"    Всего вершин: {len(graph)}")
    edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2
    print(f"    Всего рёбер: {edge_count}")
    for vertex in sorted(graph.keys()):
        neighbors = graph[vertex]
        print(f"    {vertex} → {neighbors if neighbors else 'нет соседей'}")
    print(f"\n[4] Визуализация графа...")
    visualize_graph(graph, title="Результат инициализации графа")
    return graph

# Program_Vertex_Operations
def add_vertex(graph, vertex_name):
    """Добавляет вершину в граф"""
    if vertex_name in graph:
        print(f" Вершина '{vertex_name}' уже существует!")
        return False
    
    graph[vertex_name] = []
    print(f" Вершина '{vertex_name}' добавлена!")
    return True

def remove_vertex(graph, vertex_name):
    """Удаляет вершину и все связанные рёбра"""
    if vertex_name not in graph:
        print(f" Вершина '{vertex_name}' не найдена!")
        return False
    
    # Удаляем ребра из соседей
    for neighbor in graph[vertex_name]:
        if vertex_name in graph[neighbor]:
            graph[neighbor].remove(vertex_name)
    
    del graph[vertex_name]
    print(f" Вершина '{vertex_name}' и все её рёбра удалены!")
    return True

# Program_Edge_Operations
def add_edge(graph, v1, v2):
    """Добавляет ребро между двумя вершинами (неориентированный граф)"""
    if v1 not in graph:
        print(f" Вершина '{v1}' не найдена!")
        return False
    if v2 not in graph:
        print(f" Вершина '{v2}' не найдена!")
        return False
    
    if v2 in graph[v1] or v1 in graph[v2]:
        print(f" Ребро {v1}-{v2} уже существует!")
        return False
    
    graph[v1].append(v2)
    graph[v2].append(v1)
    print(f" Ребро {v1}-{v2} добавлено!")
    return True

def remove_edge(graph, v1, v2):
    """Удаляет ребро между двумя вершинами"""
    if v1 not in graph or v2 not in graph:
        print(f" Одна из вершин не найдена!")
        return False
    
    if v2 not in graph[v1] and v1 not in graph[v2]:
        print(f" Ребра {v1}-{v2} не существует!")
        return False
    
    if v2 in graph[v1]:
        graph[v1].remove(v2)
    if v1 in graph[v2]:
        graph[v2].remove(v1)
    
    print(f" Ребро {v1}-{v2} удалено!")
    return True

# Program_Vertex_Degree
def degree(graph, vertex_name):
    """Возвращает степень вершины (количество инцидентных рёбер)"""
    if vertex_name not in graph:
        return -1  # Вершина не найдена
    return len(graph[vertex_name])

# Program_Subgraph_Check
def is_subgraph(main_graph, sub_graph):
    """Проверяет, является ли sub_graph подграфом main_graph"""
    # Проверяем все вершины подграфа
    for vertex in sub_graph:
        if vertex not in main_graph:
            return False
    
    # Проверяем все рёбра подграфа
    for vertex in sub_graph:
        for neighbor in sub_graph[vertex]:
            if neighbor not in main_graph[vertex]:
                return False
    
    return True

# Program_Graph_Type_Check
def is_directed(graph):
    """Проверяет, является ли граф направленным"""
    for vertex in graph:
        for neighbor in graph[vertex]:
            # Проверяем, есть ли обратное ребро
            if vertex not in graph[neighbor]:
                return True  # Найдено несимметричное ребро
    return False

def is_multigraph(graph):
    """Проверяет, является ли граф мультиграфом (есть кратные рёбра)"""
    # В нашем представлении проверяем дубликаты в списках смежности
    for vertex in graph:
        if len(graph[vertex]) != len(set(graph[vertex])):
            return True  # Найдены дубликаты соседей
    return False

def analyze_graph(graph):
    """Анализирует граф и возвращает словарь свойств"""
    directed = is_directed(graph)
    multigraph = is_multigraph(graph)
    
    return {
        "directed": directed,
        "multigraph": multigraph,
        "type": "Направленный" if directed else "Неориентированный",
        "multi": "Мультиграф" if multigraph else "Простой граф"
    }

# Program_Adjacency_Matrix.py
def build_adjacency_matrix(graph):
    """Строит матрицу смежности из списка смежности"""
    vertices = sorted(graph.keys())
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    
    # Создаем нулевую матрицу
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Заполняем матрицу
    for v, neighbors in graph.items():
        i = index[v]
        for u in neighbors:
            if u in index:
                j = index[u]
                matrix[i][j] = 1
    
    return vertices, matrix

# Program_Incidence_Matrix.py
def build_incidence_matrix(graph):
    """Строит матрицу инцидентности из списка смежности"""
    vertices = sorted(graph.keys())
    edges = []
    
    # Собираем все рёбра (без дубликатов)
    edges_drawn = set()
    for v in graph:
        for u in graph[v]:
            edge = tuple(sorted([v, u]))
            if edge not in edges_drawn:
                edges.append(edge)
                edges_drawn.add(edge)
    
    n = len(vertices)
    m = len(edges)
    
    # Создаем нулевую матрицу
    matrix = [[0 for _ in range(m)] for _ in range(n)]
    
    # Заполняем матрицу
    vertex_index = {v: i for i, v in enumerate(vertices)}
    
    for j, edge in enumerate(edges):
        v1, v2 = edge
        i1 = vertex_index[v1]
        i2 = vertex_index[v2]
        
        # Для неориентированного графа обе вершины имеют 1
        matrix[i1][j] = 1
        matrix[i2][j] = 1
    
    return vertices, edges, matrix

# Program_Adjacency_List.py - онли вывод графов

# Program_From_Matrix.py
def build_graph_from_adjacency_matrix(vertices, matrix):
    """Строит граф из матрицы смежности"""
    graph = {v: [] for v in vertices}
    for i, v in enumerate(vertices):
        for j, u in enumerate(vertices):
            if matrix[i][j] == 1:
                graph[v].append(u)
    return graph

# Program_Isomorphism_Check.py
def get_degree_sequence(graph):
    """Возвращает упорядоченную последовательность степеней"""
    return sorted([len(graph[v]) for v in graph], reverse=True)

def is_isomorphic(graph1, graph2):
    """Базовая проверка изоморфизма по степенным последовательностям"""
    return len(graph1) == len(graph2) and get_degree_sequence(graph1) == get_degree_sequence(graph2)

# Program_Graph_Operation.py
def union_graphs(g1, g2):
    """Объединение графов"""
    result = {v: set(g1.get(v, [])) for v in g1}
    for v, neighbors in g2.items():
        if v not in result:
            result[v] = set()
        result[v].update(neighbors)
    return {v: list(n) for v, n in result.items()}

def intersection_graphs(g1, g2):
    """Пересечение графов"""
    common = set(g1.keys()) & set(g2.keys())
    return {v: list(set(g1[v]) & set(g2[v])) for v in common}

# Program_Composition.py
def graph_composition(g1, g2):
    """Композиция графов: идем по путям g1, затем g2"""
    result = {v: [] for v in g1}
    
    for a in g1:
        for b in g1[a]:
            if b in g2:
                for c in g2[b]:
                    if c not in result[a]:
                        result[a].append(c)
    
    # Очистка пустых вершин
    return {v: sorted(n) for v, n in result.items() if n}

# Program_Reverse_Edges.py
def reverse_edges(graph):
    """Обращает направление всех рёбер"""
    # Создаем пустой граф с теми же вершинами
    reversed_graph = {v: [] for v in graph}
    
    # Заполняем обратные рёбра
    for v, neighbors in graph.items():
        for u in neighbors:
            reversed_graph[u].append(v)
    
    # Сортируем для однозначности
    for v in reversed_graph:
        reversed_graph[v].sort()
    
    return reversed_graph

# Program_Complement.py
def complement_graph(graph):
    """Строит дополнение графа (рёбра, которых нет в исходном)"""
    vertices = list(graph.keys())
    result = {v: [] for v in vertices}
    
    for i, v in enumerate(vertices):
        for u in vertices:
            if u != v and u not in graph[v]:
                result[v].append(u)
    
    # Сортируем для однозначности
    for v in result:
        result[v].sort()
    
    return result

# Program_Connected_Components.py
def bfs_component(graph, start, visited):
    """BFS для поиска одной компоненты связности"""
    component = []
    queue = [start]
    visited.add(start)
    
    while queue:
        vertex = queue.pop(0)
        component.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return sorted(component)

def find_connected_components(graph):
    """Находит все компоненты связности"""
    if not graph:
        return []
    
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = bfs_component(graph, vertex, visited)
            components.append(component)
    
    return sorted(components, key=len, reverse=True)

# Program_Path_Finder.py
def bfs_path(graph, start, end):
    """BFS для поиска кратчайшего пути"""
    if start not in graph or end not in graph:
        return None
    
    visited = {start}
    queue = [(start, [start])]
    
    while queue:
        vertex, path = queue.pop(0)
        
        if vertex == end:
            return path
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

def dfs_path(graph, start, end, visited=None, path=None):
    """DFS для поиска любого пути"""
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    visited.add(start)
    path = path + [start]
    
    if start == end:
        return path
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dfs_path(graph, neighbor, end, visited, path)
            if result:
                return result
    
    return None

# Program_Cycle_Detector.py
def has_cycle(graph):
    """Проверяет, содержит ли граф цикл (DFS с тремя состояниями)"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}
    parent = {v: None for v in graph}
    
    def dfs(vertex):
        color[vertex] = GRAY
        
        for neighbor in graph[vertex]:
            if color[neighbor] == WHITE:
                parent[neighbor] = vertex
                if dfs(neighbor):
                    return True
            elif color[neighbor] == GRAY:
                # Найден цикл
                return True
        
        color[vertex] = BLACK
        return False
    
    for vertex in graph:
        if color[vertex] == WHITE:
            if dfs(vertex):
                return True
    
    return False

def find_cycle(graph):
    """Находит один цикл в графе (если есть)"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}
    parent = {v: None for v in graph}
    cycle = []
    
    def dfs(vertex):
        color[vertex] = GRAY
        
        for neighbor in graph[vertex]:
            if color[neighbor] == WHITE:
                parent[neighbor] = vertex
                result = dfs(neighbor)
                if result:
                    return result
            elif color[neighbor] == GRAY and cycle == []:
                # Найден цикл, восстанавливаем его
                v = vertex
                while v != neighbor:
                    cycle.append(v)
                    v = parent[v]
                cycle.append(neighbor)
                cycle.append(vertex)
                cycle.reverse()
                return cycle
        
        color[vertex] = BLACK
        return None
    
    for vertex in graph:
        if color[vertex] == WHITE:
            result = dfs(vertex)
            if result:
                return result
    
    return None

# Program_Kruskal_MST.py
class DSU:
    """Система непересекающихся множеств (Union-Find)"""
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]
    
    def union(self, v1, v2):
        root1 = self.find(v1)
        root2 = self.find(v2)
        
        if root1 == root2:
            return False
        
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        
        return True

def build_weighted_edges(graph):
    """Создает список рёбер с весами (вес = 1 по умолчанию)"""
    edges = []
    seen = set()
    for v in graph:
        for u in graph[v]:
            edge = tuple(sorted([v, u]))
            if edge not in seen:
                edges.append((edge[0], edge[1], 1))  # вес 1
                seen.add(edge)
    return edges

def kruskal_mst(graph):
    """Алгоритм Краскала для построения MST"""
    vertices = list(graph.keys())
    edges = build_weighted_edges(graph)
    edges.sort(key=lambda x: x[2])  # сортировка по весу
    
    dsu = DSU(vertices)
    mst = {v: [] for v in vertices}
    total_weight = 0
    
    for v1, v2, weight in edges:
        if dsu.union(v1, v2):
            mst[v1].append(v2)
            mst[v2].append(v1)
            total_weight += weight
    
    return mst, total_weight

# Program_Graph_Dimensions.py
def bfs_distances(graph, start):
    """BFS для нахождения расстояний от start до всех вершин"""
    distances = {v: -1 for v in graph}
    distances[start] = 0
    queue = [start]
    
    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)
    
    return [dist for dist in distances.values() if dist >= 0]

def calculate_diameter_radius(graph):
    """Вычисляет диаметр и радиус графа"""
    eccentricities = {}
    
    for vertex in graph:
        distances = bfs_distances(graph, vertex)
        if not distances:
            continue
        eccentricities[vertex] = max(distances)
    
    if not eccentricities:
        return None, None
    
    diameter = max(eccentricities.values())
    radius = min(eccentricities.values())
    
    # Центральные вершины
    center = [v for v, e in eccentricities.items() if e == radius]
    # Периферийные вершины
    periphery = [v for v, e in eccentricities.items() if e == diameter]
    
    return diameter, radius, eccentricities, center, periphery

# Program_Acyclic_Checker.py
def is_acyclic(graph):
    """Проверяет, является ли граф ациклическим (DFS с тремя цветами)"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}
    
    def dfs(vertex):
        color[vertex] = GRAY
        
        for neighbor in graph[vertex]:
            if color[neighbor] == WHITE:
                if not dfs(neighbor):
                    return False
            elif color[neighbor] == GRAY:
                # Найден цикл
                return False
        
        color[vertex] = BLACK
        return True
    
    for vertex in graph:
        if color[vertex] == WHITE:
            if not dfs(vertex):
                return False
    
    return True

def analyze_graph_type(graph):
    """Анализирует тип графа по ацикличности"""
    if is_acyclic(graph):
        # Проверяем связность
        return "Ациклический граф (дерево или лес)"
    else:
        return "Граф содержит циклы"

# Program_BFS_Traversal.py
def bfs_traversal(graph, start_vertex):
    """Обход графа в ширину (BFS)"""
    if start_vertex not in graph:
        return []
    
    visited = []
    queue = [start_vertex]
    visited_set = {start_vertex}
    
    while queue:
        vertex = queue.pop(0)
        visited.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)
    
    return visited

def build_bfs_tree(graph, start_vertex):
    """Строит дерево BFS"""
    if start_vertex not in graph:
        return {}
    
    tree = {v: [] for v in graph}
    visited = {start_vertex}
    queue = [start_vertex]
    parents = {start_vertex: None}
    
    while queue:
        vertex = queue.pop(0)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parents[neighbor] = vertex
                tree[vertex].append(neighbor)
                tree[neighbor].append(vertex)  # для визуализации
    
    return tree

# Program_DFS_Traversal.py
def dfs_traversal(graph, start_vertex):
    """Обход графа в глубину (DFS)"""
    if start_vertex not in graph:
        return []
    
    visited = []
    visited_set = set()
    
    def dfs_recursive(vertex):
        visited.append(vertex)
        visited_set.add(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited_set:
                dfs_recursive(neighbor)
    
    dfs_recursive(start_vertex)
    return visited

# Program_Eulerian_Check.py
def is_connected(graph):
    """Проверяет связность графа (BFS)"""
    if not graph:
        return False
    
    start = next(iter(graph))
    visited = set()
    queue = [start]
    visited.add(start)
    
    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return len(visited) == len(graph)

def is_eulerian(graph):
    """Проверяет, является ли граф эйлеровым"""
    if not is_connected(graph):
        return False
    
    # Все вершины должны иметь четную степень
    for vertex in graph:
        if len(graph[vertex]) % 2 != 0:
            return False
    
    return True

def is_semi_eulerian(graph):
    """Проверяет, является ли граф полуэйлеровым"""
    if not is_connected(graph):
        return False
    
    # Должно быть ровно 2 вершины с нечетной степенью
    odd_vertices = [v for v in graph if len(graph[v]) % 2 != 0]
    
    return len(odd_vertices) == 2

def analyze_eulerian(graph):
    """Анализирует граф на эйлеровость"""
    if is_eulerian(graph):
        return "ЭЙЛЕРОВ ГРАФ", "Все вершины имеют четную степень"
    elif is_semi_eulerian(graph):
        odd_vertices = [v for v in graph if len(graph[v]) % 2 != 0]
        return "ПОЛУЭЙЛЕРОВ ГРАФ", f"2 вершины с нечетной степенью: {', '.join(odd_vertices)}"
    else:
        odd_vertices = [v for v in graph if len(graph[v]) % 2 != 0]
        return "НЕ ЭЙЛЕРОВ", f"Вершин с нечетной степенью: {len(odd_vertices)} ({', '.join(odd_vertices)})"

# Program_Fleury_Algorithm.py
def is_connected(graph):
    """Проверка связности графа"""
    if not graph:
        return False
    visited = set()
    queue = [next(iter(graph))]
    visited.add(queue[0])
    
    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return len(visited) == len(graph)

def is_eulerian(graph):
    """Проверка эйлеровости"""
    if not is_connected(graph):
        return False
    return all(len(graph[v]) % 2 == 0 for v in graph) and len(graph) > 0

def fleury_algorithm(graph):
    """Поиск эйлерова цикла методом Флери"""
    if not is_eulerian(graph):
        return None
    
    # Создаём копию графа
    g = {v: set(graph[v]) for v in graph}
    # Начинаем с вершины нечётной степени (если есть) или любой
    start = next(iter(g))
    for v in g:
        if len(g[v]) % 2 == 1:
            start = v
            break
    
    circuit = []
    stack = [start]
    
    while stack:
        v = stack[-1]
        if g[v]:
            # Выбираем следующее ребро, которое НЕ является мостом (упрощенная версия)
            u = next(iter(g[v]))
            stack.append(u)
            # Удаляем ребро
            g[v].remove(u)
            g[u].remove(v)
        else:
            circuit.append(stack.pop())
    
    return circuit[::-1]

# Program_Hamiltonian_Check.py
def is_hamiltonian_bruteforce(graph):
    """Простая проверка гамильтоновости (для маленьких графов)"""
    vertices = list(graph.keys())
    n = len(vertices)
    
    if n < 2:
        return False
    
    def is_valid_cycle(cycle):
        """Проверяет, является ли цикл гамильтоновым"""
        if len(cycle) != n:
            return False
        
        # Проверяем все рёбра в цикле
        for i in range(n):
            v1 = cycle[i]
            v2 = cycle[(i + 1) % n]
            if v2 not in graph[v1]:
                return False
        
        return True
    
    # Генерация всех перестановок (для n ≤ 8)
    from itertools import permutations
    
    for perm in permutations(vertices):
        if is_valid_cycle(perm):
            return list(perm)
    
    return None

def is_hamiltonian_heuristic(graph):
    """Эвристическая проверка ( для больших графов - ограниченная)"""
    n = len(graph)
    if n < 2:
        return None
    
    # Проверка необходимого условия: степень каждой вершины >= n/2 (теорема Дирака)
    for v in graph:
        if len(graph[v]) < n / 2:
            return None
    
    return "Возможно гамильтонов (по теореме Дирака)"

# Program_Shortest_Path.py
def dijkstra(graph, start, end):
    """Алгоритм Дейкстры для взвешенного графа (веса = 1 для простоты)"""
    if start not in graph or end not in graph:
        return None, None
    
    # Инициализация
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    previous = {v: None for v in graph}
    unvisited = set(graph.keys())
    
    while unvisited:
        # Находим вершину с минимальным расстоянием
        current = min(unvisited, key=lambda v: distances[v])
        unvisited.remove(current)
        
        # Если текущая вершина - бесконечность, прерываем
        if distances[current] == float('inf'):
            break
        
        # Обновляем расстояния до соседей
        for neighbor in graph[current]:
            # Вес ребра = 1 (можно модифицировать)
            weight = 1
            new_dist = distances[current] + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
    
    # Восстанавливаем путь
    if distances[end] == float('inf'):
        return None, None
    
    # Построение пути
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path, distances

# Program_Reachability_Tree.py
def build_reachability_tree(graph, start):
    """Строит дерево достижимости от start"""
    if start not in graph:
        return None
    
    tree = {start: []}
    visited = {start}
    queue = [(start, None)]  # (вершина, родитель)
    
    while queue:
        vertex, parent = queue.pop(0)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                if parent is None:
                    tree[start].append(neighbor)
                else:
                    if vertex not in tree:
                        tree[vertex] = []
                    tree[vertex].append(neighbor)
                queue.append((neighbor, vertex))
    
    # Добавляем вершины без детей для визуализации
    for v in graph:
        if v not in tree:
            tree[v] = []
    
    return tree

def display_tree(tree, title):
    print(f"\n{title}:")
    print("-" * 40)
    for vertex in sorted(tree.keys()):
        if tree[vertex]:
            print(f"  {vertex} → {tree[vertex]}")
        else:
            print(f"  {vertex} → (лист)")
            
# Program_MaxFlow_FF.py
def bfs_find_path(residual, source, sink, parent):
    """Поиск увеличивающего пути в остаточной сети"""
    visited = {v: False for v in residual}
    queue = deque([source])
    visited[source] = True
    
    while queue:
        u = queue.popleft()
        
        for v in residual[u]:
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    
    return False

def max_flow_ford_fulkerson(graph, source, sink):
    """Алгоритм Форда-Фалкерсона для максимального потока"""
    # Создаем взвешенный граф (вес = 1 по умолчанию)
    vertices = list(graph.keys())
    residual = {v: {u: 0 for u in vertices} for v in vertices}
    
    # Заполняем остаточную сеть
    for v in graph:
        for u in graph[v]:
            residual[v][u] = 1  # пропускная способность
    
    parent = {}
    max_flow = 0
    
    while bfs_find_path(residual, source, sink, parent):
        # Находим минимальную пропускную способность в пути
        path_flow = float('inf')
        s = sink
        
        while s != source:
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]
        
        # Обновляем остаточную сеть
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = parent[v]
        
        max_flow += path_flow
        parent = {}
    
    return max_flow

# Program_Augmenting_Paths.py
def find_augmenting_paths(graph, source, sink):
    """Находит все простые увеличивающие пути"""
    all_paths = []
    visited_global = set()
    
    def dfs(current, target, path, visited):
        if current == target:
            all_paths.append(path[:])
            return
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, target, path + [neighbor], visited)
                visited.remove(neighbor)
    
    visited = {source}
    dfs(source, sink, [source], visited)
    
    return all_paths

def augmenting_path_method(graph, source, sink):
    """Метод увеличивающихся путей для максимального потока"""
    flow = 0
    paths = find_augmenting_paths(graph, source, sink)
    
    # Каждый путь увеличивает поток на 1
    flow = len(paths)
    
    return flow, paths

# Program_File_IO.py - онли загрука файла

# Program_Visualization.py - онли визуализация

# Program_Info_Display.py
def graph_info(graph):
    """Собирает всю информацию о графе"""
    if not graph:
        return "Граф пустой!"
    
    n_vertices = len(graph)
    n_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    # Статистика степеней
    degrees = [len(graph[v]) for v in graph]
    min_degree = min(degrees)
    max_degree = max(degrees)
    avg_degree = sum(degrees) / n_vertices
    
    # Веришны с min/max степенью
    min_vertices = [v for v in graph if len(graph[v]) == min_degree]
    max_vertices = [v for v in graph if len(graph[v]) == max_degree]
    
    # Плотность
    max_possible_edges = n_vertices * (n_vertices - 1) // 2
    density = n_edges / max_possible_edges if max_possible_edges > 0 else 0
    
    # Проверка на регулярность
    is_regular = len(set(degrees)) == 1
    
    # Компоненты связности
    components = find_connected_components(graph)
    is_connected = len(components) == 1
    
    info_str = []
    info_str.append("="*50)
    info_str.append("          ИНФОРМАЦИЯ О ГРАФЕ")
    info_str.append("="*50)
    info_str.append(f"Вершин:            {n_vertices}")
    info_str.append(f"Рёбер:             {n_edges}")
    info_str.append(f"Минимальная степень: {min_degree} (вершины: {', '.join(min_vertices)})")
    info_str.append(f"Максимальная степень: {max_degree} (вершины: {', '.join(max_vertices)})")
    info_str.append(f"Средняя степень:   {avg_degree:.2f}")
    info_str.append(f"Плотность:         {density:.2%}")
    info_str.append(f"Регулярный:        {'Да' if is_regular else 'Нет'}")
    info_str.append(f"Связный:           {'Да' if is_connected else 'Нет'}")
    info_str.append(f"Компонент связности: {len(components)}")
    
    if not is_connected:
        for i, comp in enumerate(components, 1):
            info_str.append(f"  Компонента {i}: {', '.join(comp)} ({len(comp)} вершин)")
    
    info_str.append("="*50)
    
    return "\n".join(info_str)

def find_connected_components(graph):
    """Поиск компонент связности (для info)"""
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = []
            queue = [vertex]
            visited.add(vertex)
            
            while queue:
                v = queue.pop(0)
                component.append(v)
                
                for neighbor in graph[v]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(sorted(component))
    
    return sorted(components, key=len, reverse=True)
