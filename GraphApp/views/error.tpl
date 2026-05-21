<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>GraphApp - Ошибка</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary: #667eea; /* Основной синий */
            --accent: #6a994e;  /* Зелёный для кнопки примера */
            --error: #d93025;   /* Красный для ошибок */
            --bg-light: #f0f4ff;
            --bg-card: #ffffff;
            --text-dark: #333;
            --border-radius: 16px;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f8f9fa;
            color: var(--text-dark);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            background: var(--bg-card);
            padding: 2.5rem;
            border-radius: var(--border-radius);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            width: 100%;
            max-width: 600px;
            text-align: center;
        }

        h1 {
            text-align: center;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }

        .subtitle {
            text-align: center;
            color: #6c757d;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        .error-box {
            background-color: #fff3f3; /* Лёгкий фон для блока ошибки */
            border-left: 4px solid var(--error);
            padding: 1.5rem;
            border-radius: var(--border-radius);
        }

        .error-box h2 {
            color: var(--error);
            margin-bottom: 1rem;
        }

        .error-box p {
             font-size: 1.1rem;
             color: #333;
             margin-bottom: 2rem;
             line-height: 1.4;
        }

        .btn-return {
            display: inline-block;
            padding: 0.8rem 1.8rem;
            background-color: var(--primary);
            color: white !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: background-color 0.2s;
        }

        .btn-return:hover {
             background-color: #5a67d8; /* Темнее при наведении */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GraphApp</h1>
        <div class="subtitle">
           Исследуйте графы с помощью BFS, DFS и раскраски вершин
        </div>

        <div class="error-box">
           <h2>⚠️ Ошибка при обработке данных</h2>
           <p>{{message}}</p>
           <a href="/" class="btn-return">
               Вернуться на главную
           </a>
       </div>
    </div>
</body>
</html>