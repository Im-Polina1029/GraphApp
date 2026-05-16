from bottle import route, run, request, template, static_file

# Маршрут для статических файлов (CSS)
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

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

# Заглушка для обработки формы (пока просто выводит, что алгоритм запущен)
@route('/compute', method='POST')
def compute():
    algorithm = request.forms.get('algorithm')
    n = request.forms.get('n')
    matrix = request.forms.get('matrix')
    start = request.forms.get('start')
    
    # Здесь позже будет вызов нужного алгоритма
    return f"""
    <h1>Результат (заглушка)</h1>
    <p><strong>Выбранный алгоритм:</strong> {algorithm}</p>
    <p><strong>Количество вершин:</strong> {n}</p>
    <p><strong>Матрица смежности:</strong></p>
    <pre>{matrix}</pre>
    <p><strong>Стартовая вершина (для BFS/DFS):</strong> {start}</p>
    <a href="/">Вернуться на главную</a>
    """

# Запуск сервера
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)