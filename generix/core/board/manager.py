"""
A module for a BoardHandler which manages Board instance.
"""
import json

import pygame

from generix.core.cell.factory import factory
from generix.core.cell.id import CellId
from generix.core.cell.point import Point, generate_random_point
from generix.core.board.board import Board
from generix.core.action.executor import execute, Action
from generix.core.settings.registry import settings_reg
from generix.core.settings.encoder import SettingsEncoder
from generix.core.data.statistics import IterationStatistics


class BoardManager:
    """
    Handles boards state and manages statistics.
    """
    def __init__(self):
        """
        Constructs BoardManager instance.
        """
        self._board_data = settings_reg.find('board')
        self._prev_board = None
        self._curr_board = None
        self._statistics = IterationStatistics()
        self._clock = pygame.time.Clock()

    @property
    def statistics(self):
        return self._statistics

    def renew_statistics(self):
        self._statistics = IterationStatistics()

    def save(self, path):
        """
        Saves board cells positions to the file: (x,y): cell_id
        :param path: path to the file where data is being stored.
        :return: None.
        """
        data = {}

        for cell in self._curr_board:
            x = self._curr_board.prev_point.x
            y = self._curr_board.prev_point.y
            data[f'{x},{y}'] = cell.id.value

        with open(path, mode='w', encoding='utf-8') as f:
            json.dump(data, f, cls=SettingsEncoder)

    def load(self, path):
        """
        Loads board cells positions from the file.
        :param path: path to the file where data is being stored.
        :return: None.
        """
        with open(path, mode='r', encoding='utf-8') as f:
            data = json.load(f)

        for location, cell_id_value in data.items():
            cell_id = CellId(cell_id_value)
            if settings_reg.find_option_by_key(cell_id, 'save_location'):
                (x, y) = location.split(',')
                self._curr_board.set_cell(Point(int(x), int(y)), factory.create_cell(cell_id))

    def create_new_board(self):
        """
        Creates new Board instance and initializes it.
        :return: None.
        """
        self._curr_board = Board(self._board_data['rows'], self._board_data['cols'])
        self.init_board(self._curr_board)
        self.fill_board(self._curr_board)

    def update(self, fps, refresh_rate):
        """
        Updates board state.
        :param fps: frames per second.
        :param refresh_rate: refresh rate.
        :return: updated board.
        """
        limit = pygame.time.get_ticks()
        self._clock.tick(fps)
        if pygame.time.get_ticks() - limit > refresh_rate:
            self.switch_board()
            self.init_board(self._curr_board, CellId.EMPTY_CELL)

            # Updates state of cells on the previous frame
            for cell in self._prev_board:
                self._statistics.update(cell.id)
                self.update_cell(cell)

            # Updates visual state on the current frame
            for cell in self._curr_board:
                self.render_cell(self._curr_board, cell)

            return self._curr_board
        return None

    def init_board(self, board, cell_name=None):
        """
        Initializes board instance with cells.
        :param board: board to be initialized.
        :param cell_name: cell enum value. None means random.
        :return: None.
        """
        for x in range(board.width):
            for _ in range(board.height):
                if cell_name:
                    cell = factory.create_cell(cell_name)
                else:
                    cell = factory.create_random_cell()
                board.append_cell(x, cell)

    def fill_board(self, board):
        """
        Initializes board instance with cells which have 'amount' attribute in
        the settings.
        :param board: board to be filled.
        :return: None.
        """
        for cell_id, cell_data in settings_reg.find('cell').items():
            if not isinstance(cell_data, dict):
                continue
            amount = settings_reg.search(cell_data, 'amount')
            if amount is None:
                continue
            while amount > 0:
                point = generate_random_point(0, board.width - 1, 0, board.height - 1)
                curr_cell_id = self._curr_board.get_cell(point).id
                # Check whether the cell is empty or not, to replace it.
                if curr_cell_id == CellId.EMPTY_CELL:
                    board.set_cell(point, factory.create_cell(cell_id))
                    amount -= 1

    def switch_board(self):
        """
        Creates new board.
        :return: None.
        """
        self._prev_board = self._curr_board
        self._curr_board = Board(self._curr_board.width, self._curr_board.height)

    def update_cell(self, cell):
        """
        Updates cell state.
        :param cell: CellId object.
        :return: None.
        """
        while True:
            step_cost = settings_reg.find_option_by_key(cell.id, 'step_cost')
            if step_cost:
                cell.change_hp(step_cost)
                if cell.hp <= 0:
                    break

            # CellId is being used in every action, so passed explicitly
            action = cell.next_action()
            execute(action, cell=cell, **self.prepare_action_context(action))

            # If action is final - breaks execution. The control then moves to the next bot.
            if settings_reg.find_option_by_key(action, 'is_final'):
                break

    def render_cell(self, board, cell):
        cell_data = settings_reg.find('cell')

        width = cell_data['width']
        height = cell_data['height']

        render(board, settings_reg.find_option_by_key(cell.id, 'color'), width, height)

        if cell.id == CellId.HUNTER_CELL:
            text_settings = cell_data['text']

            font_size = width * text_settings['size_multiplier']
            rendered_text = render_text(
                str(cell.hp), text_settings['color'], text_settings['font'], int(font_size)
            )

            (x_pad, y_pad) = center_text_in_cell(
                width, height,
                rendered_text.get_width(),
                rendered_text.get_height()
            )

            x = board.prev_point.x * width + x_pad
            y = board.prev_point.y * height + y_pad

            blit_text(board, rendered_text, (x, y))


    def prepare_action_context(self, action):
        if action == Action.EAT:
            return {
                'old_board': self._prev_board,
                'new_board': self._curr_board,
                'point': self._prev_board.prev_point,
            }

        elif action == Action.MOVE:
            return {
                'old_board': self._prev_board,
                'new_board': self._curr_board,
                'point': self._prev_board.prev_point,
                'curr_cell_types': [CellId.EMPTY_CELL],
                'next_cell_types': [CellId.EMPTY_CELL],
            }

        elif action == Action.STAY:
            return {
                'board': self._curr_board,
                'point': self._prev_board.prev_point,
            }

        elif action == Action.TURN:
            return { 'angle': 45 }

        else:
            raise ValueError('undefined action value:', action)


def render(board, color, cell_width, cell_height):
    """
    Renders cell square.
    :param board: Board instance.
    :param color: color code (RGB tuple).
    :return: None.
    """
    board.fill(color, (
        cell_width * board.prev_point.x,
        cell_height * board.prev_point.y,
        cell_width, cell_height
    ))


def render_text(text, text_color=(255, 255, 255), font_name='Sans Serif', font_size=6):
    """
    Renders text.
    :param text: text to render.
    :param text_color: text color (RGB tuple).
    :param font_name: font name.
    :param font_size: font size.
    :return: rendered text.
    """
    font = pygame.font.SysFont(font_name, font_size)
    return font.render(text, False, text_color)


def blit_text(board, rendered_text, position):
    """
    Renders text on a cell square.
    :param board: Board instance.
    :param text: text.
    :return: None.
    """
    board.blit(rendered_text, position)


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