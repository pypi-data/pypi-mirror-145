def get_eight_neighbourhood(row, column, width, height):
    is_valid_neighbour = (
        lambda row, col: row >= 0 and row < height and col >= 0 and col < width
    )
    neighbours = [
        (row - 1, column - 1),
        (row - 1, column),
        (row - 1, column + 1),
        (row, column - 1),
        (row, column + 1),
        (row + 1, column - 1),
        (row + 1, column),
        (row + 1, column + 1),
    ]
    return [n for n in neighbours if is_valid_neighbour(n[0], n[1])]