"""

"""
import enum
import random


@enum.unique
class Direction(enum.Enum):
    UP = 0
    UP_RIGHT = 45
    RIGHT = 90
    DOWN_RIGHT = 135
    DOWN = 180
    DOWN_LEFT = 225
    LEFT = 270
    UP_LEFT = 315


def get_random_direction():
    """
    Gets random enum value of Direction class.
    :return: enum value of Direction.
    """
    return random.choice([direction for direction in Direction])