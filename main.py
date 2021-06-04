import logging
from menu import Menu
import pygame
from gameConstants import *


# Configure debugger
logging.basicConfig(level=logging.DEBUG)
# Init game
logging.info("Initializing pygame...")
pygame.init()
logging.info("Initializing  pygame was successfull")
screenSize = [GAME_SIZE[0], GAME_SIZE[1] + 2 * BAR_HEIGHT]
pygame.display.set_mode(screenSize)

# Run game menu
main_menu = Menu(screenSize)
main_menu.create_menu()
