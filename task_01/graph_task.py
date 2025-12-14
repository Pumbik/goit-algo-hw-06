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
        graph.add_edge(stations[i], stations[i+1], type='line')

add_line_edges(G, red_line)
add_line_edges(G, blue_line)
add_line_edges(G, green_line)

# зв'язки між лініями (переходи)
transfers = [
    ("Хрещатик", "Майдан Незалежності"),            # Перехід M1-M2
    ("Театральна", "Золоті Ворота"),                # Перехід M1-M3
    ("Площа Українських Героїв", "Палац Спорту")    # Перехід M2-M3
]
G.add_edges_from(transfers)

# --- ВІЗУАЛІЗАЦІЯ ---

plt.figure(figsize=(12, 10))
# layout для розміщення точок
pos = nx.spring_layout(G, seed=42) 

node_colors = []
for node in G.nodes():
    if node in red_line:
        node_colors.append('red')
    elif node in blue_line:
        node_colors.append('blue')
    elif node in green_line:
        node_colors.append('green')
    else:
        node_colors.append('gray')

nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, edgecolors='black')

# 2. Малюємо звичайні лінії метро (сірі)
# Відбираємо ребра, які НЕ є переходами
line_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') != 'transfer']
nx.draw_networkx_edges(G, pos, edgelist=line_edges, width=2, edge_color='gray')

# 3. Малюємо ПЕРЕХОДИ (Жовті та товсті)
# Відбираємо ребра, які Є переходами
transfer_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'transfer']
nx.draw_networkx_edges(G, pos, edgelist=transfer_edges, width=4, edge_color='orange', style='dashed')

# 4. Підписи
nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")

plt.title("Модель транспортної мережі (Метро)")
plt.axis("off") # Вимикаємо осі координат
plt.show()

# --- АНАЛІЗ ХАРАКТЕРИСТИК ---

print(f"{'='*30}")
print(f"АНАЛІЗ ГРАФА")
print(f"{'='*30}")

# Кількість вершин та ребер
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

print(f"Кількість станцій (вершин): {num_nodes}")
print(f"Кількість перегонів (ребер): {num_edges}")

# Degree
# Ступінь показує, скільки з'єднань має станція.
# Кінцеві станції матимуть ступінь 1. Звичайні - 2. Пересадочні - 3 або більше.
print(f"\nСтупінь вершин (ТОП-5 найважливіших вузлів):")
degrees = dict(G.degree())

# Сортуємо за кількістю зв'язків (від найбільшого)
sorted_degrees = sorted(degrees.items(), key=lambda item: item[1], reverse=True)

for station, degree in sorted_degrees[:5]:
    print(f"- {station}: {degree} зв'язків")

# Середній ступінь вершини
avg_degree = sum(dict(G.degree()).values()) / num_nodes
print(f"\nСередній ступінь вершини: {avg_degree:.2f}")