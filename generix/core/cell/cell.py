"""
A module for cells classes.
"""
from generix.core.cell.direction import Direction, get_random_direction
from generix.core.action.id import Action
from generix.core.cell.factory import register_cell
from generix.core.cell.id import Cell
from generix.core.settings import CELL_WIDTH_PX, CELL_HEIGHT_PX, CELL_FONT


def center_text_in_cell(cell_width_px, cell_height_px, text_width_px, text_height_px):
    """
    Centers text in a cell.
    :param cell_width_px: cell width (pixels).
    :param cell_height_px: cell height (pixels).
    :param text_width_px: text width (pixels).
    :param text_height_px: text height (pixels).
    :return: upper left corner of centered area.
    """
    x = int((cell_width_px - text_width_px) / 2)
    y = int((cell_height_px - text_height_px) / 2)
    return x, y


def search(dictionary, option):
    for k, v in dictionary.items():
        if k == option:
            return v
        if isinstance(v, dict):
            return search(v, option)
    return None

@register_cell
class EmptyCell:
    """
    Empty cell is like dark matter - fills all space but does nothing.
    """
    __slots__ = ('_i', '_genome')

    __settings__ = {
        'id': Cell.EMPTY_CELL,
        'color': (70, 70, 70),
        'chance': 10,
        'allowed_actions': [ Action.STAY ],
        'genome_max_len': 1,
    }

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

    def settings(self, option):
        """
        Gets cell settings option.
        :param option: option name.
        :return: option value.
        """
        return search(self.__settings__, option)

    def render(self, board):
        """
        Draws cell square.
        :param board: board instance where cell will be drawn.
        :return: None.
        """
        render_cell(board, self.settings('color'))


class StandardCell(EmptyCell):
    """
    Standard cell.
    """
    __slots__ = '_direction'

    __settings__ = {
        'id': Cell.STANDARD_CELL,
        'color': (70, 70, 70),
        'chance': 5,
        'allowed_actions': [ Action.STAY, Action.MOVE ],
        'genome_max_len': 64,
    }

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

    def set_relative_direction(self, angle):
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

    def set_absolute_direction(self, direction):
        """
        Sets new direction.
        :param direction: new direction.
        :return: None.
        """
        self._direction = direction

    def render(self, board):
        """
        Draws cell square.
        :param board: board instance where cell will be drawn.
        :return: None.
        """
        render_cell(board, self.settings('color'))


@register_cell
class FoodCell(EmptyCell):
    """
    FoodCell represents food which can be eaten by a HunterCell.
    """
    __slots__ = ()

    __settings__ = {
        'id': Cell.FOOD_CELL,
        'color': (150, 0, 150),
        'amount': 30,
        # 'bonus': { 'on_kill': 20 },
        'allowed_actions': [ Action.STAY ],
        'genome_max_len': 1,
    }


@register_cell
class WallCell(EmptyCell):
    """
    WallCell is s cell which blocks other cells from stepping on this coordinate.
    """
    __slots__ = ()

    __settings__ = {
        'id': Cell.WALL_CELL,
        'color': (30, 30, 30), # Dark gray
        'chance': 1,
        'allowed_actions': [ Action.STAY ],
        'genome_max_len': 1,
    }

    def render(self, board):
        """
        Draws cell square.
        :param board: board instance where cell will be drawn.
        :return: None.
        """
        render_cell(board, self.settings('color'))


@register_cell
class HunterCell(StandardCell):
    """
    HunterCell eats food to keep hp above 0.
    """
    __slots__ = '_hp'

    __settings__ = {
        'id': Cell.HUNTER_CELL,
        'color': (0, 0, 150),
        'text_color': (255, 255, 255),
        'hp': {
            'at_start': 30,
            'step_cost': -1
        },
        'amount': 30,
        'population': {
            'min': 5
        },
        'allowed_actions': [
            Action.STAY,
            Action.EAT,
            Action.MOVE,
            Action.TURN
        ],
        'genome_max_len': 64,
    }

    def __init__(self, genome, hp):
        """
        Constructs HunterCell object.
        :param genome: Genome instance.
        :param hp: health points
        """
        super(HunterCell, self).__init__(genome)
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
        if self._hp > self.settings('at_start'):
            self._hp = self.settings('at_start')
        elif self._hp < 0:
            self._hp = 0

    def render(self, board):
        """
        Draws cell square.
        :param board: board instance where cell will be drawn.
        :return: None.
        """
        render_cell(board, self.settings('color'))
        text = CELL_FONT.render(str(self._hp), False, (255, 255, 255))
        render_cell_text(board, text)


def render_cell(board, color):
    """
    Renders cell square.
    :param board: Board instance.
    :param color: color code (RGB tuple).
    :return: None.
    """
    board.fill(
        color, (
            CELL_WIDTH_PX * board.prev_point.x,
            CELL_HEIGHT_PX * board.prev_point.y,
            CELL_WIDTH_PX,
            CELL_HEIGHT_PX
        )
    )

def render_cell_text(board, text):
    """
    Renders text on a cell square.
    :param board: Board instance.
    :param text: text.
    :return: None.
    """
    (x_pad, y_pad) = center_text_in_cell(
        CELL_WIDTH_PX, CELL_HEIGHT_PX, text.get_width(), text.get_height()
    )
    board.blit(text, (
        board.prev_point.x * CELL_WIDTH_PX + x_pad,
        board.prev_point.y * CELL_HEIGHT_PX + y_pad
    ))