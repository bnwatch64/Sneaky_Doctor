import logging
import pygame
from gameLoader import *
from player import Player
from enemy import Enemy
from loadsources import load_image

from gameConstants import *


class Game:
    def __init__(self):
        self.screen = pygame.Surface(GAME_SIZE)
        self.pressedKeys = []
        self.floor = pygame.Surface(GAME_SIZE)
        self.allsprites = pygame.sprite.LayeredUpdates()

    def init_game(self):
        walls, self.realWallRects = load_level(1)
        self.player = Player(
            self.screen.get_rect(), (GAME_SIZE[0] / 2, GAME_SIZE[0] / 2)
        )
        self.allsprites.add(self.player)
        self.allsprites.add(walls)
        self.floor.fill(FLOOR_COLOR)
        self.screen.blit(self.floor, (0, 0))

    def update_game(self):
        # Update movement based on pressed keys
        self.player.move(self.pressedKeys)

        # Update the game Surface
        self.allsprites.clear(self.screen, self.floor)
        self.allsprites.update(self.realWallRects)
        # Update the layers of all movable game objects
        self.allsprites.change_layer(self.player, self.player.get_layer())
        dirtyAreas = self.allsprites.draw(self.screen)

        # Return dirty areas
        return dirtyAreas
