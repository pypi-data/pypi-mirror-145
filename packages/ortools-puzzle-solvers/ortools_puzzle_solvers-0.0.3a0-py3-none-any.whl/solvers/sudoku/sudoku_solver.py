from typing import List
from ortools.sat.python import cp_model

class SudokuSolver:
    def to_solved_board(self, solver, solved_board, board_size):
        board = []
        for row in range(board_size):
            values = []
            board.append(values)
            for col in range(board_size):
                values.append(solver.Value(solved_board[row][col]))
        return board

    def status_to_message(self, status) -> str:
        if status == cp_model.INFEASIBLE:
            return "INFEASIBLE"
        elif status == cp_model.MODEL_INVALID:
            return "MODEL_INVALD"
        else:
            return "UNKNOWN"

    def solve(
        self,
        template: List[List[str]]
    ) -> List[List[int]]:
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()
        
        board_width = 9
        subboard_width = 3
        board = [[model.NewIntVar(1, 9, f"Cell({row},{col})") for col in range(board_width)] for row in range(board_width)]

        for row in range(board_width):
            for col in range(board_width):
                template_cell = template[row][col]
                if len(template_cell) > 0:
                    model.Add(board[row][col] == int(template_cell))

        for row in range(board_width):
            model.AddAllDifferent(board[row])

        for col in range(board_width):
            cells = []
            for row in range(board_width):
                cells.append(board[row][col])
            model.AddAllDifferent(cells)

        for subboard_row in range(subboard_width):
            for subboard_col in range(subboard_width):
                subboard = []
                for row in range(subboard_width):
                    for col in range(subboard_width):
                        subboard.append(board[row + subboard_row * subboard_width][col + subboard_col * subboard_width])
                model.AddAllDifferent(subboard)

        status = solver.Solve(model)
        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            return self.to_solved_board(solver, board, board_width)
        else:
            raise Exception(f"Sudoku could not be solved. Status = {self.status_to_message(status)}")
