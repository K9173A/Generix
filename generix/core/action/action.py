"""
A module for a bot Actions.
"""
import abc
import copy

from generix.core.cell.id import Cell
from generix.core.action.processor import register_cmd
from generix.core.action.id import Action
from generix.core.action import command


class BaseAction(abc.ABC):
    """
    Action represents simple step of life activity of a cell.
    """
    @abc.abstractmethod
    def execute(self, **kwargs):
        """
        Executes action.
        :param kwargs: additional kwargs parameters.
        :return: None.
        """
        pass

    def settings(self, option):
        """
        Gets action settings option.
        :param option: option name.
        :return: option value.
        """
        return self.__settings__[option]


@register_cmd
class Turn(BaseAction):
    """
    Action to turn relatively to the current angle.
    """
    __settings__ = {
        'id': Action.TURN,
        'is_final': False
    }

    def execute(self, cell, angle):
        """
        Sums up with previous direction.
        :param cell - Cell object.
        :param angle - angle to set.
        :return: None.
        """
        command.turn_relative(cell, angle)


@register_cmd
class Stay(BaseAction):
    """
    Stay on the current position.
    """
    __settings__ = {
        'id': Action.STAY,
        'is_final': True
    }

    def execute(self, board, point, cell):
        """
        Tells cell to stay where it is.
        :param board: Board instance (new one).
        :param point: Point instance.
        :param cell: Cell instance.
        :return: None.
        """
        if command.is_cell_of_types(board, point, [Cell.EMPTY_CELL]) >= 0:
            command.move(board, point, cell)


@register_cmd
class Look(BaseAction):
    """
    Look for neighboring cell type.
    """
    __settings__ = {
        'id': Action.LOOK,
        'is_final': False
    }

    def execute(self, board, point, cell_types):
        """
        Makes cell look for neighboring cell type.
        :param board: Board instance (any: new or old).
        :param point: Point instance.
        :param cell_types: list of cell types to compare cell with.
        :return: type of cell if type is present in the list, otherwise - None.
        """
        index = command.is_cell_of_types(board, point, cell_types)
        if index >= 0:
            return cell_types[index]
        return None


@register_cmd
class Move(BaseAction):
    """
    Move in a specific direction.
    """
    __settings__ = {
        'id': Action.MOVE,
        'is_final': True
    }

    def execute(self, old_board, new_board, point, cell,
                curr_cell_types, next_cell_types):
        """
        Moves cell in a specific direction.
        :param old_board - Board instance (current frame).
        :param new_board - Board instance (new frame).
        :param point - Point instance.
        :param cell - Cell instance.
        :param curr_cell_types - current frame cell types check list.
        :param next_cell_types - next frame cell types check list.
        :return: None.
        """
        if command.reaches_bound(old_board, point, cell.direction):
            command.move(new_board, point, cell)
            return

        shifted_point = copy.copy(point)
        shifted_point.shift(cell.direction, 1)

        curr_frame_cell_is_empty = command.is_cell_of_types(
            old_board, shifted_point, curr_cell_types
        ) >= 0

        next_frame_cell_is_empty = command.is_cell_of_types(
            new_board, shifted_point, next_cell_types
        ) >= 0

        if curr_frame_cell_is_empty and next_frame_cell_is_empty:
            point = shifted_point
        command.move(new_board, point, cell)


@register_cmd
class Eat(BaseAction):
    """
    Eat something/somebody.
    """
    __settings__ = {
        'id': Action.EAT,
        'is_final': True
    }

    def execute(self, old_board, new_board, point, cell):
        """
        Eats food in set direction (if food is present).
        :param old_board - Board instance (current frame).
        :param new_board - Board instance (new frame).
        :param point - Point instance.
        :param cell - Cell instance.
        :return: None.
        """
        # It takes 5hp for bot to eat food
        cell.change_hp(-5)

        if command.reaches_bound(old_board, point, cell.direction):
            new_board.set_cell(point, cell)
            return

        shifted_point = copy.copy(point)
        shifted_point.shift(cell.direction, 1)

        # Next frame cell should be empty, because cells are being refreshed in order of their
        # indexing, so the lower index - the earlier it's being refreshed. Hence, early cells
        # can eat food before the current cell.
        next_frame_cell_is_empty = command.is_cell_of_types(
            new_board, shifted_point, [Cell.EMPTY_CELL, Cell.FOOD_CELL]
        )

        if next_frame_cell_is_empty:
            command.move(new_board, shifted_point, cell)

            curr_frame_cell_is_food = command.is_cell_of_types(
                old_board, point, [Cell.FOOD_CELL]
            )
            if curr_frame_cell_is_food:
                cell.change_hp(10)
        else:
            command.move(new_board, point, cell)
