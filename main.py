from menu import Menu
import pygame
from gameConstants import *


# TODO:
# Docstrings in all files, functions, classes
# Instead of print() use log file with important log messages

pygame.init()
screenSize = [GAME_SIZE[0], GAME_SIZE[1] + 2 * BAR_HEIGHT]
pygame.display.set_mode(screenSize)

main_menu = Menu(screenSize)
main_menu.create_menu()