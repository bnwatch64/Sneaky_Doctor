import pygame
from player import Player
from enemy import Enemy
from loadsources import load_image

from gameConstants import *


class Game:
    def __init__(self):
        self.screen = pygame.Surface(GAME_SIZE)
        self.pressedKeys = []
        self.background, _ = load_image("bg.png")
        self.allsprites = pygame.sprite.RenderUpdates()

    def init_game(self):
        self.player = Player(self.screen)
        self.allsprites.add(self.player)
        self.screen.blit(self.background, (0, 0))

    def update_game(self):
        # Update movement based on pressed keys
        self.player.move(self.pressedKeys)

        # Update the game Surface
        self.allsprites.clear(self.screen, self.background)
        self.allsprites.update()
        dirtyAreas = self.allsprites.draw(self.screen)

        # Return dirty dirtyAreas
        return dirtyAreas
