% rebase('base')

<h1>GraphApp</h1>
<div class="subtitle">
    Исследуйте графы с помощью BFS, DFS и раскраски вершин
</div>

<form action="/compute" method="post" id="graphForm">
    <label>Выберите алгоритм</label>
    <select name="algorithm" id="algorithmSelect">
        <option value="bfs">BFS — обход в ширину (остовное дерево)</option>
        <option value="dfs">DFS — обход в глубину (остовное дерево)</option>
        <option value="coloring">Раскраска вершин (жадный алгоритм + обратный поиск)</option>
    </select>

    <label>Количество вершин (1–20)</label>
    <input type="number" name="n" min="1" max="20" value="{{n}}" required>

    <label>Матрица смежности</label>
    <textarea name="matrix" rows="5" required>{{matrix}}</textarea>
    <small>Вводите числа через пробел, строки разделяйте переносом</small>

    <label id="startLabel">📍 Стартовая вершина (для BFS и DFS)</label>
    <input type="number" name="start" id="startInput" min="1" value="{{start}}" required>

    <button type="submit" class="btn-primary algorithm-submit">▶ Запустить алгоритм</button>
</form>

<div style="margin-top: 1rem;">
    <a href="/" class="example-btn">⬅️ Вернуться к пустой форме</a>
</div>

<script>
    function updateStartInputState() {
        const algorithm = document.getElementById('algorithmSelect').value;
        const startInput = document.getElementById('startInput');
        const startLabel = document.getElementById('startLabel');

        if (algorithm === 'coloring') {
            startInput.required = false;
            startInput.disabled = true;
            startInput.value = '';
            startLabel.textContent = '📍 Стартовая вершина не требуется для раскраски';
        } else {
            startInput.required = true;
            startInput.disabled = false;
            startLabel.textContent = '📍 Стартовая вершина (для BFS и DFS)';
        }
    }

    document.getElementById('algorithmSelect').addEventListener('change', updateStartInputState);
    updateStartInputState();
</script>
