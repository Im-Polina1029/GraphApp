% rebase('base')

<h1>GraphApp</h1>

<form action="/compute" method="post">
    <label>Алгоритм:</label>
    <select name="algorithm">
        <option value="bfs">BFS (обход в ширину)</option>
        <option value="dfs">DFS (обход в глубину)</option>
        <option value="coloring">Раскраска вершин</option>
    </select>

    <label>Количество вершин (1–20):</label>
    <input type="number" name="n" min="1" max="20" required>

    <label>Матрица смежности:</label>
    <textarea name="matrix" rows="5" cols="40" placeholder="0 1 1 0&#10;1 0 1 1&#10;1 1 0 0&#10;0 1 0 0" required></textarea>

    <label>Стартовая вершина:</label>
    <input type="number" name="start" min="1" required>

    <button type="submit">Запустить</button>
</form>