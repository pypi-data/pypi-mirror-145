from solvers.doplo.doplo_solver import DoploSolver


def get_sum_rows():
    return [3, 6, 1, 0, 3]


def get_sum_cols():
    return [5, 4, 0, 6, 0]


def get_board_length():
    return 5


def test_finds_all_solutions():
    solver = DoploSolver()
    solved = solver.solve(get_sum_rows(), get_sum_cols(), get_board_length())
    assert len(solved) >= 1
