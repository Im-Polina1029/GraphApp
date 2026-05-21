from bottle import route, run, request, template, static_file
import time
import json
import math
from collections import deque

# Импорт алгоритмов
from algorithms.bfs import bfs_spanning_tree
from algorithms.dfs import dfs_spanning_tree
from algorithms.coloring import greedy_coloring


# ========== ВИЗУАЛИЗАЦИЯ (для app.py) ==========

def get_all_edges(matrix, n):
    """Возвращает список всех рёбер исходного графа"""
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                edges.append((i + 1, j + 1))
    return edges


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
        start = int(request.forms.get('start'))

        # Парсинг матрицы
        matrix = []
        rows = matrix_str.strip().split('\n')
        for row in rows:
            row = row.strip()
            if row:
                matrix.append([int(x) for x in row.split()])

        if len(matrix) != n:
            return template('error', message=f'Ошибка: количество строк ({len(matrix)}) не равно n={n}')

        if start < 1 or start > n:
            return template('error', message='Ошибка: неверная стартовая вершина')

        start_time = time.time()

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

        elif algorithm == 'coloring':
            result = greedy_coloring(matrix, n)
            return template('result_coloring',
                algorithm_name='Раскраска вершин (жадный алгоритм)',
                n=n,
                colors=result['colors'],
                num_colors=result['num_colors'],
                matrix=matrix)

        else:
            return template('error', message='Неизвестный алгоритм')

        execution_time = round((time.time() - start_time) * 1000, 2)

        if not all(visited[1:]):
            return template('error', message='Граф несвязен. Остовное дерево не существует.')

        # Матрица остовного дерева
        tree_matrix = [[0] * n for _ in range(n)]
        for u, v in tree_edges:
            tree_matrix[u-1][v-1] = 1
            tree_matrix[v-1][u-1] = 1

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
    run(host='localhost', port=8080, debug=True, reloader=True)