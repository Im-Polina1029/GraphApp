# algorithms/dfs.py
# Модуль DFS (обход в глубину) для построения остовного дерева

def dfs_recursive(u, matrix, n, visited, parent, tree_edges, dfs_order):
    """
    Рекурсивная функция DFS.
    """
    visited[u] = True
    dfs_order.append(u)
    
    # Перебираем всех соседей от 1 до n (по возрастанию)
    for v in range(1, n + 1):
        if matrix[u-1][v-1] == 1 and not visited[v]:
            parent[v] = u
            tree_edges.append((u, v))
            # Рекурсивно уходим в глубину
            dfs_recursive(v, matrix, n, visited, parent, tree_edges, dfs_order)


def dfs_spanning_tree(matrix, n, start):
    """
    DFS алгоритм для построения остовного дерева.
    
    Входные параметры:
        matrix: матрица смежности (list of lists)
        n: количество вершин
        start: стартовая вершина
    
    Возвращает словарь с ключами:
        tree_edges: список рёбер остовного дерева
        dfs_order: порядок обхода вершин
        visited: список посещённых вершин
        parent: список родительских вершин
    """
    # 1. Проверка корректности входных данных
    if not (0 < n < 21):
        raise ValueError("n должен быть в диапазоне (0;21)")
    
    if not (1 <= start <= n):
        raise ValueError(f"Стартовая вершина должна быть от 1 до {n}")
    
    # Проверка симметричности матрицы и нулей на диагонали
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError(f"matrix[{i+1}][{i+1}] должен быть равен 0")
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Матрица смежности должна быть симметричной")

    # 2. Инициализация (размер n+1, индексация с 1)
    visited = [False] * (n + 1)
    parent = [0] * (n + 1)
    tree_edges = []
    dfs_order = []

    # 3. Запуск рекурсивного DFS
    dfs_recursive(start, matrix, n, visited, parent, tree_edges, dfs_order)

    # 4. Проверка связности (все ли вершины посещены)
    if not all(visited[1:]):
        unvisited = [i for i in range(1, n + 1) if not visited[i]]
        raise ValueError(f"Граф несвязен. Не посещены вершины: {unvisited}")

    return {
        'tree_edges': tree_edges,
        'dfs_order': dfs_order,
        'visited': visited,
        'parent': parent
    }
