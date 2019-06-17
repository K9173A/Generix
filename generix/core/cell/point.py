"""
A module for a 2D Point class implementation.
"""
import random

from generix.core.cell.direction import Direction


def generate_random_point(x_min, x_max, y_min, y_max):
    """
    Geberates a Point object with random coordinates,
    :param x_min: x lower bound.
    :param x_max: x upper bound.
    :param y_min: y lower bound.
    :param y_max: y upper_bound.
    :return: Point object.
    """
    return Point(
        random.randint(x_min, x_max),
        random.randint(y_min, y_max)
    )


class Point:
    """
    Point class with 2 coordinates.
    """
    def __init__(self, x, y):
        """
        Constructs point object.
        :param x: x coordinate.
        :param y: y coordinate.
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        Returns user-friendly string-representation of object.
        :return: string with point coordinates.
        """
        return f'Point({self.x};{self.y})'

    def shift(self, direction, n):
        """
        Shift coordinate(s) by n in a specific direction.
        :param direction: direction to move to.
        :param n: length of move.
        :return: None.
        """
        if direction == Direction.UP:
            self.y -= n
        elif direction == Direction.UP_RIGHT:
            self.x += n
            self.y -= n
        elif direction == Direction.RIGHT:
            self.x += n
        elif direction == Direction.DOWN_RIGHT:
            self.x += n
            self.y += n
        elif direction == Direction.DOWN:
            self.y += n
        elif direction == Direction.DOWN_LEFT:
            self.x -= n
            self.y += n
        elif direction == Direction.LEFT:
            self.x -= n
        elif direction == Direction.UP_LEFT:
            self.x -= n
            self.y -= n
        else:
            raise ValueError

