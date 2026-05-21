# algorithms/bfs.py
# Модуль BFS (обход в ширину) для построения остовного дерева

from collections import deque


def bfs_spanning_tree(matrix, n, start):
    """
    BFS алгоритм для построения остовного дерева.
    
    Входные параметры:
        matrix: матрица смежности (list of lists)
        n: количество вершин
        start: стартовая вершина
    
    Возвращает словарь с ключами:
        tree_edges: список рёбер остовного дерева
        traversal_order: порядок обхода вершин
        visited: список посещённых вершин
        parent: список родительских вершин
    """
    # Инициализация
    visited = [False] * (n + 1)
    parent = [0] * (n + 1)
    tree_edges = []
    traversal_order = []
    
    # Реализация BFS (с очередью)
    queue = deque([start])
    visited[start] = True
    
    while queue:
        u = queue.popleft()
        traversal_order.append(u)
        
        for v in range(1, n + 1):
            if matrix[u - 1][v - 1] == 1 and not visited[v]:
                visited[v] = True
                parent[v] = u
                tree_edges.append((u, v))
                queue.append(v)
    
    return {
        'tree_edges': tree_edges,
        'traversal_order': traversal_order,
        'visited': visited,
        'parent': parent
    }
