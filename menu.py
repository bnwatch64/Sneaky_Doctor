import logging
import pygame
import pygame_menu
from gameView import GameView
from gameConstants import *


class Menu:
    def __init__(self):
        self.gameView = None
        self.screen = pygame.display.get_surface()

    def _start_game(self, newGame=False):
        self.gameView = GameView(newGame)
        self.gameView.game_loop()
        self.gameView = None

    def create_menu(self):
        """Create Menu
        * pygame_menu module is used
        * New Game, Continue, How To Play?, Highscores, Level Selector, Options, Quit buttons are created
        * First view of user

        Args:
            None

        Return:
            None
        """

        logging.info("Initializing Menu...")
        my_theme = pygame_menu.themes.Theme(
            widget_font=pygame_menu.font.FONT_8BIT,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            background_color=(0, 0, 0),
        )
        menu = pygame_menu.Menu(
            "Sneaky Doctor", SCREEN_SIZE[0], SCREEN_SIZE[1], theme=my_theme
        )
        menu.add.button("Continue", self._start_game)
        menu.add.button("New Game", self._start_game, True)
        menu.add.button("How To Play?")
        menu.add.button("Highscores")
        menu.add.button("Level Selector")
        menu.add.button("Options")
        menu.add.button("Quit", pygame_menu.events.EXIT)
        logging.info("Initializing Menu was successfull")
        menu.mainloop(self.screen)
