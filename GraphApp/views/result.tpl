<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Результат</title>
    <link rel="stylesheet" href="/static/style/style.css">
</head>

<body>
<nav>
    <a href="/">🏠 Главная</a>
    <a href="/about-bfs">📖 BFS</a>
    <a href="/about-dfs">📖 DFS</a>
    <a href="/about-coloring">🎨 Раскраска</a>
    <a href="/authors">👥 Авторы</a>
</nav>

<main>
    <h1>Результат</h1>

<div class="subtitle">
    Алгоритм: <strong>{{algorithm_name}}</strong>
</div>

<div class="result-container">
    <!-- ВИЗУАЛИЗАЦИЯ -->
    <div class="graph-visualization">
        <h3>Визуализация графа</h3>
        <canvas id="graphCanvas" width="600" height="400"></canvas>
    </div>

    <!-- МАТРИЦА ОСТОВНОГО ДЕРЕВА -->
    <div class="card">
        <h3>📋 Матрица остовного дерева</h3>
        <div class="matrix-container">
            <table class="matrix-table">
                % for i in range(n):
                <tr>
                    % for j in range(n):
                    <td class="{{ 'matrix-cell-1' if tree_matrix[i][j] == 1 else '' }}">
                        {{tree_matrix[i][j]}}
                    </td>
                    % end
                </tr>
                % end
            </table>
        </div>
    </div>

    <!-- ИНФОРМАЦИЯ -->
    <div class="info-grid">
        <div class="card">
            <h3>📍 Стартовая вершина</h3>
            <p class="info-value">{{start}}</p>
        </div>
        <div class="card">
            <h3>🔄 Порядок обхода</h3>
            <p class="info-value">{{' → '.join(map(str, traversal_order))}}</p>
        </div>
        <div class="card">
            <h3>🔢 Рёбер в дереве</h3>
            <p class="info-value">{{len(tree_edges)}} / {{n - 1}}</p>
        </div>
    <div class="button-group">
    <a href="/" class="btn-primary">На главную</a>
    <button id="saveResult" class="btn-success">Сохранить результат</button>
</div>
</div>

<footer>GraphApp — учебный проект по теории графов</footer>

<script>
const vertices = {{vertices_json}};
const edges = {{edges_json}};
const treeEdges = {{tree_edges_json}};
const algorithmName = "{{algorithm_name}}";

const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');

const width = canvas.width;
const height = canvas.height;
const centerX = width / 2;
const centerY = height / 2;
const radius = 140;

// ПОЗИЦИИ ВЕРШИН
const positions = [];
for (let i = 0; i < vertices.length; i++) {
    const angle = (i * 2 * Math.PI / vertices.length) - Math.PI / 2;
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);
    positions.push({ x, y });
}

// ИСХОДНЫЙ ГРАФ (СЕРЫЙ)
ctx.strokeStyle = '#999';
ctx.lineWidth = 2;
for (const edge of edges) {
    const u = edge[0] - 1;
    const v = edge[1] - 1;
    ctx.beginPath();
    ctx.moveTo(positions[u].x, positions[u].y);
    ctx.lineTo(positions[v].x, positions[v].y);
    ctx.stroke();
}

// ОСТОВНОЕ ДЕРЕВО (ЦВЕТ ПО АЛГОРИТМУ)
let treeColor;
if (algorithmName.includes("BFS")) {
    treeColor = '#10b981'; // зелёный для BFS
} else {
    treeColor = '#2563eb'; // синий для DFS
}

ctx.strokeStyle = treeColor;
ctx.lineWidth = 5;
for (const edge of treeEdges) {
    const u = edge[0] - 1;
    const v = edge[1] - 1;
    ctx.beginPath();
    ctx.moveTo(positions[u].x, positions[u].y);
    ctx.lineTo(positions[v].x, positions[v].y);
    ctx.stroke();
}

// ВЕРШИНЫ
for (let i = 0; i < positions.length; i++) {
    const p = positions[i];
    ctx.beginPath();
    ctx.arc(p.x, p.y, 22, 0, Math.PI * 2);
    ctx.fillStyle = '#667eea';
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

// КНОПКА СОХРАНЕНИЯ
document.getElementById('saveResult').addEventListener('click', function() {
    const saveData = {
        algorithm: algorithmName,
        startVertex: {{start}},
        executionTime: "{{execution_time}} мс",
        treeEdgesCount: {{len(tree_edges)}},
        totalVertices: {{n}},
        traversalOrder: [{{','.join(map(str, traversal_order))}}],
        treeMatrix: {{tree_matrix_json}},
        originalEdges: {{edges_json}}
    };

    const jsonString = JSON.stringify(saveData, null, 2);
    const blob = new Blob([jsonString], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `graph_result_${algorithmName.replace(' ', '_')}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    const btn = document.getElementById('saveResult');
    const originalText = btn.textContent;
    btn.textContent = '✅ Сохранено!';
    setTimeout(() => {
        btn.textContent = originalText;
    }, 2000);
});
</script>

</body>
</html>
