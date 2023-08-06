from solvers.sudoku.sudoku_solver import SudokuSolver

def get_template():
    return [
        ["",   "",  "",  "",  "",  "", "5", "9",  ""],
        ["2", "4",  "", "7",  "", "8",  "", "3",  ""],
        ["8",  "", "9",  "", "5",  "", "4",  "",  ""],
        ["",  "8",  "", "9",  "", "4",  "", "7",  ""],
        ["",   "", "1",  "",  "",  "", "3",  "",  ""],
        ["",  "9",  "", "6",  "", "5",  "", "4",  ""],
        ["",   "", "8",  "", "6",  "", "9",  "", "3"],
        ["",  "2",  "", "1",  "", "9",  "", "5", "6"],
        ["",  "1", "6",  "",  "",  "",  "",  "",  ""]
    ]

def test_finds_all_solutions():
    solver = SudokuSolver()
    template = get_template()
    solved = solver.solve(template)
    assert len(solved) > 0

def test_preinitializes_board_correctly():
    yakuso_solver = SudokuSolver()
    template = get_template()
    solved = yakuso_solver.solve(template)
    for row in range(9):
        for col in range(9):
            if len(template[row][col]) > 0:
                assert solved[row][col] == int(template[row][col])