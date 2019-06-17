"""
A module for a BoardHandler which manages Board instance.
"""
import pygame

from generix.core.board import Board
from generix.core.settings import BOARD_WIDTH_N, BOARD_HEIGHT_N
from generix.core.cell.factory import factory
from generix.core.cell.id import Cell
from generix.core.action.processor import processor
from generix.core.action.id import Action
from generix.core.cell.point import generate_random_point


class BoardHandler:
    """
    Handles boards state and manages statistics.
    """
    def __init__(self, statistics):
        """
        Constructs BoardHandler instance.
        :param statistics: GameStatistics instance which collects data.
        """
        self._prev_board = None
        self._curr_board = None
        self._factory = factory
        self._statistics = statistics
        self._clock = pygame.time.Clock()

    def create_new_board(self):
        """
        Creates new Board instance and initializes it.
        :return: None.
        """
        self._curr_board = Board(BOARD_WIDTH_N, BOARD_HEIGHT_N)
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
            self.init_board(self._curr_board, Cell.EMPTY_CELL)

            # Updates state of cells on the previous frame
            for cell in self._prev_board:
                self._statistics.update_counter(cell)
                self.update_cell(cell)

            # Updates visual state on the current frame
            for cell in self._curr_board:
                cell.render(self._curr_board)

            return self._curr_board
        return None

    def init_board(self, board, cell_name=None):
        """
        Initializes board instance with cells.
        :param board: board to be initialized.
        :param cell_name: cell enum value. None means random.
        :return: None.
        """
        for x in range(BOARD_WIDTH_N):
            for _ in range(BOARD_HEIGHT_N):
                if cell_name:
                    cell = self._factory.create_cell(cell_name)
                else:
                    cell = self._factory.create_random_cell()
                board.append_cell(x, cell)

    def fill_board(self, board):
        """
        Initializes board instance with cells which have 'amount' attribute in
        the settings.
        :param board:
        :return:
        """
        for item in self._factory.storage:
            try:
                amount = item.cls.__settings__['amount']
            except KeyError:
                continue
            while amount > 0:
                point = generate_random_point(0, BOARD_WIDTH_N - 1, 0, BOARD_HEIGHT_N - 1)
                cell = self._curr_board.get_cell(point)
                # Check whether the cell is empty or not, to replace it.
                if cell.settings('id') == Cell.EMPTY_CELL:
                    cell_name = self._factory.create_cell(item.cls.__settings__['id'])
                    board.set_cell(point, cell_name)
                    amount -= 1

    def switch_board(self):
        """
        Creates new board.
        :return: None.
        """
        self._prev_board = self._curr_board
        self._curr_board = Board(BOARD_WIDTH_N, BOARD_HEIGHT_N)

    def update_cell(self, cell):
        """
        Updates cell state.
        :param cell: Cell object.
        :return: None.
        """
        while True:
            action = cell.next_action()

            step_cost = cell.settings('step_cost')
            if step_cost:
                cell.change_hp(step_cost)
                # Breaks the loop if bot is dead.
                if cell.hp <= 0:
                    break

            context = self.prepare_action_context(action)
            # Cell is being used in every action, so pass it explicitly
            processor.execute(action, cell=cell, **context)
            # If action is final - breaks execution.
            # The control then moves to the next bot.
            if processor.find('id', action.value).object.settings('is_final'):
                break

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
                'curr_cell_types': [Cell.EMPTY_CELL],
                'next_cell_types': [Cell.EMPTY_CELL],
            }
        elif action == Action.STAY:
            return {
                'board': self._curr_board,
                'point': self._prev_board.prev_point,
            }
        elif action == Action.TURN:
            return {
                'angle': 45
            }
        else:
            raise ValueError('undefined action value:', action)

    def is_complete_simulation(self, iteration):
        for cell_type, cell_count in iteration.cells_counter.items():
            item = self._factory.find('type', cell_type)
            try:
                min_population = item.cls.__settings__['population']['min']
            except KeyError:
                continue
            else:
                if min_population >= cell_count:
                    return True
        return False




