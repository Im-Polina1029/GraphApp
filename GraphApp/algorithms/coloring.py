# algorithms/coloring.py
# Модуль раскраски вершин графа (жадный алгоритм)
# В разработке


def greedy_coloring(matrix, n):
    """
    Жадный алгоритм раскраски вершин графа.
    
    Входные параметры:
        matrix: матрица смежности (list of lists)
        n: количество вершин
    
    Возвращает словарь с ключами:
        colors: список цветов для каждой вершины (индексация с 0)
        num_colors: количество использованных цветов
    """
    # Проверка корректности входных данных
    if not (0 < n < 21):
        raise ValueError("n должен быть в диапазоне (0;21)")
    
    # Проверка симметричности матрицы и нулей на диагонали
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError(f"matrix[{i+1}][{i+1}] должен быть равен 0")
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Матрица смежности должна быть симметричной")
    
    # TODO: Реализовать полноценный жадный алгоритм раскраски
    # Пока заглушка: все вершины красим в первый цвет
    
    colors = [1] * n  # все вершины цветом 1
    num_colors = 1
    
    return {
        'colors': colors,
        'num_colors': num_colors
    }


# Альтернативная заглушка для тестирования (разные цвета)
def greedy_coloring_demo(matrix, n):
    """
    Демонстрационная версия: каждая вершина получает свой номер цвета.
    """
    colors = list(range(1, n + 1))
    num_colors = n
    
    return {
        'colors': colors,
        'num_colors': num_colors
    }
