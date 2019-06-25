"""
Generix settings.
"""
import os
import datetime

import pygame

from generix.core.cell.id import CellId
from generix.core.cell import cell
from generix.core.action import action
from generix.core.action.id import Action


pygame.font.init()

EXPERIMENT_NAME = 'ex-' + datetime.datetime.now().strftime('%d%b%Y%H%M%S')
FPS = 2
REFRESH_RATE = 2

# Default path where .generix directory is being created. Change it, if needed.
ROOT = os.path.expanduser('~')

# Application data root directory
app_data_root = os.path.join(ROOT, '.generix')
if not os.path.exists(app_data_root):
    os.mkdir(app_data_root)

# Database-related directory
DB_DIR_PATH = os.path.join(app_data_root, 'db')
if not os.path.exists(DB_DIR_PATH):
    os.mkdir(DB_DIR_PATH)

# Directory where all experiments configurations are stored as JSON files (boards and cells)
EXPERIMENTS_DIR_PATH = os.path.join(app_data_root, 'experiments')
if not os.path.exists(EXPERIMENTS_DIR_PATH):
    os.mkdir(EXPERIMENTS_DIR_PATH)

# Loads cells locations from the file
CURR_EXPERIMENT_DIR_PATH = os.path.join(EXPERIMENTS_DIR_PATH, EXPERIMENT_NAME)
if not os.path.exists(CURR_EXPERIMENT_DIR_PATH):
    os.mkdir(CURR_EXPERIMENT_DIR_PATH)

# Configuration file with experiment settings
SETTINGS_FILE_PATH = os.path.join(CURR_EXPERIMENT_DIR_PATH, 'settings.json')
LOAD_SETTINGS = os.path.exists(SETTINGS_FILE_PATH)

# Configuration file with board settings
BOARD_FILE_PATH = os.path.join(CURR_EXPERIMENT_DIR_PATH, 'settings.json')
LOAD_BOARD = os.path.exists(BOARD_FILE_PATH)

# Genomes configuration file path
# GENOME_FILE_PATH = os.path.join(EXPERIMENTS_DIR_PATH, 'genome.json')

# Application database file for simulation
DB_FILE_PATH = os.path.join(DB_DIR_PATH, 'generix.sqlite')

DEFAULT_SETTINGS = {
    'window': {
        'width': 900,
        'height': 800,
    },
    'board': {
        'rows': 20,
        'cols': 20,
    },
    'cell': {
        'width': 40,
        'height': 40,
        'text': {
            'font': 'Courier New',
            'color': (255, 255, 255),
            'size_multiplier': 0.8
        },
        CellId.EMPTY_CELL: {
            'cls': cell.EmptyCell,
            'color': (70, 70, 70),
            'chance': 10,
            'allowed_actions': [Action.STAY],
            'genome_max_len': 1,
        },
        CellId.STANDARD_CELL: {
            'ignore': True,
            'cls': cell.StandardCell,
            'color': (70, 70, 70),
            'chance': 5,
            'allowed_actions': [Action.STAY, Action.MOVE],
            'genome_max_len': 64,
        },
        CellId.FOOD_CELL: {
            'cls': cell.FoodCell,
            'color': (150, 0, 150),
            'amount': 30,
            # 'bonus': { 'on_kill': 20 },
            'allowed_actions': [Action.STAY],
            'genome_max_len': 1,
        },
        CellId.WALL_CELL: {
            'cls': cell.FoodCell,
            'color': (30, 30, 30),  # Dark gray
            'chance': 1,
            'allowed_actions': [Action.STAY],
            'genome_max_len': 1,
            'save_location': True
        },
        CellId.HUNTER_CELL: {
            'cls': cell.HunterCell,
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
    },
    'action': {
        Action.TURN: {
            'cls': action.Turn
        },
        Action.STAY: {
            'cls': action.Stay,
            'is_final': True
        },
        Action.MOVE: {
            'cls': action.Move,
            'is_final': True
        },
        Action.EAT: {
            'cls': action.Eat,
            'is_final': True
        },
        Action.LOOK: {
            'cls': action.Look
        }
    }
}
