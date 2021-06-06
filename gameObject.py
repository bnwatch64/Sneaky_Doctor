"""gameObject
    * Hold the GameObject and AnimatedGameObject classes

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""
import logging
import pygame
from gameConstants import *


class GameObject(pygame.sprite.Sprite):
    """GameObject class
    * All stationary objects within game are objects of this class
    * Holds generic real rect, rect, image and layer attributes for right blitting

    Args:
        pygame.sprite.Sprite (class): Parent class of GameObject (inherits from)

    Public methods:
        def moveLayer(self, offset)
    """

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
    """AnimatedGameObject class
    * Extension of GameObject class
    * Adds attributes and functionality for object animation

    Args:
        GameObject (class): Parent class of AnimatedGameObject (inherits from)

    Public methods:
        def update(self, _)
    """

    def __init__(self, anim, realPos):
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.anim = anim
        GameObject.__init__(self, anim[0], realPos)  # call GameObject initializer

    def update(self, _):
        """update
        * Updates the image of the animated game object

        Args:
            None

        Return:
            None

        Test:
            * Check if imageCounter updates every ANIMATION_REFRESH time period
            * Check if self.image surface updates every ANIMATION_REFRESH time period
        """
        logging.info("Updating animated game objects...")
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
        logging.info("Updating animated game objects was successful")
