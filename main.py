"""Sneaky Doctor
    authors: Benjamin Ader & Sujan Kanapathipillai
    date: 02.06.2021
    license: free
"""

import logging
from menu import Menu
import pygame
from gameConstants import *


# Configure debugger
logging.basicConfig(level=logging.DEBUG)
# Init game
logging.info("Initializing pygame...")
pygame.init()
logging.info("Initializing pygame was successfull")
pygame.display.set_mode(SCREEN_SIZE)

# Run game menu
main_menu = Menu()
main_menu.create_menu()
