from enum import unique
from solvers.zehnergitter.zehnergitter_solver import ZehnergitterSolver
from solvers.neighbourhood import get_eight_neighbourhood

def get_sums():
    return [29, 27, 23, 25, 16, 18, 23, 22, 24, 18]

def get_width():
    return 10

def get_height():
    return 5

def test_finds_all_solutions():
    solver = ZehnergitterSolver()
    sums = get_sums()
    solved = solver.solve(sums)
    assert len(solved) > 0

def test_numbers_are_between_0_and_9():
    solver = ZehnergitterSolver()
    sums = get_sums()
    solved = solver.solve(sums)[0]
    for row in range(get_height()):
        for col in range(get_width()):
            assert solved[row][col] >= 0 and solved[row][col] <= 9

def test_numbers_per_row_are_unique():
    solver = ZehnergitterSolver()
    sums = get_sums()
    solved = solver.solve(sums)[0]
    for row in range(get_height()):
        unique_numbers = len(set(solved[row]))
        assert unique_numbers == 10

def test_center_differs_from_its_eight_neighbourhood():
    solver = ZehnergitterSolver()
    sums = get_sums()
    solved = solver.solve(sums)[0]
    for row in range(get_height()):
        for col in range(get_width()):
            neighbourhoods = get_eight_neighbourhood(row, col, get_width(), get_height())
            for neighbourhood_index in neighbourhoods:
                neighbour = solved[neighbourhood_index[0]][neighbourhood_index[1]]
                assert solved[row][col] != neighbour

def test_center_differs_from_its_eight_neighbourhood():
    solver = ZehnergitterSolver()
    sums = get_sums()
    solved = solver.solve(sums)[0]
    for col in range(get_width()):
        total = 0        
        for row in range(get_height()):
            total += solved[row][col]
        assert sums[col] == total
    