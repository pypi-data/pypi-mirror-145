from typing import List
from ortools.sat.python import cp_model


class SolutionAggregator(cp_model.CpSolverSolutionCallback):
    def __init__(self, solved_board, black_cells, rows_inbetween, cols_inbetween):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.solved_board = solved_board
        self.black_cells = black_cells
        self.rows_inbetween = rows_inbetween
        self.cols_inbetween = cols_inbetween
        self.solutions = []

    def on_solution_callback(self):
        board = []
        n = len(self.solved_board)
        for i in range(n):
            r = []
            board.append(r)
            for j in range(n):
                # Mask out black fields.
                value = self.Value(self.solved_board[i][j])
                if value > n - 2:
                    value = None
                r.append(value)
        self.solutions.append(board)


class DoploSolver:
    def solve(
        self, sum_rows: List[int], sum_cols: List[int], length: int
    ) -> List[List[int]]:
        model = cp_model.CpModel()

        # The effective numbers on the board, integer values.
        board = []
        # The blacked out fields, boolean variables.
        black_cells = []
        # The values that are in between black fields and must adhere to a sum constraint.
        rows_inbetween = []
        cols_inbetween = []

        # We allow numbers on the board from 1-N (not 1-(N-2))
        # This way we can use the all different constraint and force
        # the black fields > N-2
        for row in range(length):
            rows = []
            for col in range(length):
                rows.append(model.NewIntVar(1, length, f"{row}{col}"))
            board.append(rows)

        # Black fields are between -1 und 1
        # 0 = not a black field
        # 1 or -1 = start or end of a black field
        # This way we can sum the fields, if the sum is NOT zero
        # we're between two black fields.
        for row in range(length):
            values = []
            for col in range(length):
                values.append(model.NewIntVar(-1, 1, f"black-{row}{col}"))
            black_cells.append(values)

        for row in range(length):
            values = []
            for col in range(length):
                values.append(model.NewBoolVar(f"inbetween-row-{row}{col}"))
            rows_inbetween.append(values)

        for row in range(length):
            values = []
            for col in range(length):
                values.append(model.NewBoolVar(f"inbetween-col-{row}{col}"))
            cols_inbetween.append(values)

        # Ensure all values in a row are different.
        for row in range(length):
            model.AddAllDifferent(board[row])

        # Ensure all values in a column are different.
        for col in range(length):
            all_rows = []
            for row in range(length):
                all_rows.append(board[row][col])
            model.AddAllDifferent(all_rows)

        # Ensure there are only two black fields per row
        # Having negative values for the black cells make this a bit tedious
        # that's why we shift the value by 2, take the modulo and add up the modulos
        # To also make sure we have a 1 and -1, we check if the total is 0.
        for row in range(length):
            total = 0
            abs_total = 0
            for col in range(length):
                mult = model.NewIntVar(0, length, f"mult-row-{row}-{col}")
                model.AddModuloEquality(mult, black_cells[row][col] + 2, 2)
                abs_total += mult
                total += black_cells[row][col]
            model.Add(abs_total == 2)
            model.Add(total == 0)

        # Same as above, but this time for columns.
        for col in range(length):
            abs_total = 0
            total = 0
            for row in range(length):
                mult = model.NewIntVar(0, length, f"mult-col-{row}-{col}")
                model.AddModuloEquality(mult, black_cells[row][col] + 2, 2)
                abs_total += mult
                total += black_cells[row][col]
            model.Add(abs_total == 2)
            model.Add(total == 0)

        # Set the cells to true that are in between black fields
        for row in range(length):
            history = []
            for col in range(length):
                if len(history) > 0 and col < (length - 1):
                    sum_bool = sum(history)
                    should_enforce = model.NewBoolVar(f"apply-{row}{col}")
                    # Only enforce the constraint if it's not a black cell.
                    model.Add(black_cells[row][col] == 0).OnlyEnforceIf(should_enforce)
                    model.Add(black_cells[row][col] != 0).OnlyEnforceIf(
                        should_enforce.Not()
                    )
                    is_inside = model.NewBoolVar("temp")
                    # Simplify the comparison.
                    # If we're in between two black fields, the summed history is not 0.
                    model.Add(sum_bool != 0).OnlyEnforceIf(is_inside)
                    model.Add(sum_bool == 0).OnlyEnforceIf(is_inside.Not())
                    model.Add(rows_inbetween[row][col] == is_inside).OnlyEnforceIf(
                        should_enforce
                    )
                    model.Add(rows_inbetween[row][col] == 0).OnlyEnforceIf(
                        should_enforce.Not()
                    )
                else:
                    model.Add(rows_inbetween[row][col] == 0)
                history.append(black_cells[row][col])

        # Same as above, but for columns
        for col in range(length):
            sum_bool = 0
            for row in range(length):
                if len(history) > 0 and row < (length - 1):
                    should_enforce = model.NewBoolVar(f"apply-{row}{col}")
                    model.Add(black_cells[row][col] == 0).OnlyEnforceIf(should_enforce)
                    model.Add(black_cells[row][col] != 0).OnlyEnforceIf(
                        should_enforce.Not()
                    )
                    is_inside = model.NewBoolVar("abc")
                    model.Add(sum_bool != 0).OnlyEnforceIf(is_inside)
                    model.Add(sum_bool == 0).OnlyEnforceIf(is_inside.Not())
                    model.Add(cols_inbetween[row][col] == is_inside).OnlyEnforceIf(
                        should_enforce
                    )
                    model.Add(cols_inbetween[row][col] == 0).OnlyEnforceIf(
                        should_enforce.Not()
                    )
                else:
                    model.Add(cols_inbetween[row][col] == 0)
                sum_bool += black_cells[row][col]

        # Force black cells > N-2
        for row in range(length):
            for col in range(length):
                should_enforce = model.NewBoolVar(f"apply-{row}{col}")
                model.Add(black_cells[row][col] == 0).OnlyEnforceIf(should_enforce)
                model.Add(black_cells[row][col] != 0).OnlyEnforceIf(
                    should_enforce.Not()
                )
                model.Add(board[row][col] <= (length - 2)).OnlyEnforceIf(should_enforce)
                model.Add(board[row][col] > (length - 2)).OnlyEnforceIf(
                    should_enforce.Not()
                )

        # Ensure row sum is correct
        for row in range(length):
            total = 0
            for col in range(length):
                multres = model.NewIntVar(
                    0, (length * (length + 1)) // 2, f"multres-rows-{row}-{col}"
                )
                model.AddMultiplicationEquality(
                    multres, [board[row][col], rows_inbetween[row][col]]
                )
                total += multres
            model.Add(sum_rows[row] == total)

        # Ensure column sum is correct
        for col in range(length):
            total = 0
            for row in range(length):
                multres = model.NewIntVar(
                    0, (length * (length + 1)) // 2, f"multres-rows-{row}-{col}"
                )
                model.AddMultiplicationEquality(
                    multres, [board[row][col], cols_inbetween[row][col]]
                )
                total += multres
            model.Add(sum_cols[col] == total)

        solver = cp_model.CpSolver()
        aggregator = SolutionAggregator(
            board, black_cells, rows_inbetween, cols_inbetween
        )
        solver.parameters.enumerate_all_solutions = False
        _ = solver.Solve(model, aggregator)
        return aggregator.solutions
