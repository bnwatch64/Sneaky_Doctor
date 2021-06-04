import pygame
import pygame_menu
from gameView import GameView
from gameConstants import *


class Menu:
    def __init__(self, screenSize):
        self.gameView = GameView(screenSize)
        self.screen = pygame.display.get_surface()
        self.screenSize = screenSize

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
        my_theme = pygame_menu.themes.Theme(
            widget_font=pygame_menu.font.FONT_8BIT,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            background_color=(0, 0, 0),
        )
        menu = pygame_menu.Menu(
            "Sneaky Doctor", self.screenSize[0], self.screenSize[1], theme=my_theme
        )
        menu.add.button("New Game", self.gameView.game_loop)
        menu.add.button(
            "Continue",
        )
        menu.add.button("How To Play?")
        menu.add.button("Highscores")
        menu.add.button("Level Selector")
        menu.add.button("Options")
        menu.add.button("Quit", pygame_menu.events.EXIT)
        menu.mainloop(self.screen)
