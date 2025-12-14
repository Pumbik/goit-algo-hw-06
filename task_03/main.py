import networkx as nx
import matplotlib.pyplot as plt

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
def add_line_edges(graph, stations, time_weight):
    for i in range(len(stations) - 1):
        graph.add_edge(stations[i], stations[i+1], weight=time_weight)

add_line_edges(G, red_line, 2)# 2 хв між станціями
add_line_edges(G, blue_line, 2)
add_line_edges(G, green_line, 2)

# зв'язки між лініями (переходи)
transfers = [
    ("Хрещатик", "Майдан Незалежності"),            # Перехід M1-M2
    ("Театральна", "Золоті Ворота"),                # Перехід M1-M3
    ("Площа Українських Героїв", "Палац Спорту")    # Перехід M2-M3
]
G.add_edges_from(transfers, weight=5)



def find_shortest_path_dijkstra(graph, start, end):
    try:
        # Знаходимо найкоротший шлях, враховуючи вагу 'weight'
        path = nx.dijkstra_path(graph, start, end, weight='weight')
        
        # Рахуємо загальну довжину (час) цього шляху
        total_time = nx.dijkstra_path_length(graph, start, end, weight='weight')
        
        return path, total_time
    except nx.NetworkXNoPath:
        return None, None

# Приклад: Шлях від Академмістечка до Либідської
start_station = "Академмістечко"
end_station = "Либідська"

path, time = find_shortest_path_dijkstra(G, start_station, end_station)

print(f"--- Найкоротший шлях (Дейкстра) ---")
print(f"Від: {start_station} -> До: {end_station}")
print(f"Маршрут: {path}")
print(f"Розрахунковий час: {time} хв")


# Найкоротші шляхи між ВСІМА вершинами 

print(f"\n--- Час доїзду від ст. 'Вокзальна' до інших станцій ---")
# single_source_dijkstra_path_length повертає словник {станція: час}
all_paths_from_vokzalna = nx.single_source_dijkstra_path_length(G, "Вокзальна", weight='weight')

# Сортуємо за часом (від найближчих до найдальших)
sorted_stations = sorted(all_paths_from_vokzalna.items(), key=lambda item: item[1])

print(f"{'Станція':<25} | {'Час (хв)':<10}")
print("-" * 40)
for station, t in sorted_stations:
    print(f"{station:<25} | {t:<10}")


# Візуалізація з підписами ваги
plt.figure(figsize=(12, 10))
pos = nx.kamada_kawai_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', edgecolors='black')
nx.draw_networkx_labels(G, pos, font_size=8)

nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')

# Додаємо підписи ваги на ребрах (скільки хвилин їхати)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("Метро з вагами ребер (Час проїзду)")
plt.axis("off")
plt.show()