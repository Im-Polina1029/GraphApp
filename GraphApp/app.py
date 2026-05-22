from bottle import route, run, request, template, static_file
import time
import json
import os

# Импорт алгоритмов
from algorithms.bfs import bfs_spanning_tree
from algorithms.dfs import dfs_spanning_tree
from algorithms.coloring import greedy_coloring


# ========== ВИЗУАЛИЗАЦИЯ (для app.py) ==========

def get_all_edges(matrix, n):
    """Возвращает список всех рёбер исходного графа."""
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                edges.append((i + 1, j + 1))
    return edges


def parse_matrix(matrix_str, n):
    """Преобразует текстовую матрицу из формы в список списков."""
    matrix = []
    rows = matrix_str.strip().split('\n')
    for row in rows:
        row = row.strip()
        if row:
            matrix.append([int(x) for x in row.split()])

    if len(matrix) != n:
        raise ValueError(f'Количество строк ({len(matrix)}) не равно n={n}')

    for index, row in enumerate(matrix, start=1):
        if len(row) != n:
            raise ValueError(f'Строка {index} должна содержать ровно {n} элементов')

    return matrix


# ========== МАРШРУТЫ ==========

@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root='./static')


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
        algorithm = request.forms.get('algorithm')
        n = int(request.forms.get('n'))
        matrix_str = request.forms.get('matrix')
        matrix = parse_matrix(matrix_str, n)

        start_time = time.time()

        if algorithm == 'coloring':
            result = greedy_coloring(matrix, n)
            execution_time = round((time.time() - start_time) * 1000, 2)
            vertices = list(range(1, n + 1))
            all_edges = get_all_edges(matrix, n)

            return template('result_coloring',
                algorithm_name='Раскраска вершин: жадный алгоритм + обратный поиск',
                n=n,
                colors=result['colors'],
                num_colors=result['num_colors'],
                min_colors=result['min_colors'],
                greedy_colors=result['greedy_colors'],
                greedy_num_colors=result['greedy_num_colors'],
                order=result['order'],
                degrees=result['degrees'],
                checks=result['checks'],
                is_valid=result['is_valid'],
                execution_time=execution_time,
                matrix=matrix,
                vertices_json=json.dumps(vertices),
                edges_json=json.dumps(all_edges),
                colors_json=json.dumps(result['colors']))

        start = int(request.forms.get('start'))
        if start < 1 or start > n:
            return template('error', message='Ошибка: неверная стартовая вершина')

        if algorithm == 'dfs':
            result = dfs_spanning_tree(matrix, n, start)
            algorithm_name = 'DFS (обход в глубину)'
            traversal_order = result['dfs_order']
            tree_edges = result['tree_edges']
            visited = result['visited']

        elif algorithm == 'bfs':
            result = bfs_spanning_tree(matrix, n, start)
            algorithm_name = 'BFS (обход в ширину)'
            traversal_order = result['traversal_order']
            tree_edges = result['tree_edges']
            visited = result['visited']

        else:
            return template('error', message='Неизвестный алгоритм')

        execution_time = round((time.time() - start_time) * 1000, 2)

        if not all(visited[1:]):
            return template('error', message='Граф несвязен. Остовное дерево не существует.')

        # Матрица остовного дерева
        tree_matrix = [[0] * n for _ in range(n)]
        for u, v in tree_edges:
            tree_matrix[u - 1][v - 1] = 1
            tree_matrix[v - 1][u - 1] = 1

        vertices = list(range(1, n + 1))
        all_edges = get_all_edges(matrix, n)

        return template('result',
            algorithm_name=algorithm_name,
            n=n,
            start=start,
            tree_matrix=tree_matrix,
            tree_edges=tree_edges,
            traversal_order=traversal_order,
            execution_time=execution_time,
            vertices_json=json.dumps(vertices),
            edges_json=json.dumps(all_edges),
            tree_edges_json=json.dumps(tree_edges),
            tree_matrix_json=json.dumps(tree_matrix))

    except ValueError as e:
        return template('error', message=f'Ошибка ввода: {str(e)}')
    except Exception as e:
        return template('error', message=f'Ошибка: {str(e)}')


@route('/upload', method='POST')
def upload_file():
    try:
        upload = request.files.get('data_file')
        if not upload:
            return template('error', message='Файл не выбран')

        file_content = upload.file.read().decode('utf-8')

        if upload.filename.endswith('.json'):
            data = json.loads(file_content)
        else:
            lines = file_content.strip().split('\n')
            data = {
                'n': int(lines[0]),
                'start': int(lines[1]),
                'matrix': '\n'.join(lines[2:])
            }

        return template('index_with_data', **data)

    except json.JSONDecodeError:
        return template('error', message='Ошибка: неверный формат JSON')
    except Exception as e:
        return template('error', message=f'Ошибка при загрузке файла: {str(e)}')


# ========== ЗАПУСК ==========

if __name__ == '__main__':
    host = os.environ.get('GRAPHAPP_HOST', 'localhost')
    port = int(os.environ.get('GRAPHAPP_PORT', '8080'))
    run(host=host, port=port, debug=True, reloader=True)
