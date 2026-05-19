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

    <h1>📊 Результат</h1>

<div class="subtitle">
    Алгоритм: <strong>{{algorithm_name}}</strong>
</div>

<div class="result-container">

    <!-- Визуализация (SVG, сгенерированный на Python) -->
    <div class="graph-visualization">
        <h3>Визуализация графа</h3>
        <div style="text-align: center;">
            {{!svg_graph}}
        </div>
        <p style="font-size: 0.85rem; color: #666; text-align: center; margin-top: 0.5rem;">
            🔵 Синие жирные линии — рёбра остовного дерева<br>
            ⚪ Серые линии — остальные рёбра графа
        </p>
    </div>

    <!-- Матрица остовного дерева -->
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

    <!-- Информационные карточки -->
    <div class="info-grid">
        <div class="card">
            <h3>📍 Стартовая вершина</h3>
            <p class="info-value">{{start}}</p>
        </div>
        <div class="card">
            <h3>🌲 Порядок обхода DFS</h3>
            <p class="info-value">{{' → '.join(map(str, dfs_order))}}</p>
        </div>
        <div class="card">
            <h3>🔢 Рёбер в дереве</h3>
            <p class="info-value">{{len(tree_edges)}} / {{n - 1}}</p>
        </div>
    </div>

    <!-- Кнопка возврата -->
    <div style="display:flex; gap:1rem; justify-content:center; margin-top:2rem;">
        <a href="/" class="example-btn" style="text-decoration:none; padding:12px 20px;">🏠 На главную</a>
    </div>

</div>
</body>
</html>