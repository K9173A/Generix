"""
Application entry point.
"""
import pygame

# Imports to trigger class decorators which should register actions and cells
# before they will be accessed via storage classes (processor and factory).
import generix.core.cell.cell
import generix.core.action.action

from generix.core.app import AppWindow
from generix.core.settings import WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX


def main():
    """
    Application entry point.
    """
    pygame.init()
    app = AppWindow(WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX)
    app.run()


if __name__ == '__main__':
    main()