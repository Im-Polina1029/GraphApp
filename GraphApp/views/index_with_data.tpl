% rebase('base')

<h1>GraphApp</h1>
<div class="subtitle">
    Исследуйте графы с помощью BFS, DFS и раскраски вершин
</div>

<form action="/compute" method="post">
    <label>Выберите алгоритм</label>
    <select name="algorithm">
        <option value="bfs">BFS — обход в ширину (остовное дерево)</option>
        <option value="dfs">DFS — обход в глубину (остовное дерево)</option>
        <option value="coloring">Раскраска вершин (жадный алгоритм)</option>
    </select>

    <label>Количество вершин (1–20)</label>
    <input type="number" name="n" min="1" max="20" value="{{n}}" required>

    <label>Матрица смежности</label>
    <textarea name="matrix" rows="5" required>{{matrix}}</textarea>
    <small>Вводите числа через пробел, строки разделяйте переносом</small>

    <label>📍 Стартовая вершина (для BFS и DFS)</label>
    <input type="number" name="start" min="1" value="{{start}}" required>

    <button type="submit">Запустить алгоритм</button>
</form>

<!-- Кнопка для возврата к пустой форме -->
<div style="margin-top: 1rem;">
    <a href="/" class="example-btn">⬅️ Вернуться к пустой форме</a>
</div>
