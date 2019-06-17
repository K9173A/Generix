"""
A module for a game board.
"""
import copy

import pygame

from generix.core.settings import CELL_WIDTH_PX, CELL_HEIGHT_PX
from generix.core.cell.point import Point

class Board(pygame.Surface):
    """
    Board - a grid of cells.
    """
    def __init__(self, width_n, height_n):
        super(Board, self).__init__((width_n * CELL_WIDTH_PX, height_n * CELL_HEIGHT_PX))
        self._width = width_n
        self._height = height_n
        self._cells = []
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
        Gets next Cell object on the 2D board.
        :return: Cell object.
        """
        if self._curr_point.x == self._width:
            self._curr_point.x = 0
            raise StopIteration

        cell = self.get_cell(self._curr_point)

        # Without shallow copy, we will have prev_point reference
        # to the curr_point, so in practice - it will be the same object,
        # but we need them to exist separately. Shallow copy is enough for
        # this purpose, not need in the copy.deepcopy().
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
        Gets specific cell.
        :param point: Point object.
        :return: Cell object.
        """
        return self._cells[point.x][point.y]

    def set_cell(self, point, cell):
        """
        Replaces current cell with a new one.
        :param point: Point object.
        :param cell: Cell object.
        :return: None.
        """
        self._cells[point.x][point.y] = cell

    def append_cell(self, index, cell):
        """
        Appends cell to the end of board.
        :param index: index of appending place.
        :param cell: Cell object.
        :return:
        """
        if index == len(self._cells):
            self._cells.append([])
        self._cells[index].append(cell)
