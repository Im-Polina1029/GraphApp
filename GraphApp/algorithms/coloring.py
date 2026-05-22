"""Алгоритмы раскраски вершин графа.

Модуль реализует вариант 3:
- жадная раскраска используется как быстрая оценка сверху;
- алгоритм обратного поиска уточняет результат и подбирает минимальное
  количество цветов для заданного графа.

Вершины в коде нумеруются с 0, но для вывода пользователю используются
номера вершин с 1.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

Matrix = List[List[int]]


def validate_adjacency_matrix(matrix: Sequence[Sequence[int]], n: int) -> None:
    """Проверяет корректность матрицы смежности неориентированного графа."""
    if not isinstance(n, int) or not (1 <= n <= 20):
        raise ValueError("Количество вершин n должно быть в диапазоне от 1 до 20")

    if len(matrix) != n:
        raise ValueError(f"Количество строк матрицы ({len(matrix)}) не равно n={n}")

    for i in range(n):
        if len(matrix[i]) != n:
            raise ValueError(f"Строка {i + 1} должна содержать ровно {n} элементов")

        if matrix[i][i] != 0:
            raise ValueError(f"Элемент главной диагонали matrix[{i + 1}][{i + 1}] должен быть равен 0")

        for j in range(n):
            if matrix[i][j] not in (0, 1):
                raise ValueError("Матрица смежности должна содержать только 0 и 1")
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Матрица смежности неориентированного графа должна быть симметричной")


def get_degrees(matrix: Sequence[Sequence[int]], n: int) -> List[int]:
    """Возвращает степени всех вершин графа."""
    validate_adjacency_matrix(matrix, n)
    return [sum(matrix[i][j] for j in range(n)) for i in range(n)]


def get_vertex_order_by_degree(matrix: Sequence[Sequence[int]], n: int) -> List[int]:
    """Возвращает порядок обработки вершин по убыванию степени."""
    degrees = get_degrees(matrix, n)
    return sorted(range(n), key=lambda vertex: (-degrees[vertex], vertex))


def is_valid_coloring(matrix: Sequence[Sequence[int]], colors: Sequence[int]) -> bool:
    """Проверяет, что соседние вершины имеют разные цвета."""
    n = len(matrix)
    if len(colors) != n:
        return False

    for i in range(n):
        if colors[i] <= 0:
            return False
        for j in range(i + 1, n):
            if matrix[i][j] == 1 and colors[i] == colors[j]:
                return False
    return True


def greedy_coloring(matrix: Matrix, n: int) -> Dict[str, object]:
    """Выполняет жадную раскраску и затем уточняет результат обратным поиском.

    Функция оставлена с названием ``greedy_coloring`` для совместимости с
    существующим ``app.py``. В результате возвращаются и жадная оценка, и
    оптимальная раскраска, найденная обратным поиском.
    """
    validate_adjacency_matrix(matrix, n)

    degrees = get_degrees(matrix, n)
    order = get_vertex_order_by_degree(matrix, n)

    greedy_colors = [0] * n
    greedy_num_colors = 0

    for vertex in order:
        used = {
            greedy_colors[neighbor]
            for neighbor in range(n)
            if matrix[vertex][neighbor] == 1 and greedy_colors[neighbor] != 0
        }

        color = 1
        while color in used:
            color += 1

        greedy_colors[vertex] = color
        greedy_num_colors = max(greedy_num_colors, color)

    optimal = optimal_coloring(matrix, n, upper_bound=greedy_num_colors)

    return {
        "colors": optimal["colors"],
        "num_colors": optimal["num_colors"],
        "min_colors": optimal["num_colors"],
        "best_color": optimal["colors"],
        "greedy_colors": greedy_colors,
        "greedy_num_colors": greedy_num_colors,
        "order": [vertex + 1 for vertex in order],
        "degrees": {vertex + 1: degrees[vertex] for vertex in range(n)},
        "checks": optimal["checks"],
        "is_valid": is_valid_coloring(matrix, optimal["colors"]),
    }


def optimal_coloring(matrix: Matrix, n: int, upper_bound: Optional[int] = None) -> Dict[str, object]:
    """Находит минимальную раскраску графа методом обратного поиска."""
    validate_adjacency_matrix(matrix, n)

    degrees = get_degrees(matrix, n)
    order = get_vertex_order_by_degree(matrix, n)

    if upper_bound is None:
        upper_bound = n

    lower_bound = 1 if not _has_edges(matrix, n) else 2
    checks: List[Dict[str, object]] = []

    for color_count in range(lower_bound, upper_bound + 1):
        colors = [0] * n
        success, result_colors, steps = _try_color_with_k(matrix, n, order, color_count, colors)
        checks.append({
            "k": color_count,
            "success": success,
            "steps": steps,
        })

        if success and result_colors is not None:
            return {
                "colors": result_colors,
                "num_colors": color_count,
                "checks": checks,
            }

    # Теоретически эта ветка не должна выполняться, так как n цветов всегда
    # достаточно для раскраски графа из n вершин.
    fallback_colors = list(range(1, n + 1))
    return {
        "colors": fallback_colors,
        "num_colors": n,
        "checks": checks,
    }


def _has_edges(matrix: Sequence[Sequence[int]], n: int) -> bool:
    return any(matrix[i][j] == 1 for i in range(n) for j in range(i + 1, n))


def _try_color_with_k(
    matrix: Sequence[Sequence[int]],
    n: int,
    order: Sequence[int],
    color_count: int,
    colors: List[int],
) -> Tuple[bool, Optional[List[int]], int]:
    """Пытается раскрасить граф ``color_count`` цветами."""
    steps = 0

    def backtrack(position: int) -> bool:
        nonlocal steps
        steps += 1

        if position == n:
            return True

        vertex = order[position]
        neighbor_colors = {
            colors[neighbor]
            for neighbor in range(n)
            if matrix[vertex][neighbor] == 1 and colors[neighbor] != 0
        }

        for color in range(1, color_count + 1):
            if color not in neighbor_colors:
                colors[vertex] = color

                if backtrack(position + 1):
                    return True

                colors[vertex] = 0

        return False

    success = backtrack(0)
    return success, colors.copy() if success else None, steps
