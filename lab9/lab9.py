# Создание, анализ, раскраска графов.
import networkx as nx
# Визуализация графа
import matplotlib.pyplot as plt
# Обход графа
from collections import deque

# Исходные данные
edges = [
    (4, 13), (2, 8), (13, 16), (4, 12), (8, 13), (7, 9), (11, 14),
    (6, 12), (14, 16), (3, 13), (10, 14), (2, 6), (7, 15),
    (6, 14), (5, 10), (3, 14), (9, 13), (5, 16), (2, 10), (4, 5),
    (2, 3), (2, 16), (10, 13), (3, 7), (2, 4), (5, 8), (7, 16),
    (4, 14), (3, 12), (6, 13), (7, 11), (5, 15), (5, 11),
    (13, 15), (9, 12)
]

G = nx.Graph()
G.add_edges_from(edges)


# Проверка двудольности
def is_bipartite(graph):
    try:
        color = nx.bipartite.color(graph)
        return True, color
    except nx.NetworkXError:
        return False, None


bipartite, coloring = is_bipartite(G)
print(f"Граф двудольный: {bipartite}")

if not bipartite:
    cycles = list(nx.cycle_basis(G))
    edges_to_remove = set()
    for cycle in cycles:
        if len(cycle) % 2 != 0:
            edges_to_remove.add((cycle[0], cycle[1]))
    print(f"Удаляем рёбра: {edges_to_remove}")
    G.remove_edges_from(edges_to_remove)
    bipartite, coloring = is_bipartite(G)
    print(f"После удаления рёбер граф двудольный: {bipartite}")

if bipartite:
    left = {node for node in coloring if coloring[node] == 0}
    right = set(G.nodes()) - left
    print(f"Левая доля: {left}")
    print(f"Правая доля: {right}")
else:
    print("Не удалось сделать граф двудольным")
    exit()


# Форд-Фалкерсон
def ford_fulkerson_matching(graph, left, right):
    flow_network = nx.DiGraph()

    source = 'source'
    sink = 'sink'
    flow_network.add_node(source)
    flow_network.add_node(sink)

    for node in left:
        flow_network.add_edge(source, node, capacity=1)

    for node in right:
        flow_network.add_edge(node, sink, capacity=1)

    for u, v in graph.edges():
        if u in left and v in right:
            flow_network.add_edge(u, v, capacity=1)
        elif v in left and u in right:
            flow_network.add_edge(v, u, capacity=1)

    flow_value, flow_dict = nx.maximum_flow(flow_network, source, sink)

    matching = []
    for u in flow_dict:
        if u == source or u == sink:
            continue
        for v in flow_dict[u]:
            if v != sink and flow_dict[u][v] == 1:
                matching.append((u, v))

    return matching


# Алгоритм Куна
def kuhn_matching(graph, left, right):
    pair_U = {u: None for u in left}
    pair_V = {v: None for v in right}

    def dfs(u, visited):
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                if pair_V[v] is None or dfs(pair_V[v], visited):
                    pair_U[u] = v
                    pair_V[v] = u
                    return True
        return False

    for u in left:
        dfs(u, set())
    matching = [(u, v) for u, v in pair_U.items() if v is not None]
    return matching


ff_matching = ford_fulkerson_matching(G, left, right)
kuhn_matching = kuhn_matching(G, left, right)

print("\nНаибольшее паросочетание (Форд-Фалкерсон):")
print(ff_matching)
print(f"Размер: {len(ff_matching)}")

print("\nНаибольшее паросочетание (Кун):")
print(kuhn_matching)
print(f"Размер: {len(kuhn_matching)}")


def visualize_combined(graph, left, right, matching1, matching2, title1="Алгоритм 1", title2="Алгоритм 2"):
    plt.figure(figsize=(16, 8))

    # Используем bipartite_layout для лучшей визуализации
    pos = nx.bipartite_layout(graph, nodes=left)

    # Цвета
    color_map = []
    for node in graph:
        if node in left:
            color_map.append('skyblue')
        else:
            color_map.append('lightgreen')

    # Первый график — Форд-Фалкерсон
    plt.subplot(1, 2, 1)
    nx.draw_networkx_nodes(graph, pos, node_color=color_map, node_size=600)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1, alpha=0.7)
    nx.draw_networkx_edges(graph, pos, edgelist=matching1, edge_color='red', width=2.5)
    nx.draw_networkx_labels(graph, pos)
    plt.title(title1)
    plt.axis('off')

    # Второй график — Кун
    plt.subplot(1, 2, 2)
    nx.draw_networkx_nodes(graph, pos, node_color=color_map, node_size=600)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1, alpha=0.7)
    nx.draw_networkx_edges(graph, pos, edgelist=matching2, edge_color='red', width=2.5)
    nx.draw_networkx_labels(graph, pos)
    plt.title(title2)
    plt.axis('off')

    # Легенда
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='skyblue', edgecolor='black', label='Левая доля'),
        Patch(facecolor='lightgreen', edgecolor='black', label='Правая доля'),
        plt.Line2D([0], [0], color='red', lw=2, label='Паросочетание'),
        plt.Line2D([0], [0], color='gray', lw=1, label='Другие рёбра')
    ]
    plt.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4, frameon=False)

    plt.tight_layout()
    plt.show()


# Вызов объединённой визуализации
visualize_combined(G, left, right, ff_matching, kuhn_matching,
                   title1="Форд-Фалкерсон", title2="Алгоритм Куна")