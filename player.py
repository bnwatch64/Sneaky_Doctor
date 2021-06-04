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

    def _get_middle_value(self, valueList):
        # Returns the the value of a list with length 3, that is neither max nor min
        valueList.remove(max(valueList))
        valueList.remove(min(valueList))
        return valueList[0]

    def _turn(self):
        # Horizontaly flips all images
        for i in range(0, len(self.idle_anim)):
            self.idle_anim[i] = pygame.transform.flip(self.idle_anim[i], True, False)
        for i in range(0, len(self.sprint_anim)):
            self.sprint_anim[i] = pygame.transform.flip(
                self.sprint_anim[i], True, False
            )

    def _handleWallCollisions(self, realWallRects):
        # Handles all possible collisions with stationary game objects
        collidedWallIdxs = self.realRect.collidelistall(realWallRects)

        # Only colliding with horizontal or vertical wall
        if 0 < len(collidedWallIdxs) < 3:
            collideRect = realWallRects[collidedWallIdxs[0]]
            testRect = self.realRect.copy()

            # Assume collision with vertical wall
            if self.movex > 0:
                # Moving right (and down/up)
                testRect.right = collideRect.left
            else:
                # Moving left (and down/up)
                testRect.left = collideRect.right

            # Test assumption
            testCollide = testRect.collidelist(realWallRects)
            testDist = self.realRect.x - testRect.x
            if testCollide == -1 and -CHARACTER_SPEED <= testDist <= CHARACTER_SPEED:
                # Assumption was correct and jump distance is in range, use it
                test1 = self.realRect[0]
                self.realRect = testRect.copy()
            else:
                # Assumption was wrong, handle collision with horizontal wall
                if self.movey > 0:
                    self.realRect.bottom = collideRect.top
                else:
                    self.realRect.top = collideRect.bottom

        # Colliding with a corner
        elif len(collidedWallIdxs) == 3:
            if self.movex > 0 and self.movey > 0:
                # Moving right down
                cornerIdx = max(collidedWallIdxs)
                cornerRect = realWallRects[cornerIdx]
                self.realRect.bottomright = cornerRect.topleft
            elif self.movex > 0 and self.movey < 0:
                # Moving right up
                cornerIdx = self._get_middle_value(collidedWallIdxs)
                cornerRect = realWallRects[cornerIdx]
                self.realRect.topright = cornerRect.bottomleft
            elif self.movex < 0 and self.movey > 0:
                # Moving left down
                cornerIdx = self._get_middle_value(collidedWallIdxs)
                cornerRect = realWallRects[cornerIdx]
                self.realRect.bottomleft = cornerRect.topright
            elif self.movex < 0 and self.movey < 0:
                # Moving left up
                cornerIdx = min(collidedWallIdxs)
                cornerRect = realWallRects[cornerIdx]
                self.realRect.topleft = cornerRect.bottomright

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
        self._handleWallCollisions(realWallRects)

        # Translate real rect to display rect
        self.rect.x = self.realRect.x - int(round(0.5 * BLOCK_SIZE))
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
