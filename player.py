import pygame
from loadsources import *
from gameConstants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, parentRect, realStartPos):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.idle_anim = load_animation("doctor_idle", scale=PLAYER_SIZE)
        self.sprint_anim = load_animation("doctor_sprint", scale=PLAYER_SIZE)
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.image = self.idle_anim[0]
        self.realRect = pygame.Rect(realStartPos, (BLOCK_SIZE, BLOCK_SIZE))
        startPos = (realStartPos[0], int(round(0.7 * realStartPos[1])))
        self.rect = self.idle_anim[0].get_rect().move(startPos)
        self._layer = int(self.realRect.top / BLOCK_SIZE)
        self.realArea = pygame.Rect((0, 0), REAL_GAME_SIZE)
        self.movex = 0
        self.movey = 0
        self.facingRight = True

    def _turn(self):
        # Horizontaly flips all images
        for i in range(0, len(self.idle_anim)):
            self.idle_anim[i] = pygame.transform.flip(self.idle_anim[i], True, False)
        for i in range(0, len(self.sprint_anim)):
            self.sprint_anim[i] = pygame.transform.flip(
                self.sprint_anim[i], True, False
            )

    def update(self, realWallRects):
        # Animate Character
        if self.subFrameCounter == ANIMATION_REFRESH - 1:
            # Increment ImageCounter
            newImageCount = self.imageCounter + 1
            if newImageCount >= len(self.idle_anim):
                newImageCount = 0
            self.imageCounter = newImageCount

            # Set new Image
            if self.movex == 0 and self.movey == 0:
                self.image = self.idle_anim[self.imageCounter]
            else:
                self.image = self.sprint_anim[self.imageCounter]

            # Reset SubFrameCounter
            self.subFrameCounter = 0
        else:
            self.subFrameCounter += 1

        # Move Character
        newRealPos = self.realRect.move((self.movex, self.movey))
        self.realRect = newRealPos

        # Keep character in bounds
        if not self.realArea.contains(newRealPos):
            if self.realRect.left < self.realArea.left:
                self.realRect.left = self.realArea.left
            if self.realRect.right > self.realArea.right:
                self.realRect.right = self.realArea.right
            if self.realRect.top < self.realArea.top:
                self.realRect.top = self.realArea.top
            if self.realRect.bottom > self.realArea.bottom:
                self.realRect.bottom = self.realArea.bottom

        # Handle wall collisions

        # PROBLEM: bei gleichzeitig movex und movey veruscht sich in wand zu glitchen
        # PROBLEM: Nach rechts zu spät
        collidedWallIdx = self.realRect.collidelist(realWallRects)
        if not collidedWallIdx == -1:
            collideRect = realWallRects[collidedWallIdx]
            if not self.movex == 0:
                if self.movex > 0:
                    # Moving right
                    self.realRect.right = collideRect.left - 1
                else:
                    # Moving left
                    self.realRect.left = collideRect.right + 1

            if not self.movey == 0:
                if self.movey > 0:
                    # Moving down
                    self.realRect.bottom = collideRect.top - 1
                else:
                    # Moving up
                    self.realRect.top = collideRect.bottom + 1

        # Translate real rect to display rect
        self.rect.x = self.realRect.x
        self.rect.y = int(round(0.7 * self.realRect.y)) + WALL_HEIGHT - self.rect.height

        # Update layer
        self._layer = int(self.realRect.top / BLOCK_SIZE)

    def get_layer(self):
        return self._layer

    def move(self, keys):
        movedY = False
        movedX = False
        # Change Speed of Player according to all pressed keys regarding order, change orientation if necessary
        for key in reversed(keys):
            if key == pygame.K_w and not movedY:
                self.movey = -CHARACTER_SPEED
                movedY = True
            elif key == pygame.K_a and not movedX:
                # Flip if direction changes
                if self.facingRight:
                    self._turn()
                    self.facingRight = False
                self.movex = -CHARACTER_SPEED
                movedX = True
            elif key == pygame.K_s and not movedY:
                self.movey = CHARACTER_SPEED
                movedY = True
            elif not movedX:
                # Flip if direction changes
                if not self.facingRight:
                    self._turn()
                    self.facingRight = True
                self.movex = CHARACTER_SPEED
                movedX = True

            if movedX and movedY:
                break

        if not movedX:
            self.movex = 0
        if not movedY:
            self.movey = 0
