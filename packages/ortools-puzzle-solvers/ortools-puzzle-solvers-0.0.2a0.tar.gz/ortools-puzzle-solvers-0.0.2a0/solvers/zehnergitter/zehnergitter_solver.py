from typing import List, Tuple
from ortools.sat.python import cp_model
from solvers.neighbourhood import get_eight_neighbourhood

class SolutionAggregator(cp_model.CpSolverSolutionCallback):
    def __init__(self, solved_board, width, height):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.solved_board = solved_board
        self.width = width
        self.height = height
        self.solutions = []

    def on_solution_callback(self):
        board = []
        self.solutions.append(board)
        for row in range(self.height):
            values = []
            board.append(values)
            for col in range(self.width):
                values.append(self.Value(self.solved_board[row][col]))

class ZehnergitterSolver:
    def solve(
        self, sums: List[int]
    ) -> List[List[int]]:
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()
        width = 10
        height = 5

        # Allowed numbers are 0-9
        board = [[model.NewIntVar(0, 9, f"Cell({row},{col})") for col in range(width)] for row in range(height)]

        # All numbers in a row must be different to eachother.
        for row in range(height):
            model.AddAllDifferent(board[row])

        # Orthogonal and diagonal neighbours must be different from center.
        for row in range(height):
            for col in range(width):
                center = board[row][col]
                neighbours = get_eight_neighbourhood(row, col, width, height)
                for neighbour in neighbours:
                    neighbour_cell = board[neighbour[0]][neighbour[1]]
                    model.Add(center != neighbour_cell)

        # A column must sum up to the values in the predefined list of sums.
        for col in range(width):
            total = 0
            for row in range(height):
                total += board[row][col]
            model.Add(sums[col] == total)

        aggregator = SolutionAggregator(board, width, height)
        solver.parameters.enumerate_all_solutions = False
        _ = solver.Solve(model, aggregator)
        return aggregator.solutions
