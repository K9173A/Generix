"""
A module for an application base window.
"""
import pygame

from generix.core.handler import BoardHandler
from generix.core.settings import save_settings
from generix.core.statistics import GameStatistics


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
        self._statistics = GameStatistics()
        self._board_handler = BoardHandler(self._statistics)
        self._display = pygame.display.set_mode((width_px, height_px))

    def __del__(self):
        save_settings()

    def run(self):
        """
        Main loop of the game.
        :return: None.
        """
        self._board_handler.create_new_board()
        while not AppWindow.is_quit_event():
            updated_board = self._board_handler.update(fps=10, refresh_rate=2)
            if updated_board:
                self.refresh_display(updated_board)
            self._statistics.complete_iteration()
            iter = self._statistics.get_last_iteration()
            if self._board_handler.is_complete_simulation(iter):
                self._board_handler.create_new_board()

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
