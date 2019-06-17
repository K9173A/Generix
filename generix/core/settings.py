"""
Generix settings.
"""
import os

import pygame

from generix.core.config import Config


def save_settings():
    # TODO
    pass


pygame.font.init()

app_data_root = os.path.join(os.path.expanduser('~'), '.generix')
if not os.path.exists(app_data_root):
    os.mkdir(app_data_root)

# General game parameters
game_config = Config(os.path.join(app_data_root, 'settings.ini'), "w")

WINDOW_WIDTH_PX = int(game_config.get_option('SETTINGS', 'window_width'))
WINDOW_HEIGHT_PX = int(game_config.get_option('SETTINGS', 'window_height'))
CELL_WIDTH_PX = int(game_config.get_option('SETTINGS', 'cell_width'))
CELL_HEIGHT_PX = int(game_config.get_option('SETTINGS', 'cell_height'))
BOARD_WIDTH_N = int(game_config.get_option('SETTINGS', 'board_width'))
BOARD_HEIGHT_N = int(game_config.get_option('SETTINGS', 'board_height'))
CELL_FONT = pygame.font.SysFont('Courier New', int(CELL_WIDTH_PX * 0.8))