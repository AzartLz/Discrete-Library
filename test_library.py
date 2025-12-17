
from GraphLibrary import add_vertex, add_edge, degree, bfs_traversal, kruskal_mst

g = {}
for v in "ABCDE":
    add_vertex(g, v)
for e in ("AB", "BC", "CD", "DE", "EA"):
    add_edge(g, e[0], e[1])

print("Степень A :", degree(g, 'A'))
print("BFS из A  :", bfs_traversal(g, 'A'))
print("MST вес   :", kruskal_mst(g)[1])

print(" Библиотека работает!")