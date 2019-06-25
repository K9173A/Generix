"""
A module for different commands which composes into Action.
"""
from generix.core.cell.direction import Direction


def reaches_bound(board, point, direction):
    """
    Checks whether a cell reached bounds or not.
    :param direction: direction to check.
    :param board: board instance.
    :param point: Point object.
    :return: True - reached, False - not reached.
    """
    if direction == Direction.UP:
        return is_upper_bound(point.y)
    elif direction == Direction.UP_RIGHT:
        return is_upper_bound(point.y) or is_right_bound(point.x, board)
    elif direction == Direction.RIGHT:
        return is_right_bound(point.x, board)
    elif direction == Direction.DOWN_RIGHT:
        return is_lower_bound(point.y, board) or is_right_bound(point.x, board)
    elif direction == Direction.DOWN:
        return is_lower_bound(point.y, board)
    elif direction == Direction.DOWN_LEFT:
        return is_lower_bound(point.y, board) or is_left_bound(point.x)
    elif direction == Direction.LEFT:
        return is_left_bound(point.x)
    elif direction == Direction.UP_LEFT:
        return is_upper_bound(point.y) or is_left_bound(point.x)

def is_left_bound(x):
    """
    Was left bound reached?
    :param x: x coordinate.
    :return: True - bound was reached, False - otherwise.
    """
    return x <= 0

def is_upper_bound(y):
    """
    Was right bound reached?
    :param y: y coordinate.
    :return: True - bound was reached, False - otherwise.
    """
    return y <= 0

def is_lower_bound(y, board):
    """
    Was lower bound reached?
    :param y: y coordinate.
    :param board: Board instance.
    :return: True - bound was reached, False - otherwise.
    """
    return y >= board.height - 1

def is_right_bound(x, board):
    """
    Was right bound reached?
    :param x: x coordinate.
    :param board: Board instance.
    :return: True - bound was reached, False - otherwise.
    """
    return x >= board.width - 1

def move(board, point, cell):
    """
    Sets cell on point position.
    :param board: Board instance.
    :param point: Point instance of cell location.
    :param cell: CellId instance.
    :return: None.
    """
    board.set_cell(point, cell)

def turn(cell, angle):
    """
    Turns cell to specific angle.
    :param cell: Cell object.
    :param angle: angle to turn to from current position.
    :return: None.
    """
    cell.turn(angle)

def is_cell_of_types(board, point, types):
    """
    Searches cell type in the list and returns an index if found.
    :param board: Board instance.
    :param point: Point instance.
    :param types: list of cell types (enum).
    :return: index if found, otherwise it returns -1.
    """
    try:
        index = types.index(board.get_cell(point).id)
    except ValueError:
        return -1
    return index
