# 📚 GraphLibrary  
**Учебная библиотека по дискретной математике – теория графов**  
**Python ≥ 3.8** | **UTF-8** | **pip-installable**

---

##  Установка

### Локально (без pip)
```bash
git clone https://github.com/ВАШ_ЛОГИН/GraphLibrary.git
cd GraphLibrary
pip install -e .
```

### Или просто добавьте путь
```python
import sys, os
sys.path.append('путь/к/GraphLibrary')
from GraphLibrary import add_vertex, bfs_traversal, ...
```

---

##  Структура пакета

```
GraphLibrary/
├── __init__.py              # import GraphLibrary as gl
├── GraphLibrary.py          # 33 функции + вспомогательные классы
├── inputgraph.py            # универсальный ввод/вывод графов
└── vizgraph.py              # визуализация на matplotlib
```

---

##  Поддерживаемые форматы графов

**Один и тот же код** работает с **любым** форматом:

| Формат | Пример файла |
|--------|--------------|
| **Список смежности** | `A:B,C\nB:A,D` |
| **Матрица смежности** | `A,B,C\n0,1,1\n1,0,1` |
| **Матрица инцидентности** | `A,B,C\n1,1,0\n1,0,1` |

---

##  Быстрый старт

```python
from GraphLibrary import read_graph_from_file, degree, bfs_traversal, kruskal_mst

# 1. Загружаем граф
graph = read_graph_from_file('test_data/my_graph.txt')

# 2. Работаем как с обычным dict
print("Степень A:", degree(graph, 'A'))
print("BFS:", bfs_traversal(graph, 'A'))
print("Вес MST:", kruskal_mst(graph)[1])
```

---

##  Полный список функций

| Раздел | Функции |
|--------|---------|
| **Базовые операции** | `add_vertex`, `remove_vertex`, `add_edge`, `remove_edge`, `degree` |
| **Представления** | `adjacency_matrix`, `incidence_matrix`, `adjacency_list` |
| **Изоморфизм** | `is_isomorphic`, `union`, `intersection`, `composition`, `reverse_edges`, `complement` |
| **Связность** | `connected_components`, `find_path`, `find_cycle`, `diameter`, `radius`, `acyclic_check` |
| **Обходы** | `bfs_traversal`, `dfs_traversal`, `is_eulerian`, `is_semi_eulerian`, `fleury_algorithm`, `is_hamiltonian` |
| **Кратчайшие пути** | `shortest_path_dijkstra`, `build_reachability_tree` |
| **Потоки** | `max_flow_ford_fulkerson`, `augmenting_path_method` |
| **Деревья** | `kruskal_mst`, `build_reachability_tree` |
| **Утилиты** | `read_graph_from_file`, `write_graph_to_file`, `visualize_graph` |

---

##  Пример вывода

```
[1] Загрузка графа из demo_graph.txt
[2] Информация о графе:
   Всего вершин: 8
   Всего рёбер: 12
[3] Степени вершин:
   deg(A) = 3
   deg(B) = 4
   ...
[4] Компоненты связности (1):
   Компонента 1: A,B,C,D,E,F,G,H
[5] BFS из 'A':
   Порядок обхода: A → B → C → D → E → F → G → H
[6] Минимальное остовное дерево:
   Общий вес: 7
   Рёбра MST: A-B, A-C, A-D, B-E, C-F, D-G, E-H
[7] Визуализация...
```
(откроются 2 окна matplotlib)

---

##  Тестирование

```bash
python -m pytest tests/    # если добавите тесты
# или просто:
python main.py             # демонстрация 5 функций
```

---

##  Лицензия

MIT © 2024 – свободно для учебных и научных целей.

---

