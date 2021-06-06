"""menu
    * Displaying menu
    * menu created with pygame_menu
    * pygame_menu has seperate user input handler

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""
import logging
import pygame
import pygame_menu
import os
from gameView import GameView
from gameConstants import *
from loadsources import check_save_file_exists


class Menu:
    """Menu class
    * Creates game menu providing 'continue', 'new game' and 'quit' functionality

    Public Methods:
        * def create_menu(self)
    """

    def __init__(self):
        self.gameView = None
        self.screen = pygame.display.get_surface()

    def _start_game(self, newGame=False):
        """start game (private)
        * Callback function for 'new game' and 'continue' UI buttons
        * Creates a new GameView object, runs the game with game_loop() and redraws the menu after

        Args:
            newGame (bool, optional): Determines whether game should be loaded from save file, defaults to False

        Return:
            None

        Test:
            * Value of newGame is passed to GameView initializer successfully
            * Menu is redrawn under all conditions
        """
        self.gameView = GameView(newGame)
        self.gameView.game_loop()
        self.gameView = None

        self.create_menu()

    def create_menu(self):
        """create menu
        * pygame_menu module is used
        * New Game, Continue, How To Play?, Highscores, Level Selector, Options, Quit buttons are created
        * First view of user

        Args:
            None

        Return:
            None

        Test:
            * Fonts are loaded correctly on different systems
            * 'continue' option is always greyed out if no save.json exists
        """

        logging.info("Initializing Menu...")
        my_theme = pygame_menu.themes.Theme(
            widget_font=pygame_menu.font.FONT_8BIT,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            title_font=pygame_menu.font.FONT_8BIT,
            title_font_size=75,
            background_color=(0, 0, 0),
        )
        myImage = pygame_menu.baseimage.BaseImage(
            image_path=os.path.join(ASSETS_LOCATION, "background.png"),
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER,
        )
        my_theme.background_color = myImage
        menu = pygame_menu.Menu(
            "Sneaky Doctor", SCREEN_SIZE[0], SCREEN_SIZE[1], theme=my_theme
        )
        pygame.font.init()
        if not check_save_file_exists():
            buttonContinue = menu.add.button("Continue")
            buttonContinue.set_font(
                font=pygame_menu.font.FONT_8BIT,
                font_size=30,
                color=(20, 20, 20, 0),
                selected_color=(20, 20, 20, 0),
                readonly_color=(255, 255, 255, 0),
                readonly_selected_color=(255, 255, 255, 0),
                background_color=(0, 0, 0, 255),
                antialias=False,
            )
        else:
            menu.add.button("Continue", self._start_game)
        menu.add.button("New Game", self._start_game, True)
        menu.add.button("Quit", pygame_menu.events.EXIT)
        logging.info("Initializing Menu was successfull")
        menu.mainloop(self.screen)
