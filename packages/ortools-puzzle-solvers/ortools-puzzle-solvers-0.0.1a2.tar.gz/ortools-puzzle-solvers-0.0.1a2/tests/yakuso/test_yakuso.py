from solvers.yakuso.yakuso_solver import YakusoSolver


def get_template():
    return [
        ["", "", "", "1", "", ""],
        ["", "", "", "", "3", ""],
        ["", "0", "", "4", "0", ""],
        ["", "", "", "", "", ""],
        ["5", "5", "", "", "", ""],
    ]


def get_sum_columns():
    return ["", "", "4", "12", "10", "9"]


def test_finds_all_solutions():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)
    assert len(solved) == 2


def test_preinitializes_board_correctly():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)[0]
    for i in range(rows):
        for j in range(cols):
            if len(template[i][j]) > 0:
                assert solved[i][j] == int(template[i][j])


def test_cols_sum_correctly():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)[0]
    for j in range(cols):
        total = 0
        for i in range(rows):
            total += solved[i][j]
        if len(sum_cols[j]) > 0:
            assert total == int(sum_cols[j])


def test_all_numbers_in_row_must_be_zero_or_same_number():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)[0]
    for i in range(rows):
        max_num = max(solved[i])
        for j in range(cols):
            assert solved[i][j] == max_num or solved[i][j] == 0


def test_number_of_non_zeros_per_row_is_equal_to_max_number():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)[0]
    for i in range(rows):
        max_num = max(solved[i])
        count = len([j for j in range(cols) if solved[i][j] == max_num])
        assert max_num == count


def test_each_row_has_different_number():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)[0]
    distinct_numbers = len(set([max(solved[i]) for i in range(rows)]))
    assert distinct_numbers == rows


def test_each_number_from_1_to_rowsnum_is_used():
    yakuso_solver = YakusoSolver()
    rows = 5
    cols = 6
    template = get_template()
    sum_cols = get_sum_columns()
    solved = yakuso_solver.solve(template, sum_cols, rows, cols)[0]
    distinct_numbers = [max(solved[i]) for i in range(rows)]
    all_numbers = [i + 1 for i in range(rows)]
    not_used_numbers = len([i for i in all_numbers if i not in distinct_numbers])
    assert not_used_numbers == 0
