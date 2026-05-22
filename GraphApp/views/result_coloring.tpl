% rebase('base')

<h1>🎨 Результат раскраски вершин</h1>
<div class="subtitle">
    Алгоритм: <strong>{{algorithm_name}}</strong>
</div>

<div class="result-container">
    <div class="graph-visualization card">
        <h3>Визуализация раскрашенного графа</h3>
        <canvas id="graphCanvas" width="600" height="420"></canvas>
    </div>

    <div class="info-grid">
        <div class="card">
            <h3>Минимальное количество цветов</h3>
            <p class="info-value">{{num_colors}}</p>
        </div>
        <div class="card">
            <h3>Жадная оценка</h3>
            <p class="info-value">{{greedy_num_colors}}</p>
        </div>
        <div class="card">
            <h3>Корректность раскраски</h3>
            <p class="info-value">{{'Да' if is_valid else 'Нет'}}</p>
        </div>
    </div>

    <div class="card">
        <h3>Цвета вершин</h3>
        <table class="matrix-table">
            <tr>
                <th>Вершина</th>
                <th>Цвет</th>
                <th>Степень вершины</th>
            </tr>
            % for i in range(n):
            <tr>
                <td>{{i + 1}}</td>
                <td>{{colors[i]}}</td>
                <td>{{degrees[i + 1]}}</td>
            </tr>
            % end
        </table>
    </div>

    <div class="card">
        <h3>Порядок обработки вершин</h3>
        <p class="info-value">{{' → '.join(map(str, order))}}</p>
    </div>

    <div class="card">
        <h3>Проверки обратного поиска</h3>
        <table class="matrix-table">
            <tr>
                <th>Количество цветов k</th>
                <th>Результат</th>
                <th>Количество шагов</th>
            </tr>
            % for item in checks:
            <tr>
                <td>{{item['k']}}</td>
                <td>{{'раскраска найдена' if item['success'] else 'раскраска не найдена'}}</td>
                <td>{{item['steps']}}</td>
            </tr>
            % end
        </table>
    </div>

    <div class="button-group">
        <a href="/" class="btn-primary">На главную</a>
    </div>
</div>

<script>
const vertices = {{vertices_json}};
const edges = {{edges_json}};
const colors = {{colors_json}};
const palette = [
    '#ef4444', '#3b82f6', '#22c55e', '#f59e0b', '#a855f7',
    '#14b8a6', '#f97316', '#64748b', '#ec4899', '#84cc16'
];

const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;
const centerX = width / 2;
const centerY = height / 2;
const radius = Math.min(width, height) / 2 - 70;

const positions = [];
for (let i = 0; i < vertices.length; i++) {
    const angle = (i * 2 * Math.PI / vertices.length) - Math.PI / 2;
    positions.push({
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
    });
}

ctx.strokeStyle = '#94a3b8';
ctx.lineWidth = 2;
for (const edge of edges) {
    const u = edge[0] - 1;
    const v = edge[1] - 1;
    ctx.beginPath();
    ctx.moveTo(positions[u].x, positions[u].y);
    ctx.lineTo(positions[v].x, positions[v].y);
    ctx.stroke();
}

for (let i = 0; i < positions.length; i++) {
    const p = positions[i];
    const colorIndex = (colors[i] - 1) % palette.length;

    ctx.beginPath();
    ctx.arc(p.x, p.y, 24, 0, Math.PI * 2);
    ctx.fillStyle = palette[colorIndex];
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = 'white';
    ctx.stroke();

    ctx.fillStyle = 'white';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(vertices[i], p.x, p.y);
}
</script>
