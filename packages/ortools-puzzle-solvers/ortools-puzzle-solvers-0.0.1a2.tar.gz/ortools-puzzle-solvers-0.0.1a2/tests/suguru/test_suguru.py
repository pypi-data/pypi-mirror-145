from enum import unique
from solvers.suguru.suguru_solver import SuguruSolver


def get_template():
    return [
        [(0, ""), (0, ""), (0, ""), (2, "3"), (11, ""), (11, ""), (10, "2"), (10, "")],
        [(0, "4"), (1, ""), (1, ""), (2, ""), (11, ""), (11, ""), (10, ""), (10, "")],
        [(1, ""), (1, "2"), (2, ""), (2, ""), (11, ""), (9, ""), (9, ""), (10, "")],
        [(1, ""), (3, "1"), (3, "5"), (2, ""), (12, ""), (12, "1"), (9, "5"), (9, "")],
        [(4, ""), (4, "2"), (3, ""), (3, ""), (12, ""), (8, ""), (8, ""), (9, "")],
        [(5, ""), (4, ""), (4, ""), (3, ""), (12, "4"), (7, ""), (8, ""), (8, "4")],
        [(5, ""), (5, ""), (4, ""), (6, ""), (12, ""), (7, "3"), (7, ""), (8, "")],
        [(5, ""), (5, "5"), (6, ""), (6, ""), (6, ""), (6, "5"), (7, ""), (7, "")],
    ]


def test_finds_all_solutions():
    solver = SuguruSolver()
    length = 8
    template = get_template()
    solved = solver.solve(template, length)
    assert len(solved) == 1


def test_preinitializes_board_correctly():
    solver = SuguruSolver()
    length = 8
    template = get_template()
    solved = solver.solve(template, length)[0]
    for i in range(length):
        for j in range(length):
            if len(template[i][j][1]) > 0:
                assert solved[i][j] == int(template[i][j][1])


def test_range_inside_region_is_correct():
    solver = SuguruSolver()
    length = 8
    template = get_template()
    solved = solver.solve(template, length)[0]
    cells = [cell for row in template for cell in row]
    for i in range(length):
        for j in range(length):
            region_index, value = template[i][j]
            region_size = len([cell for cell in cells if cell[0] == region_index])
            allowed_range = [i + 1 for i in range(region_size)]
            assert solved[i][j] in allowed_range


def test_numbers_inside_region_are_unique():
    solver = SuguruSolver()
    length = 8
    template = get_template()
    solved = solver.solve(template, length)[0]
    cells = [cell for row in template for cell in row]
    num_regions = max([cell[0] for cell in cells]) + 1
    region_values = [[] for i in range(num_regions)]
    for row in range(length):
        for col in range(length):
            region_index, _ = template[row][col]
            region_values[region_index].append(solved[row][col])
    for region in region_values:
        unique_numbers = len(set(region))
        assert len(region) == unique_numbers
