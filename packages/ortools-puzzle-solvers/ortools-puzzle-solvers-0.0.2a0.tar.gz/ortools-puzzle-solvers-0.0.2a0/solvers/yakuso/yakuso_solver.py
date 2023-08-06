from typing import List
from ortools.sat.python import cp_model
from itertools import product


class SolutionAggregator(cp_model.CpSolverSolutionCallback):
    def __init__(self, board_bools, board_numbers, rows, cols, sum_cols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.board_bools = board_bools
        self.board_numbers = board_numbers
        self.rows = rows
        self.cols = cols
        self.sum_cols = sum_cols
        self.solutions = []

    def on_solution_callback(self):
        board = []
        self.solutions.append(board)
        for i in range(self.rows):
            r = []
            board.append(r)
            for j in range(self.cols):
                r.append(
                    self.Value(
                        self.board_bools[i][j] * self.Value(self.board_numbers[i])
                    )
                )
        return board


class YakusoSolver:
    def __create_board_bools(self, model, rows, cols):
        return [
            [model.NewBoolVar(f"({_i},{_j})") for _j in range(cols)]
            for _i in range(rows)
        ]

    def __create_board_maxima(self, model, rows):
        return [model.NewIntVar(1, rows, f"row_({_i})") for _i in range(rows)]

    def __create_board_sums(self, model, rows, cols):
        max_sum = rows * (rows + 1) // 2
        return [model.NewIntVar(0, max_sum, f"sum_col=({j})") for j in range(cols)]

    def __add_sum_constraints(self, model, sums, sum_cols, cols):
        for j in range(cols):
            if len(sums[j]) > 0:
                model.Add(int(sums[j]) == sum_cols[j])

    def __initialize_board_values(
        self, model, template, rows, cols, board_bools, board_maxima
    ):
        for i in range(rows):
            for j in range(cols):
                if len(template[i][j]) > 0:
                    template_num = int(template[i][j])
                    model.Add(board_bools[i][j] * template_num == template_num)
                    if template_num > 0:
                        model.Add(board_maxima[i] == template_num)

    def __add_row_value_constraints(self, model, rows, cols, board_bools, board_maxima):
        for i in range(rows):
            total = 0
            for j in range(cols):
                total += board_bools[i][j]
            model.Add(total == board_maxima[i])

    def __add_different_maxima_constraint(self, model, board_maxima):
        model.AddAllDifferent(board_maxima)

    def __add_sum_per_column_constraint(
        self, model, sums, sum_cols, rows, board_bools, board_maxima
    ):
        for j in range(len(sums)):
            cur_sum = sum_cols[j]
            total = 0
            for i in range(rows):
                mult = model.NewIntVar(0, rows, f"temp-mult-{i}")
                model.AddMultiplicationEquality(
                    mult, [board_maxima[i], board_bools[i][j]]
                )
                total += mult
            model.Add(total == cur_sum)

    def solve(
        self, template: List[List[str]], sums: List[str], rows: int, cols: int
    ) -> List[List[int]]:
        model = cp_model.CpModel()
        board_bools = self.__create_board_bools(model, rows, cols)
        board_maxima = self.__create_board_maxima(model, rows)
        sum_cols = self.__create_board_sums(model, rows, cols)
        self.__add_sum_constraints(model, sums, sum_cols, cols)
        self.__initialize_board_values(
            model, template, rows, cols, board_bools, board_maxima
        )
        self.__add_row_value_constraints(model, rows, cols, board_bools, board_maxima)
        self.__add_different_maxima_constraint(model, board_maxima)
        self.__add_sum_per_column_constraint(
            model, sums, sum_cols, rows, board_bools, board_maxima
        )
        solver = cp_model.CpSolver()
        aggregator = SolutionAggregator(board_bools, board_maxima, rows, cols, sum_cols)
        solver.parameters.enumerate_all_solutions = True
        _ = solver.Solve(model, aggregator)
        return aggregator.solutions
