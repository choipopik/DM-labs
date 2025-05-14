import numpy as np
from collections import deque
import copy

# Названия вершин
VERTEX_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Исходная матрица пропускных способностей
original_matrix = np.array([
    # A  B  C  D  E  F  G  H  I
    [0, 5, 9, 0, 0, 0, 0, 0, 4],  # A (исток)
    [0, 0, 2, 0, 0, 0, 2, 0, 2],  # B
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # C (сток)
    [0, 0, 0, 2, 0, 0, 0, 0, 0],  # D
    [0, 0, 0, 7, 0, 0, 0, 0, 0],  # E
    [0, 0, 2, 7, 7, 0, 0, 0, 0],  # F
    [0, 0, 7, 3, 3, 3, 0, 0, 0],  # G
    [0, 0, 7, 0, 0, 0, 7, 7, 0],  # H
    [0, 0, 4, 0, 0, 0, 2, 7, 0],  # I
])

# Функция для красивого вывода матрицы смежности
def print_matrix(matrix, title="Матрица смежности"):
    print(f"\n{title}:")
    print("   " + " ".join(VERTEX_NAMES))
    for i, row in enumerate(matrix):
        print(f"{VERTEX_NAMES[i]}: {' '.join(str(x).rjust(3) for x in row)}")

# Функция BFS для поиска пути в остаточной сети
def bfs(graph, s, t, parent):
    visited = [False] * len(graph)
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in range(len(graph)):
            if not visited[v] and graph[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                if v == t:
                    return True
    return False

# Алгоритм Форда-Фалкерсона
def ford_fulkerson(graph, source, sink):
    residual_graph = copy.deepcopy(graph)
    parent = [-1] * len(residual_graph)
    max_flow = 0

    while bfs(residual_graph, source, sink, parent):
        path_flow = float('inf')
        t = sink
        while t != source:
            path_flow = min(path_flow, residual_graph[parent[t]][t])
            t = parent[t]

        max_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]

    return max_flow, residual_graph

# Определение минимального разреза
def find_min_cut(residual_graph, source, original_graph):
    visited = [False] * len(residual_graph)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(len(residual_graph)):
            if residual_graph[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)

    left_partition = [VERTEX_NAMES[i] for i in range(len(visited)) if visited[i]]
    right_partition = [VERTEX_NAMES[i] for i in range(len(visited)) if not visited[i]]

    min_cut_edges = []
    for i in range(len(original_graph)):
        for j in range(len(original_graph[i])):
            if visited[i] and not visited[j] and original_graph[i][j] > 0:
                min_cut_edges.append((VERTEX_NAMES[i], VERTEX_NAMES[j], original_graph[i][j]))

    return left_partition, right_partition, min_cut_edges

# Генерация случайной матрицы
def generate_random_graph(matrix):
    random_graph = copy.deepcopy(matrix)
    for i in range(len(random_graph)):
        for j in range(len(random_graph[i])):
            if random_graph[i][j] > 0:
                random_graph[i][j] = np.random.randint(100, 1000)
    return random_graph


# === Выводим исходную матрицу ===
print_matrix(original_matrix, "Исходная матрица смежности")

# === Решение для исходной матрицы ===
max_flow_original, residual_graph_original = ford_fulkerson(original_matrix, 0, 2)
left_part_orig, right_part_orig, edges_orig = find_min_cut(residual_graph_original, 0, original_matrix)

print("\n=== Исходная сеть ===")
print(f"Максимальный поток: {max_flow_original}")
print("Минимальный разрез:")
print(f"Левая часть разреза (достижимые из истока): {left_part_orig}")
print(f"Правая часть разреза (недостижимые): {right_part_orig}")
print("Рёбра минимального разреза:")
for u, v, cap in edges_orig:
    print(f"  {u} -> {v}, пропускная способность: {cap}")

# === Выводим случайную матрицу ===
random_matrix = generate_random_graph(original_matrix)
print_matrix(random_matrix, "Случайная матрица смежности")

# === Решение для случайной матрицы ===
max_flow_random, residual_graph_random = ford_fulkerson(random_matrix, 0, 2)
left_part_rand, right_part_rand, edges_rand = find_min_cut(residual_graph_random, 0, random_matrix)

print("\n=== Сеть со случайными пропускными способностями ===")
print(f"Максимальный поток: {max_flow_random}")
print("Минимальный разрез:")
print(f"Левая часть разреза (достижимые из истока): {left_part_rand}")
print(f"Правая часть разреза (недостижимые): {right_part_rand}")
print("Рёбра минимального разреза:")
for u, v, cap in edges_rand:
    print(f"  {u} -> {v}, пропускная способность: {cap}")