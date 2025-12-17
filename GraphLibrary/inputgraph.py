# modules/inputgraph.py
import os
from typing import Dict, List

def read_graph_from_file(filename: str) -> Dict[str, List[str]]:
    """
    Универсальный ввод:
      – список смежности  A:B,C
      – матрица смежности  A,B,C  \n 0,1,1  \n 1,0,1  \n 1,1,0
      – матрица инцидентности  A,B,C  \n 0,1,1  \n 1,0,1  \n 1,1,0  \n 0,1,1
    Возвращает dict – список смежности (неориентированный граф).
    """
    try:
        with open(filename, encoding='utf-8') as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        print(f" Файл '{filename}' не найден")
        return {}
    except Exception as e:
        print(f" Ошибка чтения: {e}")
        return {}

    # 1. Если хотя бы одна строка содержит «:» — это список смежности
    if any(':' in ln for ln in lines):
        return _parse_adj_list(lines)

    # 2. Иначе это матрица: первую строку считаем заголовком вершин
    if len(lines) < 2:
        print(" Матрица должна содержать ≥ 2 строк")
        return {}

    vertices = [v.strip() for v in lines[0].split(',')]
    matrix   = [[int(x.strip()) for x in ln.split(',')] for ln in lines[1:]]

    # 2а. Квадратная → матрица смежности
    if len(matrix) == len(vertices):
        return _adj_matrix_to_list(vertices, matrix)

    # 2б. Прямоугольная → матрица инцидентности (строки = вершины, столбцы = рёбра)
    return _inc_matrix_to_list(vertices, matrix)


# ---------- парсеры ----------
def _parse_adj_list(lines: List[str]) -> Dict[str, List[str]]:
    """Старый парсер списка смежности с проверкой симметрии."""
    graph: Dict[str, List[str]] = {}
    for ln in lines:
        if ':' not in ln:
            continue
        v, neigh = ln.split(':', 1)
        v = v.strip()
        graph[v] = [n.strip() for n in neigh.split(',') if n.strip()]

    # сделать неориентированным
    for v in list(graph):
        for u in graph[v]:
            if u not in graph:
                graph[u] = []
            if v not in graph[u]:
                graph[u].append(v)
    return graph


def _adj_matrix_to_list(vertices: List[str], matrix: List[List[int]]) -> Dict[str, List[str]]:
    """Квадратная матрица → список смежности."""
    graph = {v: [] for v in vertices}
    for i, v in enumerate(vertices):
        for j, u in enumerate(vertices):
            if matrix[i][j] == 1 and v != u:
                graph[v].append(u)
    return graph


def _inc_matrix_to_list(vertices: List[str], matrix: List[List[int]]) -> Dict[str, List[str]]:
    """Матрица инцидентности (вершины × рёбра) → список смежности."""
    graph = {v: [] for v in vertices}
    n_edges = len(matrix[0]) if matrix else 0
    for edge_idx in range(n_edges):
        ends = [v for i, v in enumerate(vertices) if matrix[i][edge_idx] == 1]
        # строим неориентированное ребро
        for v in ends:
            for u in ends:
                if v != u and u not in graph[v]:
                    graph[v].append(u)
    return graph


# ---------- вывод ----------
def write_graph_to_file(graph: Dict[str, List[str]], filename: str) -> bool:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for v in sorted(graph):
                f.write(f"{v}:{','.join(sorted(graph[v]))}\n")
        print(f" Граф сохранён в {filename}")
        return True
    except Exception as e:
        print(f" Ошибка записи: {e}")
        return False