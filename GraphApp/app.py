from bottle import route, run, request, template, static_file
import time
import json
import math

# Маршрут для статических файлов (CSS)
@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root='./static')

# ========== ФУНКЦИИ ДЛЯ ВИЗУАЛИЗАЦИИ (на Python, без JS) ==========

def calculate_positions(n, width=600, height=400):
    """
    Вычисляет координаты вершин на окружности.
    Возвращает список словарей с ключами 'x' и 'y'.
    """
    positions = []
    center_x = width / 2
    center_y = height / 2
    radius = 140
    
    for i in range(n):
        # Угол: равномерно распределяем вершины по окружности
        # Сдвиг -pi/2, чтобы первая вершина была сверху
        angle = (i * 2 * math.pi / n) - math.pi / 2
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append({'x': round(x, 2), 'y': round(y, 2)})
    
    return positions


def generate_svg(n, edges, tree_edges, positions, width=600, height=400):
    """
    Генерирует SVG-изображение графа.
    - edges: рёбра исходного графа (серые)
    - tree_edges: рёбра остовного дерева (синие жирные)
    - positions: координаты вершин
    """
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background: #fafafa; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">'
    
    # 1. Рисуем рёбра исходного графа (серые, тонкие)
    for u, v in edges:
        p1 = positions[u-1]
        p2 = positions[v-1]
        svg += f'<line x1="{p1["x"]}" y1="{p1["y"]}" x2="{p2["x"]}" y2="{p2["y"]}" stroke="#cbd5e0" stroke-width="2"/>'
    
    # 2. Рисуем рёбра остовного дерева (синие, жирные)
    for u, v in tree_edges:
        p1 = positions[u-1]
        p2 = positions[v-1]
        svg += f'<line x1="{p1["x"]}" y1="{p1["y"]}" x2="{p2["x"]}" y2="{p2["y"]}" stroke="#2563eb" stroke-width="5"/>'
    
    # 3. Рисуем вершины (круги с номерами)
    for i, pos in enumerate(positions):
        svg += f'''
        <circle cx="{pos["x"]}" cy="{pos["y"]}" r="22" fill="#667eea" stroke="white" stroke-width="3"/>
        <text x="{pos["x"]}" y="{pos["y"]}" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="16" font-weight="bold">{i+1}</text>
        '''
    
    svg += '</svg>'
    return svg


# ========== МАРШРУТЫ (ROUTES) ==========

# Главная страница (ввод данных + выбор алгоритма)
@route('/')
@route('/index')
def index():
    return template('index')


# Обучающие страницы
@route('/about-bfs')
def about_bfs():
    return template('about_bfs')


@route('/about-dfs')
def about_dfs():
    return template('about_dfs')


@route('/about-coloring')
def about_coloring():
    return template('about_coloring')


# Страница об авторах
@route('/authors')
def authors():
    return template('authors')


# Обработка формы (запуск алгоритма DFS)
@route('/compute', method='POST')
def compute():
    try:
        # ----- Получение данных из формы -----
        algorithm = request.forms.get('algorithm')
        n = int(request.forms.get('n'))
        matrix_str = request.forms.get('matrix')
        start = int(request.forms.get('start'))

        # ----- Парсинг матрицы смежности -----
        matrix = []
        rows = matrix_str.strip().split('\n')
        for row in rows:
            row = row.strip()
            if row:
                matrix.append([int(x) for x in row.split()])

        # ----- Проверка размерности матрицы -----
        if len(matrix) != n:
            return template(
                'error',
                message=f'Ошибка: количество строк ({len(matrix)}) не равно n={n}'
            )

        for row in matrix:
            if len(row) != n:
                return template(
                    'error',
                    message='Ошибка: матрица должна быть квадратной'
                )

        # ----- Проверка стартовой вершины -----
        if start < 1 or start > n:
            return template(
                'error',
                message='Ошибка: неверная стартовая вершина'
            )

        # ----- Запуск DFS (алгоритм обхода в глубину) -----
        start_time = time.time()

        visited = [False] * (n + 1)  # visited[0] не используется
        parent = [0] * (n + 1)       # parent[0] не используется
        tree_edges = []              # рёбра остовного дерева
        dfs_order = []               # порядок обхода вершин
        stack = [start]              # стек для DFS
        visited[start] = True

        while stack:
            u = stack.pop()          # достаём вершину с верхушки стека
            dfs_order.append(u)      # запоминаем порядок обхода

            # Перебираем всех соседей (от 1 до n, по возрастанию)
            for v in range(1, n + 1):
                if matrix[u - 1][v - 1] == 1 and not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    tree_edges.append((u, v))  # добавляем ребро в дерево
                    stack.append(v)             # кладём в стек для дальнейшего обхода

        execution_time = round((time.time() - start_time) * 1000, 2)

        # ----- Проверка связности графа -----
        if not all(visited[1:]):
            return template(
                'error',
                message='Граф несвязен. Остовное дерево не существует.'
            )

        # ----- Матрица остовного дерева -----
        tree_matrix = [[0] * n for _ in range(n)]
        for u, v in tree_edges:
            tree_matrix[u - 1][v - 1] = 1
            tree_matrix[v - 1][u - 1] = 1

        # ----- Список рёбер исходного графа (для визуализации) -----
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    edges.append((i + 1, j + 1))

        # ----- Вершины графа -----
        vertices = list(range(1, n + 1))

        # ----- ВИЗУАЛИЗАЦИЯ НА PYTHON (без JS) -----
        # Вычисляем позиции вершин
        positions = calculate_positions(n)
        # Генерируем SVG
        svg_graph = generate_svg(n, edges, tree_edges, positions)

        # ----- Рендер страницы результата -----
        return template(
            'result',
            algorithm_name='DFS (обход в глубину)',
            n=n,
            start=start,
            tree_matrix=tree_matrix,
            tree_edges=tree_edges,
            dfs_order=dfs_order,
            execution_time=execution_time,
            vertices=vertices,
            edges=edges,
            svg_graph=svg_graph  # передаём SVG в шаблон
        )

    except ValueError:
        return template(
            'error',
            message='Ошибка: вводите только числа'
        )
    except Exception as e:
        return template(
            'error',
            message=f'Ошибка: {str(e)}'
        )


# Запуск сервера
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)