import pygame 
import pygame_menu
from game import Game

WINDOW_SIZE = [720, 720]

class Menu():
    def __init__(self):
        self.game = Game()
        self.screen = self.game.screen

    def create_menu(self):
        my_theme = pygame_menu.themes.Theme(
            widget_font=pygame_menu.font.FONT_8BIT, title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            background_color=(0,0,0))
        menu = pygame_menu.Menu("Sneaky Doctor",720,720, theme=my_theme)
        menu.add.button('New Game', self.game.game_loop)  
        menu.add.button('Continue',) 
        menu.add.button('How To Play?')   
        menu.add.button('Highscores')
        menu.add.button('Level Selector')
        menu.add.button('Options')
        menu.add.button('Quit', pygame_menu.events.EXIT)     
        menu.mainloop(self.screen)