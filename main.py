"""Sneaky Doctor
    * Main function that initializes pygame and creates menu

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""

import logging
from menu import Menu
import pygame
from gameConstants import *


# Configure logger
logging.basicConfig(filename='game.log', filemode='w',level=logging.INFO)
# Init game
logging.info("Initializing pygame...")
pygame.init()
logging.info("Initializing pygame was successfull")
pygame.display.set_mode(SCREEN_SIZE)

# Run game menu
main_menu = Menu()
main_menu.create_menu()
