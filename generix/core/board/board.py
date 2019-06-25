"""
A module for a game board.
"""
import copy

import pygame

from generix.core.cell.point import Point
from generix.core.settings.registry import settings_reg


class Board(pygame.Surface):
    """
    Board forms grid of cells  (cell managers).
    """
    def __init__(self, width_n, height_n):
        """
        Constructs Board instance.
        :param width_n: width of the board (amount of rows).
        :param height_n: height of the board (amount of columns).
        """
        cell_data = settings_reg.find('cell')
        super(Board, self).__init__((width_n * cell_data['width'], height_n * cell_data['height']))
        self._width = width_n
        self._height = height_n
        self._grid = []
        self._prev_point = Point(0, 0)
        self._curr_point = Point(0, 0)

    def __iter__(self):
        """
        Returns iterator (self).
        :return: iterator object.
        """
        return self

    def __next__(self):
        """
        Gets next CellManager object on the 2D board.
        :return: CellManager object.
        """
        if self._curr_point.x == self._width:
            self._curr_point.x = 0
            raise StopIteration

        cell = self.get_cell(self._curr_point)

        # Without shallow copy we will have prev_point reference
        # to the curr_point, so in practice - it will be the same object,
        # but we need them to exist separately. Shallow copy is enough for
        # this purpose, no need in copy.deepcopy().
        self._prev_point = copy.copy(self._curr_point)

        if self._curr_point.y < self._height - 1:
            self._curr_point.y += 1
        else:
            self._curr_point.x += 1
            self._curr_point.y = 0

        return cell

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def curr_point(self):
        return self._curr_point

    @property
    def prev_point(self):
        return self._prev_point

    def get_cell(self, point):
        """
        Gets specific cell manager.
        :param point: Point object.
        :return: CellManager object.
        """
        return self._grid[point.x][point.y]

    def set_cell(self, point, cell):
        """
        Replaces current cell manager with a new one.
        :param point: Point object.
        :param cell: Cell object.
        :return: None.
        """
        self._grid[point.x][point.y] = cell

    def append_cell(self, index, cell):
        """
        Appends cell manager to the end of board.
        :param index: index of appending place.
        :param cell: Cell object.
        :return: None.
        """
        if index == len(self._grid):
            self._grid.append([])
        self._grid[index].append(cell)
