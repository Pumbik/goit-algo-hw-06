import networkx as nx
import matplotlib.pyplot as plt

# для реалізації цієї задачі обрав смеху Київського метрополітену (але чуть образіну на три гілки)
# Вершини (Nodes): Станції метро.
# Ребра (Edges): Перегони між станціями (тунелі) та переходи між станціями.

G = nx.Graph()

# Червона гілка (М1)
red_line = [
    "Академмістечко", "Житомирська", "Святошин", "Нивки", 
    "Вокзальна", "Театральна", "Хрещатик", "Арсенальна", "Дніпро"
]

# Синя гілка (М2)
blue_line = [
    "Героїв Дніпра", "Мінська", "Оболонь", "Почайна", 
    "Майдан Незалежності", "Площа Українських Героїв", "Олімпійська", "Либідська"
]

# Зелена гілка (М3)
green_line = [
    "Сирець", "Дорогожичі", "Лук'янівська", 
    "Золоті Ворота", "Палац Спорту", "Кловська", "Печерська"
]

# Зв'язки всередині ліній
def add_line_edges(graph, stations):
    for i in range(len(stations) - 1):
        graph.add_edge(stations[i], stations[i+1], weight=1)

add_line_edges(G, red_line)
add_line_edges(G, blue_line)
add_line_edges(G, green_line)

# зв'язки між лініями (переходи)
transfers = [
    ("Хрещатик", "Майдан Незалежності"),            # Перехід M1-M2
    ("Театральна", "Золоті Ворота"),                # Перехід M1-M3
    ("Площа Українських Героїв", "Палац Спорту")    # Перехід M2-M3
]
G.add_edges_from(transfers, weight=1)

# --

def dfs_path_finder(graph, start, goal):
    try:
        # Створюємо дерево DFS, починаючи зі стартової вершини
        # Це дерево показує, як алгоритм обходив граф
        dfs_tree = nx.dfs_tree(graph, source=start)
        
        # Знаходимо шлях у цьому дереві (це і буде шлях DFS)
        path = nx.shortest_path(dfs_tree, source=start, target=goal)
        return path
    except nx.NetworkXNoPath:
        return None

def bfs_path_finder(graph, start, goal):
    try:
        return nx.shortest_path(graph, source=start, target=goal)
    except nx.NetworkXNoPath:
        return None

# пошук
start_station = "Академмістечко"
end_station = "Либідська"

print(f"--- Шукаємо шлях від '{start_station}' до '{end_station}' ---")

# DFS
dfs_path = dfs_path_finder(G, start_station, end_station)
print(f"\nDFS (Глибина): {dfs_path}")
if dfs_path:
    print(f"Довжина шляху DFS: {len(dfs_path) - 1} переходів")

# BFS
bfs_path = bfs_path_finder(G, start_station, end_station)
print(f"\nBFS (Ширина): {bfs_path}")
if bfs_path:
    print(f"Довжина шляху BFS: {len(bfs_path) - 1} переходів")

plt.figure(figsize=(10, 8))
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=500, font_size=8)
plt.title("Транспортна мережа Києва")
plt.show()