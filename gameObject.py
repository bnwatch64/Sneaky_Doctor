import logging
import pygame
from gameConstants import *


class GameObject(pygame.sprite.Sprite):
    def __init__(self, surf, realPos, layer):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = surf
        # Create 'real' rect for collision detect in 2.5D space
        self.realRect = pygame.Rect(realPos, (BLOCK_SIZE, BLOCK_SIZE))
        pos = (realPos[0], int(round(0.7 * realPos[1])))
        self.rect = surf.get_rect().move(pos)
        self._layer = layer
