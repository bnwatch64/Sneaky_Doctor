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
        going = True

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            if event.type == pygame.KEYUP and event.key in [
                pygame.K_w,
                pygame.K_a,
                pygame.K_s,
                pygame.K_d,
            ]:
                self.pressedKeys.remove(event.key)
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_w,
                pygame.K_a,
                pygame.K_s,
                pygame.K_d,
            ]:
                self.pressedKeys.append(event.key)

            self.player.move(self.pressedKeys)

        # Update the game Surface
        self.allsprites.clear(self.screen, self.background)
        self.allsprites.update()
        dirtyAreas = self.allsprites.draw(self.screen)

        # Return dirty dirtyAreas
        return dirtyAreas, going
