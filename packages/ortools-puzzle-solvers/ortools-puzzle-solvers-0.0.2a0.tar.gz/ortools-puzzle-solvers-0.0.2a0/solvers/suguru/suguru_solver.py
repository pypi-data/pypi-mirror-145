from typing import List, Tuple
from ortools.sat.python import cp_model


class SolutionAggregator(cp_model.CpSolverSolutionCallback):
    def __init__(self, solved_board):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.solved_board = solved_board
        self.solutions = []

    def on_solution_callback(self):
        board = []
        self.solutions.append(board)
        for row in range(len(self.solved_board)):
            values = []
            board.append(values)
            for col in range(len(self.solved_board)):
                values.append(self.Value(self.solved_board[row][col]))
        return board


class SuguruSolver:
    def __get_8er_neighbours(self, i, j, length):
        is_valid_neighbour = (
            lambda row, col: row >= 0 and row < length and col >= 0 and col < length
        )
        neighbours = [
            (i - 1, j - 1),
            (i - 1, j),
            (i - 1, j + 1),
            (i, j - 1),
            (i, j + 1),
            (i + 1, j - 1),
            (i + 1, j),
            (i + 1, j + 1),
        ]
        return [n for n in neighbours if is_valid_neighbour(n[0], n[1])]

    def solve(
        self, template: List[List[Tuple[int, str]]], length: int
    ) -> List[List[int]]:
        model = cp_model.CpModel()
        # We'll use the entire board for neighbour value checking
        board = [[0 for _j in range(length)] for _i in range(length)]

        # We'll use the region variables to ensure that all numbers inside a region are different
        # from eachother and in a certain range (1-size of region)
        cells = [cell for row in template for cell in row]
        num_regions = max([cell[0] for cell in cells]) + 1
        region_variables = [[] for i in range(num_regions)]

        for row in range(len(template)):
            for col in range(len(template[row])):
                region_index, value = template[row][col]
                # Define the max number inside a region to 1 - region size.
                region_size = len([i for i in cells if i[0] == region_index])
                variable = model.NewIntVar(1, region_size, f"({row},{col})")

                # Store the variable so that "global board constraints" can be checked
                # such as neighbours
                board[row][col] = variable

                # Preinitialize the board.
                if len(value) > 0:
                    model.Add(variable == int(value))
                region_variables[region_index].append(variable)

        # Ensure all numbers inside a region are different.
        for region in region_variables:
            model.AddAllDifferent(region)

        # Ensure the number x, centered in a certain 8-neighbourhood,
        # does not appear in any of its neighbours.
        for row in range(length):
            for col in range(length):
                cell_variable = board[row][col]
                neighbour_indices = self.__get_8er_neighbours(row, col, length)
                for neighbour_index in neighbour_indices:
                    neighbour_variable = board[neighbour_index[0]][neighbour_index[1]]
                    model.Add(cell_variable != neighbour_variable)

        solver = cp_model.CpSolver()
        aggregator = SolutionAggregator(board)
        solver.parameters.enumerate_all_solutions = True
        _ = solver.Solve(model, aggregator)
        return aggregator.solutions
