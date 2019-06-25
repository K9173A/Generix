"""
Application entry point.
"""
import pygame

from generix.core.app import AppWindow
from generix.core.settings.registry import settings_reg
from generix.core.settings.settings import EXPERIMENT_NAME


def main():
    """
    Application entry point.
    """
    pygame.init()
    width = settings_reg.find_option_by_key('window', 'width')
    height = settings_reg.find_option_by_key('window', 'height')
    app = AppWindow(width, height)
    app.run(EXPERIMENT_NAME)


if __name__ == '__main__':
    main()