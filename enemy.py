import logging
import pygame
from loadsources import *
from gameConstants import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, parentSurface):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.anims = load_enemy_animations(scale=ENEMY_SIZE)
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.image = self.anims["right"][0]
        self.rect = self.anims["right"][0].get_rect().move([x / 2 for x in GAME_SIZE])
        self.area = parentSurface.get_rect()
        self.movex = 0
        self.movey = 0
        self.facing = "right"

    def update(self):
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

        # Move Character
        newpos = self.rect.move((self.movex, self.movey))
        self.rect = newpos
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left:
                self.rect.left = self.area.left
            if self.rect.right > self.area.right:
                self.rect.right = self.area.right
            if self.rect.top < self.area.top:
                self.rect.top = self.area.top
            if self.rect.bottom > self.area.bottom:
                self.rect.bottom = self.area.bottom

    def move(self, keys):
        movedY = False
        movedX = False
        # Change Speed of Enemy according to all pressed keys regarding order
        # Change orientation if necessary
        for key in reversed(keys):
            if key == pygame.K_w and not movedY:
                self.facing = "back"
                self.movey = -CHARACTER_SPEED
                movedY = True
            elif key == pygame.K_a and not movedX:
                self.facing = "left"
                self.movex = -CHARACTER_SPEED
                movedX = True
            elif key == pygame.K_s and not movedY:
                self.facing = "front"
                self.movey = CHARACTER_SPEED
                movedY = True
            elif not movedX:
                self.facing = "right"
                self.movex = CHARACTER_SPEED
                movedX = True

            if movedX and movedY:
                break

        if not movedX:
            self.movex = 0
        if not movedY:
            self.movey = 0
