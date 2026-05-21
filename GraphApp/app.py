from bottle import route, run, request, template, static_file
import time
import json
from collections import deque

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
       
        # Получение данных из формы
        


        algorithm = request.forms.get('algorithm')
        n = int(request.forms.get('n'))
        matrix_str = request.forms.get('matrix')
        start = int(request.forms.get('start'))

      
        # Парсинг матрицы смежности
       
        if algorithm == 'dfs':
            algorithm_name = 'DFS (обход в глубину)'
        elif algorithm == 'bfs':
            algorithm_name = 'BFS (обход в ширину)'
        matrix = []

        rows = matrix_str.strip().split('\n')

        for row in rows:
            row = row.strip()

            if row:
                matrix.append([int(x) for x in row.split()])

        
        # Проверка размерности матрицы
       
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

     
        # Проверка стартовой вершины
        

        if start < 1 or start > n:
            return template(
                'error',
                message='Ошибка: неверная стартовая вершина'
            )

        
        # Запуск алгоритма в зависимости от выбора
        

        start_time = time.time()

        visited = [False] * (n + 1)
        parent = [0] * (n + 1)

        tree_edges = []
        traversal_order = []  

        if algorithm == 'dfs':
            # Реализация DFS
            stack = [start]
            visited[start] = True

            while stack:
                u = stack.pop()
                traversal_order.append(u)

                for v in range(1, n + 1):
                    if matrix[u - 1][v - 1] == 1 and not visited[v]:
                        visited[v] = True
                        parent[v] = u
                        tree_edges.append((u, v))
                        stack.append(v)

            algorithm_name = 'DFS (обход в глубину)'

        elif algorithm == 'bfs':
            # Реализация BFS
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

            algorithm_name = 'BFS (обход в ширину)'

        else:  # algorithm == 'coloring'
            
            pass

        execution_time = round(
            (time.time() - start_time) * 1000,
            2
        )

   
        # Проверка связности графа
   
        if not all(visited[1:]):
            return template(
                'error',
                message='Граф несвязен. Остовное дерево не существует.'
            )

        
        # Матрица остовного дерева
        

        tree_matrix = [[0] * n for _ in range(n)]

        for u, v in tree_edges:
            tree_matrix[u - 1][v - 1] = 1
            tree_matrix[v - 1][u - 1] = 1

        # Список рёбер исходного графа
       

        edges = []

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    edges.append((i + 1, j + 1))

        # Вершины графа
       

        vertices = list(range(1, n + 1))


        # Рендер страницы результата
      
        vertices_json = json.dumps(vertices)
        edges_json = json.dumps(edges)
        tree_edges_json = json.dumps(tree_edges)
        tree_matrix_json = json.dumps(tree_matrix)
        return template(
            'result',
            algorithm_name=algorithm_name,
            n=n,
            start=start,
            tree_matrix=tree_matrix,
            tree_edges=tree_edges,
            traversal_order=traversal_order,
            execution_time=execution_time,
            vertices_json=json.dumps(vertices),
            edges_json=json.dumps(edges),
            tree_edges_json=json.dumps(tree_edges),
            tree_matrix_json=tree_matrix_json
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
@route('/upload', method='POST')
def upload_file():
    try:
        # Получаем загруженный файл
        upload = request.files.get('data_file')
        if not upload:
            return template('error', message='Файл не выбран')

        # Читаем содержимое файла
        file_content = upload.file.read().decode('utf-8')

        # Парсим JSON или текстовый формат
        if upload.filename.endswith('.json'):
            data = json.loads(file_content)
        else:
            # Для текстового формата: первая строка — n, вторая — start, далее — матрица
            lines = file_content.strip().split('\n')
            data = {
                'n': int(lines[0]),
                'start': int(lines[1]),
                'matrix': '\n'.join(lines[2:])
            }

        # Передаём данные в шаблон формы с предзаполненными полями
        return template('index_with_data', **data)

    except json.JSONDecodeError:
        return template('error', message='Ошибка: неверный формат JSON')
    except Exception as e:
        return template('error', message=f'Ошибка при загрузке файла: {str(e)}')


# Запуск сервера
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
