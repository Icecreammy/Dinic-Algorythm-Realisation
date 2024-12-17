import random
import time
from collections import deque

def generate_random_graph(num_vertices, edge_probability, capacity_range=(1, 10)):
    """
    Генерирует случайный граф в виде матрицы смежности.

    :param num_vertices: Количество вершин.
    :param edge_probability: Вероятность создания ребра между вершинами.
    :param capacity_range: Диапазон возможных значений пропускных способностей рёбер.
    :return: Матрица смежности графа.
    """
    graph = [[0] * num_vertices for _ in range(num_vertices)]

    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j and random.random() < edge_probability:
                graph[i][j] = random.randint(*capacity_range)

    return graph


def bfs_level_graph(capacity, flow, source, sink):
    """
    BFS для построения уровневого графа.

    :param capacity: Матрица пропускных способностей.
    :param flow: Матрица потока.
    :param source: Исток.
    :param sink: Сток.
    :return: Массив уровней для вершин, либо None, если путь до стока не найден.
    """
    num_vertices = len(capacity)
    level = [-1] * num_vertices
    level[source] = 0

    queue = deque([source])

    while queue:
        current = queue.popleft()
        for neighbor in range(num_vertices):
            if level[neighbor] == -1 and flow[current][neighbor] < capacity[current][neighbor]:
                level[neighbor] = level[current] + 1
                queue.append(neighbor)

    return level if level[sink] != -1 else None


def send_flow(u, flow, capacity, level, sink, current_flow):
    """
    DFS для отправки потока по уровневому графу.

    :param u: Текущая вершина.
    :param flow: Матрица потока.
    :param capacity: Матрица пропускных способностей.
    :param level: Уровневый граф.
    :param sink: Сток.
    :param current_flow: Текущий поток.
    :return: Объём потока, который можно отправить.
    """
    if u == sink:
        return current_flow

    for v in range(len(capacity)):
        if level[v] == level[u] + 1 and flow[u][v] < capacity[u][v]:
            min_cap = min(current_flow, capacity[u][v] - flow[u][v])
            result = send_flow(v, flow, capacity, level, sink, min_cap)
            if result > 0:
                flow[u][v] += result
                flow[v][u] -= result
                return result

    return 0


def dinic_algorithm(capacity, source, sink):
    """
    Реализация алгоритма Диница для поиска максимального потока.

    :param capacity: Матрица пропускных способностей.
    :param source: Исток.
    :param sink: Сток.
    :return: Максимальный поток.
    """
    start_time = time.time()
    num_vertices = len(capacity)
    flow = [[0] * num_vertices for i in range(num_vertices)]
    max_flow = 0

    while True:
        level = bfs_level_graph(capacity, flow, source, sink)
        if level is None:
            break

        while True:
            pushed = send_flow(source, flow, capacity, level, sink, float('Inf'))
            if pushed == 0:
                break
            max_flow += pushed

    end_time = time.time()
    print(f"\nВреме выполнения программы {end_time - start_time} с")
    return max_flow


# Пример использования
if __name__ == "__main__":
    while True:
        print("Выберите тестирование (введите 1,2 или 3)")
        print("1. Простой тест на небольшом графе")
        print("2. Тест на нескольких графах с низкой плотностью и увеличивающимся количеством вершин")
        print("3. Тест на нескольких графах с увеличивающимся количеством вершин")
        print("4. Тест на нескольких графах с высокой плотностью и увеличивающимся количеством вершин")
        t = input()
        if t == '1':
            g = generate_random_graph(6, 0.4)
            print(*g, sep='\n')
            print(f"Максимальный поток: {dinic_algorithm(g, 0, len(g)-1)}")
        elif t == '2':
            for i in range(50, 501, 50):
                g = generate_random_graph(i, 0.125)
                print(f"Количество вершин: {i}, максимальный поток: {dinic_algorithm(g, 0, len(g)-1)}")
        elif t == '3':
            for i in range(50, 501, 50):
                g = generate_random_graph(i, 0.25)
                print(f"Количество вершин: {i}, максимальный поток: {dinic_algorithm(g, 0, len(g)-1)}")
        elif t == '4':
            for i in range(50, 501, 50):
                g = generate_random_graph(i, 0.5)
                print(f"Количество вершин: {i}, максимальный поток: {dinic_algorithm(g, 0, len(g)-1)}")
        else:
            print("Некорректный ввод")
            continue
        break
