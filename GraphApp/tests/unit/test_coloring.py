import pytest

from algorithms.coloring import (
    greedy_coloring,
    is_valid_coloring,
    validate_adjacency_matrix,
)


def assert_coloring(matrix, expected_colors):
    result = greedy_coloring(matrix, len(matrix))
    assert result["num_colors"] == expected_colors
    assert result["min_colors"] == expected_colors
    assert is_valid_coloring(matrix, result["colors"])
    return result


def test_01_empty_graph_uses_one_color():
    matrix = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    result = assert_coloring(matrix, 1)
    assert result["colors"] == [1, 1, 1, 1]


def test_02_path_graph_uses_two_colors():
    matrix = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
    ]
    assert_coloring(matrix, 2)


def test_03_triangle_graph_uses_three_colors():
    matrix = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
    assert_coloring(matrix, 3)


def test_04_square_cycle_uses_two_colors():
    matrix = [
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ]
    assert_coloring(matrix, 2)


def test_05_odd_cycle_uses_three_colors():
    matrix = [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0],
    ]
    assert_coloring(matrix, 3)


def test_06_star_graph_uses_two_colors():
    matrix = [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ]
    result = assert_coloring(matrix, 2)
    assert result["colors"][0] != result["colors"][1]
    assert result["colors"][1:] == [result["colors"][1]] * 4


def test_07_complete_graph_k4_uses_four_colors():
    matrix = [
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
    ]
    assert_coloring(matrix, 4)


def test_08_disconnected_triangle_and_edge_uses_three_colors():
    matrix = [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
    ]
    assert_coloring(matrix, 3)


def test_09_matrix_with_loop_is_rejected():
    matrix = [
        [1, 1],
        [1, 0],
    ]
    with pytest.raises(ValueError, match="главной диагонали"):
        validate_adjacency_matrix(matrix, 2)


def test_10_asymmetric_matrix_is_rejected():
    matrix = [
        [0, 1, 0],
        [0, 0, 1],
        [0, 1, 0],
    ]
    with pytest.raises(ValueError, match="симметричной"):
        validate_adjacency_matrix(matrix, 3)
