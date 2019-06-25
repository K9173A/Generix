"""
A module for cells classes.
"""
import pygame

from generix.core.cell.direction import Direction, get_random_direction
from generix.core.cell.id import CellId


class EmptyCell:
    """
    Empty cell is like dark matter - fills all space but does nothing.
    """
    __slots__ = ('_i', '_genome')

    id = CellId.EMPTY_CELL

    def __init__(self, genome):
        """
        Constructs StandardCell object.
        :param genome: Genome instance.
        """
        self._i = -1
        self._genome = genome

    def current_action(self):
        """
        Gets current action to execute.
        :return: action name.
        """
        return self._genome.get_cmd(self._i)

    def next_action(self):
        """
        Gets next action to execute.
        :return: action name.
        """
        self._i = self._i + 1 if self._i < len(self._genome) - 1 else 0
        return self.current_action()


class StandardCell(EmptyCell):
    """
    Standard cell.
    """
    __slots__ = '_direction'

    id = CellId.STANDARD_CELL

    def __init__(self, genome):
        """
        Constructs StandardCell object.
        :param genome: Genome instance.
        """
        super(StandardCell, self).__init__(genome)
        self._direction = get_random_direction()

    @property
    def direction(self):
        return self._direction

    def turn(self, angle):
        """
        Makes cell change direction on a set angle.
        :param angle: relative angle.
        :return: None.
        """
        if angle % 45 != 0:
            raise ValueError('Angle should be a multiple of 45!')
        if 360 < angle or angle < -360:
            raise ValueError('Angle should be in range of [-360;360]!')
        result = self._direction.value + angle
        if abs(result / 360) >= 1:
            if result < 0:
                result += 360
            else:
                result -= 360
        self._direction = Direction(result)


class FoodCell(EmptyCell):
    """
    FoodCell represents food which can be eaten by a HunterCell.
    """
    __slots__ = ()

    id = CellId.FOOD_CELL


class WallCell(EmptyCell):
    """
    WallCell is s cell which blocks other cells from stepping on this coordinate.
    """
    __slots__ = ()

    id = CellId.WALL_CELL


class HunterCell(StandardCell):
    """
    HunterCell eats food to keep hp above 0.
    """
    __slots__ = ('_hp', '_max_hp')

    id = CellId.HUNTER_CELL

    def __init__(self, genome, hp):
        """
        Constructs HunterCell object.
        :param genome: Genome instance.
        :param hp: health points
        """
        super(HunterCell, self).__init__(genome)
        self._max_hp = hp
        self._hp = hp

    @property
    def hp(self):
        return self._hp

    def change_hp(self, value):
        """
        Changes health by <value> point(s).
        :param value: delta of change, can be negative.
        :return: None.
        """
        self._hp += value
        if self._hp > self._max_hp:
            self._hp = self._max_hp
        elif self._hp < 0:
            self._hp = 0
