% rebase('base', template_name='authors')

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Об авторах | GraphApp</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e9edf2 100%);
            color: #2c3e50;
            line-height: 1.6;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 1.5rem;
            box-shadow: 0 20px 35px -10px rgba(0,0,0,0.1);
            overflow: hidden;
            padding: 2rem;
        }

        h1 {
            font-size: 2.5rem;
            border-left: 5px solid #3498db;
            padding-left: 1rem;
            margin-bottom: 2rem;
            color: #2c3e50;
        }

        .team-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .card {
            background: #ffffff;
            border-radius: 1rem;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #eef2f7;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 30px -12px rgba(0,0,0,0.15);
        }

        .card-header {
            background: #3498db;
            color: white;
            padding: 1rem;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
        }

        .card-body {
            padding: 1.5rem;
        }

        .role {
            font-weight: bold;
            color: #3498db;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }

        .contribution {
            margin-top: 0.8rem;
            font-size: 0.9rem;
            color: #4a627a;
            border-top: 1px dashed #e2e8f0;
            padding-top: 0.8rem;
        }

        .github-link {
            display: inline-block;
            margin-top: 1rem;
            color: #2c3e50;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }

        .github-link:hover {
            color: #3498db;
        }

        .back-link {
            display: inline-block;
            margin-top: 2rem;
            padding: 0.6rem 1.2rem;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 2rem;
            transition: background 0.2s;
        }

        .back-link:hover {
            background: #2980b9;
        }

        footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #7f8c8d;
        }

        @media (max-width: 700px) {
            body { padding: 1rem; }
            .container { padding: 1rem; }
            h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👥 Об авторах</h1>
        <div class="team-grid">
            <div class="card">
                <div class="card-header">Максим Кукушкин</div>
                <div class="card-body">
                    <div class="role">🔹 BFS – обход в ширину</div>
                    <div>Реализовал алгоритм BFS, построение остовного дерева с использованием очереди (FIFO), вывод порядка обхода вершин.</div>
                    <div class="contribution">✨ Вклад: модуль `bfs.py`, интеграция с веб-интерфейсом, отладка производительности.</div>
                    <a href="#" class="github-link">GitHub: @s1nvaise</a>
                </div>
            </div>
            <div class="card">
                <div class="card-header">Полина Коробова</div>
                <div class="card-body">
                    <div class="role">🔹 DFS – обход в глубину</div>
                    <div>Разработала алгоритм DFS, построение остовного дерева через стек (LIFO), обработку графов с несколькими компонентами связности.</div>
                    <div class="contribution">✨ Вклад: модуль `dfs.py`, создание интерактивной визуализации, тестирование.</div>
                    <a href="https://github.com/Im-Polina1029" class="github-link" target="_blank">GitHub: @Im-Polina1029</a>
                </div>
            </div>
            <div class="card">
                <div class="card-header">Виктор Повеличенко</div>
                <div class="card-body">
                    <div class="role">🎨 Раскраска вершин</div>
                    <div>Реализовал жадный алгоритм раскраски и алгоритм обратного поиска для нахождения минимального числа цветов.</div>
                    <div class="contribution">✨ Вклад: модуль `coloring.py`, оптимизация выбора порядка вершин, вывод результатов.</div>
                    <a href="#" class="github-link">GitHub: @VPovelychenko</a>
                </div>
            </div>
        </div>

        <div style="background: #f8fafc; border-radius: 1rem; padding: 1.5rem; margin-top: 1rem;">
            <h3 style="margin-top: 0;">📌 О проекте GraphApp</h3>
            <p>Учебный проект по дисциплине «Элементы теории графов». Приложение позволяет решать три классические задачи: построение остовного дерева (BFS/DFS) и минимальная раскраска вершин.</p>
        </div>

        <a href="/" class="back-link">← На главную</a>
        <footer>GraphApp — 2026 | Учебный демо-проект</footer>
    </div>
</body>
</html>