from bottle import route, run, request, template, static_file
import time
import json

# Маршрут для статических файлов (CSS)
@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root='./static')

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

# Обработка формы (запуск алгоритма)
@route('/compute', method='POST')
def compute():
    try:
        # =========================================
        # Получение данных из формы
        # =========================================

        algorithm = request.forms.get('algorithm')
        n = int(request.forms.get('n'))
        matrix_str = request.forms.get('matrix')
        start = int(request.forms.get('start'))

        # =========================================
        # Парсинг матрицы смежности
        # =========================================

        matrix = []

        rows = matrix_str.strip().split('\n')

        for row in rows:
            row = row.strip()

            if row:
                matrix.append([int(x) for x in row.split()])

        # =========================================
        # Проверка размерности матрицы
        # =========================================

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

        # =========================================
        # Проверка стартовой вершины
        # =========================================

        if start < 1 or start > n:
            return template(
                'error',
                message='Ошибка: неверная стартовая вершина'
            )

        # =========================================
        # Запуск DFS
        # =========================================

        start_time = time.time()

        visited = [False] * (n + 1)
        parent = [0] * (n + 1)

        tree_edges = []
        dfs_order = []

        stack = [start]
        visited[start] = True

        while stack:
            u = stack.pop()

            dfs_order.append(u)

            for v in range(1, n + 1):

                if matrix[u - 1][v - 1] == 1 and not visited[v]:

                    visited[v] = True
                    parent[v] = u

                    tree_edges.append((u, v))

                    stack.append(v)

        execution_time = round(
            (time.time() - start_time) * 1000,
            2
        )

        # =========================================
        # Проверка связности графа
        # =========================================

        if not all(visited[1:]):

            return template(
                'error',
                message='Граф несвязен. Остовное дерево не существует.'
            )

        # =========================================
        # Матрица остовного дерева
        # =========================================

        tree_matrix = [[0] * n for _ in range(n)]

        for u, v in tree_edges:

            tree_matrix[u - 1][v - 1] = 1
            tree_matrix[v - 1][u - 1] = 1

        # =========================================
        # Список рёбер исходного графа
        # =========================================

        edges = []

        for i in range(n):
            for j in range(i + 1, n):

                if matrix[i][j] == 1:
                    edges.append((i + 1, j + 1))

        # =========================================
        # Вершины графа
        # =========================================

        vertices = list(range(1, n + 1))

        # =========================================
        # Рендер страницы результата
        # =========================================

        return template(
            'result',

            algorithm_name='DFS (обход в глубину)',

            n=n,
            start=start,

            tree_matrix=tree_matrix,
            tree_edges=tree_edges,

            dfs_order=dfs_order,

            execution_time=execution_time,

            vertices_json=json.dumps(vertices),
            edges_json=json.dumps(edges),
            tree_edges_json=json.dumps(tree_edges)
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