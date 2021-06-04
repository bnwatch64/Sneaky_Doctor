import logging
import pygame
from loadsources import *
from gameConstants import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, realStartPos, path):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.anims = load_enemy_animations(scale=ENEMY_SIZE)
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.image = self.anims["right"][0]
        self.realRect = pygame.Rect(realStartPos, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.anims["right"][0].get_rect()
        self._calcRect()
        self._layer = int(self.realRect.top / BLOCK_SIZE)
        self.realArea = pygame.Rect((0, 0), REAL_GAME_SIZE)
        self.path = path
        self.pathPos = path.index(realStartPos)
        self.speed = MAX_NPC_SPEED  # TODO: Change according to transparency
        self.facing = "right"

    def get_layer(self):
        return self._layer

    def _calcRect(self):
        self.rect.x = self.realRect.x - int(round(0.25 * BLOCK_SIZE))
        self.rect.y = int(round(0.7 * self.realRect.y)) + WALL_HEIGHT - self.rect.height

    def _move(self):
        # Get the next position alongside the path
        newPathPos = self.pathPos + self.speed
        if self.speed > 0:
            overshoot = newPathPos - len(self.path) + 1
            if overshoot > 0:
                newPathPos = len(self.path) - overshoot
                self.speed = -self.speed
        else:
            overshoot = -newPathPos
            if overshoot > 0:
                newPathPos = overshoot
                self.speed = -self.speed

        # Update facing attribute
        xDiff = self.path[newPathPos][0] - self.path[self.pathPos][0]
        yDiff = self.path[newPathPos][1] - self.path[self.pathPos][1]
        if abs(xDiff) >= abs(yDiff):
            if xDiff > 0:
                # Moving right
                self.facing = "right"
            else:
                # Moving left
                self.facing = "left"
        elif abs(xDiff) < abs(yDiff):
            if yDiff > 0:
                # Moving down
                self.facing = "front"
            else:
                # Moving up
                self.facing = "back"

        # Update path index position and real position
        self.pathPos = newPathPos
        return self.path[self.pathPos]

    def update(self, _):
        # Move Character
        newRealPos = self._move()
        self.realRect.update(newRealPos, self.realRect.size)

        # Animate Character
        if self.subFrameCounter == ANIMATION_REFRESH - 1:
            # Increment ImageCounter
            newImageCount = self.imageCounter + 1
            if newImageCount >= len(self.anims[self.facing]):
                newImageCount = 0
            self.imageCounter = newImageCount

            # Set new Image
            self.image = self.anims[self.facing][self.imageCounter]

            # Reset SubFrameCounter
            self.subFrameCounter = 0
        else:
            self.subFrameCounter += 1

        # Translate real rect to display rect
        self._calcRect()

        # Update layer
        self._layer = int(self.realRect.top / BLOCK_SIZE)
