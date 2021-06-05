import logging
import pygame
from gameConstants import *


class GameObject(pygame.sprite.Sprite):
    def __init__(self, surf, realPos):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = surf
        # Create 'real' rect for collision detect in 2.5D space
        self.realRect = pygame.Rect(realPos, (BLOCK_SIZE, BLOCK_SIZE))
        pos = (realPos[0], int(round(0.7 * realPos[1])))
        self.rect = surf.get_rect().move(pos)
        self._layer = int(self.realRect.top / BLOCK_SIZE)

    def moveLayer(self, offset):
        self._layer = self._layer + offset


class AnimatedGameObject(GameObject):
    def __init__(self, anim, realPos):
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.anim = anim
        GameObject.__init__(self, anim[0], realPos)  # call GameObject initializer

    def update(self, _):
        # Animate Object
        if self.subFrameCounter == ANIMATION_REFRESH - 1:
            # Increment ImageCounter
            newImageCount = self.imageCounter + 1
            if newImageCount >= len(self.anim):
                newImageCount = 0
            self.imageCounter = newImageCount

            # Set new Image
            self.image = self.anim[self.imageCounter]

            # Reset SubFrameCounter
            self.subFrameCounter = 0
        else:
            self.subFrameCounter += 1
