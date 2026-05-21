from bottle import route, run, request, template, static_file
import time
import json
import math

# Маршрут для статических файлов (CSS)
@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root='./static')


# функция для визуализации

def calculate_positions(n, width=600, height=400):
    """Вычисляет координаты вершин"""
    positions = []
    center_x = width / 2
    center_y = height / 2
    radius = 140
    
    for i in range(n):
        angle = (i * 2 * math.pi / n) - math.pi / 2 # вычисляет угол в радианах для каждой точки
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append({'x': round(x, 2), 'y': round(y, 2)})
    
    return positions


def generate_svg(n, all_edges, tree_edges, positions, width=600, height=400):
    """Генерирует SVG с исходным графом и остовным деревом"""
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background: #fafafa; border-radius: 16px;">'
    
    # Рёбра исходного графа (серые)
    for u, v in all_edges:
        p1 = positions[u-1]
        p2 = positions[v-1]
        svg += f'<line x1="{p1["x"]}" y1="{p1["y"]}" x2="{p2["x"]}" y2="{p2["y"]}" stroke="#cbd5e0" stroke-width="2"/>'
    
    # Рёбра остовного дерева (синие жирные)
    for u, v in tree_edges:
        p1 = positions[u-1]
        p2 = positions[v-1]
        svg += f'<line x1="{p1["x"]}" y1="{p1["y"]}" x2="{p2["x"]}" y2="{p2["y"]}" stroke="#2563eb" stroke-width="5"/>'
    
    # Вершины
    for i, pos in enumerate(positions):
        svg += f'''
        <circle cx="{pos["x"]}" cy="{pos["y"]}" r="22" fill="#667eea" stroke="white" stroke-width="3"/>
        <text x="{pos["x"]}" y="{pos["y"]}" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="16" font-weight="bold">{i+1}</text>
        '''
    
    svg += '</svg>'
    return svg


# алгоритм DFS (рекурсивный, правильный обход в глубину) 

def dfs_recursive(u, matrix, n, visited, parent, tree_edges, dfs_order):
    
    visited[u] = True
    dfs_order.append(u)
    
    # Перебираем всех соседей от 1 до n (по возрастанию)
    for v in range(1, n + 1):
        if matrix[u-1][v-1] == 1 and not visited[v]:
            parent[v] = u
            tree_edges.append((u, v))
            # Рекурсивно уходим в глубину
            dfs_recursive(v, matrix, n, visited, parent, tree_edges, dfs_order)


def compute_spanning_tree(matrix, n, start):
    """
    Запускает рекурсивный DFS для построения остовного дерева.
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

    # 5. Построение матрицы остовного дерева
    tree_matrix = [[0] * n for _ in range(n)]
    for u, v in tree_edges:
        tree_matrix[u-1][v-1] = 1
        tree_matrix[v-1][u-1] = 1

    # 6. Список всех рёбер исходного графа (для визуализации)
    all_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                all_edges.append((i + 1, j + 1))

    return {
        "tree_matrix": tree_matrix,
        "tree_edges": tree_edges,
        "all_edges": all_edges,
        "dfs_order": dfs_order,
        "visited": visited,
        "parent": parent
    }


# маршруты

@route('/')
@route('/index')
def index():
    return template('index')


@route('/about-bfs')
def about_bfs():
    return template('about_bfs')


@route('/about-dfs')
def about_dfs():
    return template('about_dfs')


@route('/about-coloring')
def about_coloring():
    return template('about_coloring')


@route('/authors')
def authors():
    return template('authors')


@route('/compute', method='POST')
def compute():
    try:
        start_time = time.time()

        # Получение данных из формы
        algorithm = request.forms.get('algorithm')
        n = int(request.forms.get('n'))
        matrix_str = request.forms.get('matrix')
        start = int(request.forms.get('start'))

        # Парсинг матрицы
        matrix = []
        rows = matrix_str.strip().split('\n')
        for row in rows:
            row = row.strip()
            if row:
                matrix.append([int(x) for x in row.split()])

        # Проверка размерности
        if len(matrix) != n:
            return template('error', message=f"Ошибка: количество строк ({len(matrix)}) не равно n={n}")

        # Запуск алгоритма
        result = compute_spanning_tree(matrix, n, start)

        execution_time = round((time.time() - start_time) * 1000, 2)

        # Визуализация (SVG)
        positions = calculate_positions(n)
        svg_graph = generate_svg(n, result["all_edges"], result["tree_edges"], positions)

        return template(
            'result',
            algorithm_name='DFS (обход в глубину)',
            n=n,
            start=start,
            tree_matrix=result["tree_matrix"],
            tree_edges=result["tree_edges"],
            dfs_order=result["dfs_order"],
            execution_time=execution_time,
            svg_graph=svg_graph
        )

    except ValueError as e:
        return template('error', message=str(e))
    except Exception as e:
        return template('error', message=f'Ошибка: {str(e)}')


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)