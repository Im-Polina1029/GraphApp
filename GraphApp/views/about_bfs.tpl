% rebase('base')
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Теория BFS | Обход в ширину | GraphApp</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f4f8;
            color: #1e2a3e;
            padding: 2rem;
            line-height: 1.7;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 1.5rem;
            box-shadow: 0 20px 35px -12px rgba(0,0,0,0.1);
            padding: 2rem;
        }

        h1 {
            font-size: 2.2rem;
            border-bottom: 4px solid #3498db;
            display: inline-block;
            padding-bottom: 0.3rem;
            margin-bottom: 1rem;
        }

        .subtitle {
            color: #4a627a;
            margin-bottom: 2rem;
            font-style: italic;
        }

        h2 {
            font-size: 1.6rem;
            margin: 1.8rem 0 1rem 0;
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 0.8rem;
        }

        h3 {
            font-size: 1.3rem;
            margin: 1.2rem 0 0.6rem;
            color: #3498db;
        }

        p {
            margin-bottom: 1rem;
        }

        .definition {
            background: #eef2fa;
            padding: 1rem;
            border-radius: 0.8rem;
            border-left: 5px solid #3498db;
            margin: 1.5rem 0;
        }

        .note {
            background: #fef9e3;
            padding: 1rem;
            border-radius: 0.8rem;
            border-left: 5px solid #f1c40f;
            margin: 1.5rem 0;
        }

        code {
            background: #f0f0f0;
            padding: 0.2rem 0.4rem;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        pre {
            background: #1e2a3a;
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 0.8rem;
            overflow-x: auto;
            font-size: 0.9rem;
            margin: 1rem 0;
        }

        ul, ol {
            margin: 0.8rem 0 1rem 1.8rem;
        }

        li {
            margin: 0.5rem 0;
        }

        .table-wrap {
            overflow-x: auto;
            margin: 1rem 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: #f9fafc;
        }
        th, td {
            border: 1px solid #cbd5e0;
            padding: 0.5rem;
            text-align: center;
        }
        th {
            background: #e2e8f0;
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
            color: #5a6e7c;
            border-top: 1px solid #e2e8f0;
            padding-top: 1.5rem;
        }

        @media (max-width: 700px) {
            body { padding: 1rem; }
            .container { padding: 1.2rem; }
            h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>📘 Поиск в ширину (BFS)</h1>
    <div class="subtitle">Breadth‑First Search — алгоритм обхода графа «по слоям»</div>

    <div class="definition">
        <strong>📌 Определение из теории графов:</strong> <em>Обход графа</em> — это систематическое перечисление его вершин (и/или рёбер).  
        <strong>Поиск в ширину (BFS)</strong> использует в качестве вспомогательной структуры данных <strong>очередь (FIFO — First In, First Out)</strong>.  
        Вершины обрабатываются в порядке их удалённости от стартовой: сначала все соседи на расстоянии 1, затем на расстоянии 2 и т.д.
    </div>

    <h2>1. Базовые понятия (по документу УП02)</h2>
    <ul>
        <li><strong>Граф</strong> \( G(V,E) \) — совокупность непустого множества вершин \( V \) и множества рёбер \( E \) — двухэлементных подмножеств \( V \).</li>
        <li><strong>Неориентированный граф</strong> — рёбра не имеют направления.</li>
        <li><strong>Маршрут</strong> — последовательность вершин \( v_0, v_1, …, v_k \), где каждые две соседние соединены ребром.</li>
        <li><strong>Расстояние</strong> \( d(u,v) \) — длина кратчайшей цепи между вершинами.</li>
        <li><strong>Ярус</strong> \( D(v,n) \) — множество вершин, находящихся на расстоянии \( n \) от вершины \( v \). BFS естественным образом разбивает граф на ярусы.</li>
        <li><strong>Связный граф</strong> — для любых двух вершин существует маршрут.</li>
    </ul>

    <h2>2. Алгоритм BFS</h2>
    <p><strong>Вход:</strong> граф \( G(V,E) \), представленный списками смежности \( \Gamma \), и начальная вершина \( v \).<br>
    <strong>Выход:</strong> последовательность вершин в порядке обхода (и/или остовное дерево BFS).</p>

    <pre>
Алгоритм BFS (с очередью):
  для всех вершин x ∈ V:
      x[отметка] := 0       // все вершины не посещены
  v → очередь T
  отметить v как посещённую

  пока T не пуста:
      u ← извлечь из начала очереди
      выдать u (например, добавить в порядок обхода)
      для каждой смежной вершины w ∈ Γ(u):
          если w не отмечена:
              отметить w
              добавить w в конец очереди T
              (при построении остовного дерева: добавить ребро (u,w) в дерево)
    </pre>

    <div class="note">
        💡 <strong>Ключевое отличие BFS от DFS:</strong>  
        BFS использует <strong>очередь (FIFO)</strong> и исследует вершины «в ширину» — слой за слоем.  
        DFS использует <strong>стек (LIFO)</strong> и идёт «в глубину» до упора, затем возвращается.
    </div>

    <h2>3. Свойства и приложения BFS</h2>
    <ul>
        <li>Находит <strong>кратчайшие пути</strong> в невзвешенном графе (по числу рёбер).</li>
        <li>Строит <strong>BFS-дерево</strong> — остовное дерево, где путь от корня к любой вершине является кратчайшим.</li>
        <li>Определяет компоненты связности графа.</li>
        <li>Используется в волновых алгоритмах, поиске выхода из лабиринта, в социальных сетях (степень удаления).</li>
        <li><strong>В проекте GraphApp</strong> BFS реализован для построения остовного дерева по заданной матрице смежности.</li>
    </ul>

    <h2>4. Сложность и реализация</h2>
    <ul>
        <li><strong>Время работы:</strong> \( O(V + E) \) при использовании списков смежности.</li>
        <li><strong>Дополнительная память:</strong> \( O(V) \) для очереди и массива отметок.</li>
        <li>Граф может быть задан <strong>матрицей смежности</strong> (квадратная булева матрица \( A \), где \( A[i][j]=1 \), если вершины смежны) или <strong>списками смежности</strong> (рекомендуется для разреженных графов).</li>
    </ul>
     что не так поеое БЮ поет 
    <h2>5. Пример работы BFS</h2>
    <p>Рассмотрим граф:</p>
    <pre>
Вершины: 1 — 2 — 4
|      |
3      5
    </pre>
    <p>Старт с вершины <strong>1</strong>:</p>
    <ul>
        <li>Ярус 0: {1}</li>
        <li>Ярус 1: {2, 3}</li>
        <li>Ярус 2: {4, 5}</li>
    </ul>
    <p><strong>Порядок обхода BFS:</strong> 1 → 2 → 3 → 4 → 5<br>
    <strong>Рёбра BFS-дерева:</strong> (1,2), (1,3), (2,4), (2,5)</p>

    <div class="definition">
        📖 <strong>Из документа (п. 1.3 Достижимость):</strong>  
        Вершина \( x_j \) <em>достижима</em> из \( x_i \), если существует путь. Множество достижимых вершин для \( x_i \) — это все вершины, до которых BFS найдёт путь.  
        BFS строит <strong>достижимое множество</strong> ярусно.
    </div>

    <h2>6. Способы представления графа (памятка)</h2>
    <div class="table-wrap">
        <table>
            <tr><th>Представление</th><th>Объём памяти</th><th>Примечание</th></tr>
            <tr><td>Матрица смежности</td><td>\( O(p^2) \)</td><td>быстрый доступ, но много памяти для разреженных графов</td></tr>
            <tr><td>Списки смежности</td><td>\( O(p + 2q) \) (неориент.)</td><td>экономично, используется в BFS/DFS</td></tr>
            <tr><td>Матрица инциденций</td><td>\( O(pq) \)</td><td>редко применяется для обходов</td></tr>
            <tr><td>Массив рёбер</td><td>\( O(q) \)</td><td>удобно для алгоритмов на рёбрах</td></tr>
        </table>
    </div>

    <h2>7. Использование в вашем проекте GraphApp</h2>
    <p>Приложение реализует:</p>
    <ul>
        <li>Ввод <strong>количества вершин</strong> и <strong>матрицы смежности</strong> (или генерация случайного графа).</li>
        <li>Выбор начальной вершины обхода.</li>
        <li>Построение <strong>остовного дерева BFS</strong> и вывод матрицы смежности дерева.</li>
        <li>Отображение порядка обхода вершин.</li>
    </ul>
    <p>Программная реализация (Python + Bottle) строго следует псевдокоду из п. 1.5 документа.</p>

    <div class="note">
        📚 <strong>Источник теории:</strong> Данная страница составлена на основе методического материала <em>«Элементы теории графов»</em> из задания на учебную практику УП02 (специальность 09.02.07 «Информационные системы и программирование»).
    </div>

    <a href="/" class="back-link">← Вернуться в приложение</a>
    <footer>GraphApp — учебный проект по теории графов, 2026 | BFS реализован Михаилом Кукушкиным</footer>
</div>
</body>
</html>