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
    <input type="number" name="n" min="1" max="20" placeholder="Например: 4" required>

    <label>Матрица смежности</label>
    <textarea name="matrix" rows="5" placeholder="0 1 1 0&#10;1 0 1 1&#10;1 1 0 0&#10;0 1 0 0" required></textarea>
    <small>Вводите числа через пробел, строки разделяйте переносом</small>

    <label>📍 Стартовая вершина (для BFS и DFS)</label>
    <input type="number" name="start" min="1" placeholder="Например: 1" required>

    <button type="submit">Запустить алгоритм</button>
</form>

</div>

<script>
    function loadExample() {
        document.querySelector('textarea[name="matrix"]').value = "0 1 1 0\n1 0 1 1\n1 1 0 0\n0 1 0 0";
        document.querySelector('input[name="n"]').value = "4";
        document.querySelector('input[name="start"]').value = "1";
    }
</script>