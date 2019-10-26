"""
A module for an application base window.
"""
import os

import pygame

from generix.core.board.manager import BoardManager
from generix.core.data.db import Database
from generix.core.settings.registry import settings_reg
from generix.core.settings.settings import BOARD_FILE_PATH, LOAD_BOARD, FPS, REFRESH_RATE


class AppWindow:
    """
    Application base window.
    """
    def __init__(self, width_px, height_px):
        """
        Constructs application window.
        :param width_px: window width.
        :param height_px: window height.
        """
        self._db = Database()
        self._board_manager = BoardManager()
        self._display = pygame.display.set_mode((width_px, height_px))

    def run(self, experiment_name):
        """
        Main loop of the game.
        :param experiment_name: name of experiment to run.
        :return: None.
        """
        if self._db.find_experiment_by_name(experiment_name) is None:
            # Creates a new experiment in the DB
            self._db.create_experiment(experiment_name)

        # Creates new board for the experiment
        self._board_manager.create_new_board()
        if LOAD_BOARD:
            self._board_manager.load(BOARD_FILE_PATH)

        # Main loop of simulation
        i = 0
        while not AppWindow.is_quit_event():
            updated_board = self._board_manager.update(fps=FPS, refresh_rate=REFRESH_RATE)
            # Updates only if enough time passed
            if updated_board:
                self.refresh_display(updated_board)
            # Checks minimum population of cells to decide: should we continue or not
            if is_complete_simulation(self._board_manager.statistics):
                # Saves cells locations to the file
                self._board_manager.save(BOARD_FILE_PATH)
                # Saves statistics to the database
                self._db.create_simulation(experiment_name, i)
                # Creates new board to start a new simulation
                self._board_manager.create_new_board()
                # Loads cells locations from the file (from previous simulation)
                self._board_manager.load(BOARD_FILE_PATH)
                # TODO
                # 1) Считать геномы выживших ботов
                # 2) Клонировать каждую клетку n раз
                # 3) Мутировать n / 10 клеток
                self._board_manager.form_bots_generation()

            # Statistics is being recalculated on each iteration
            self._board_manager.renew_statistics()
            i += 1

    def refresh_display(self, bitmap):
        """
        Blits board pixels to the display.
        :return: None.
        """
        self._display.blit(bitmap, (0, 0))
        pygame.display.flip()

    @staticmethod
    def is_quit_event():
        """
        Handles clicking on the [X] button.
        :return: True if user clicked on the [X], otherwise - False.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False


def is_complete_simulation(iteration):
    """
    Compares current population of cells with minimum barrier and decides
    whether to continue simulation or not.
    :param iteration: statistics data.
    :return: True - continue simulation, False - stop simulation.
    """
    for cell_id, cell_count in iteration.cells_counter.items():
        min_population = settings_reg.find_option_by_key(cell_id, 'min')
        if min_population is None:
            continue
        if min_population >= cell_count:
            return True
    return False