"""player
    * Creates the player the user controls during game

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""
import pygame
from loadsources import *
from gameConstants import *


class Player(pygame.sprite.Sprite):
    """Player class
        * player is created
        * player is controlled by user

        Public Methods:
        * def get_layer(self)
        * def deathProtect(self)
        * def die(self)
        * def move(self, keys)
        * def update(self, realWallRects)
    """

    def __init__(self, realStartPos):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.idle_anim = load_animation("doctor_idle", scale=PLAYER_SIZE)
        self.sprint_anim = load_animation("doctor_sprint", scale=PLAYER_SIZE)
        self.death_anim = load_animation("doctor_death", scale=PLAYER_SIZE)
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.image = self.idle_anim[0]
        self.realRect = pygame.Rect(realStartPos, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.idle_anim[0].get_rect()
        self._calcRect()
        self._layer = int(self.realRect.top / BLOCK_SIZE)
        self.realArea = pygame.Rect((0, 0), REAL_GAME_SIZE)
        self.movex = 0
        self.movey = 0
        self.facingRight = True
        self.deathProtectCounter = 0
        self.dyingCounter = 0

    def _get_middle_value(self, valueList):
        """get middle value
            * Determines the value of a list with length 3, that is neither max nor min

        Args:
            valueList (list): Contains three values 

        Returns:
            valuelist[0](int): Returns the the value of a list with length 3, that is neither max nor min
        
        Test:
            * Returned value is neither max nor min value of the valueList
            * 
        """
        
        valueList.remove(max(valueList))
        valueList.remove(min(valueList))
        return valueList[0]

    def _turn(self):
        """turn
            * horizontally flips all images if player isn't dying

            Args:
                None

            Return:
                None
            
            Test:
                * Compare initial image with turned image
                * Image not turned when player is dying
        """

        if self.dyingCounter:
            return
        for i in range(0, len(self.idle_anim)):
            self.idle_anim[i] = pygame.transform.flip(self.idle_anim[i], True, False)
        for i in range(0, len(self.sprint_anim)):
            self.sprint_anim[i] = pygame.transform.flip(
                self.sprint_anim[i], True, False
            )
        for i in range(0, len(self.death_anim)):
            self.death_anim[i] = pygame.transform.flip(self.death_anim[i], True, False)

    def _calcRect(self):
        """calc rect
            * Calculates the real rect sizes(top down view) into display rect sizes(gamer view)

            Args:
                None
            
            Return:
                None
            
            Test:
                * 
                * 
        """
        self.rect.x = self.realRect.x - int(round(0.5 * BLOCK_SIZE))
        self.rect.y = int(round(0.7 * self.realRect.y)) + WALL_HEIGHT - self.rect.height

    def _handleWallCollisions(self, realWallRects):
        """handle wall collisions
            * Handles all possible collisions with stationary game objects

            Args:
                realWallRects (Rect): 

            Return:
                None

            Test:
                * All different possibilities of collissions with wall do not result in exception
                * 
        """
        
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
            if testCollide == -1 and -PLAYER_SPEED <= testDist <= PLAYER_SPEED:
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

    def get_layer(self):
        """get layer
            * Game screen is divided vertically into layers 

            Args:
                None

            Return:
                _layer(int): Current layer number a certain object stands on is returned
        """
        return self._layer

    def deathProtect(self):
        """death protect
            * player is protected while mask counter bigger than 0

            Args:
                None
            
            Return:
                None

            Test:
                * Collide with enemy after collecting mask
                * 
        """
        # Activate death protect for specified duration
        self.deathProtectCounter = int(round(PROTECT_DURATION * FRAMERATE))

    def die(self):
        """die 
            * after colliding with enemy (without masks) player animation changes

            Args:
                None

            Return:
                None
            
            Test:
                * Collide with enemy and observe animation
                * dyingCounter is iterating
        """
        # Play dying animation
        self.dyingCounter = int(round(DYING_DURATION * FRAMERATE))
        self.subFrameCounter = 0
        self.imageCounter = 0

    def move(self, keys):
        """move
            * player is moved according to pressed keys

            Args:
                keys (list): List of all pressed keys

            Return:
                None

            Test:
                * all pressed keys (w, a, s, d, arrow keys) change player position
                * press two keys (e.g. w, d) at the same time
        """
        movedY = False
        movedX = False
        # Change Speed of Player according to all pressed keys regarding order, change orientation if necessary
        for key in reversed(keys):
            if key == pygame.K_w and not movedY:
                self.movey = -PLAYER_SPEED
                movedY = True
            elif key == pygame.K_a and not movedX:
                # Flip if direction changes
                if self.facingRight:
                    self._turn()
                    self.facingRight = False
                self.movex = -PLAYER_SPEED
                movedX = True
            elif key == pygame.K_s and not movedY:
                self.movey = PLAYER_SPEED
                movedY = True
            elif not movedX:
                # Flip if direction changes
                if not self.facingRight:
                    self._turn()
                    self.facingRight = True
                self.movex = PLAYER_SPEED
                movedX = True

            if movedX and movedY:
                break

        if not movedX:
            self.movex = 0
        if not movedY:
            self.movey = 0

    def update(self, realWallRects):
        """update
            * animation updated after moved player

            Args:
                realWallRects (Rect): Reactangle of walls(top down view sizes)

            Return:
                None
            
            Test:
                * Move player and observe animation
                * Collide with wall
        """
        
        logging.debug("Updating player animation...")
        # Animate Character
        if self.subFrameCounter == ANIMATION_REFRESH - 1:
            # Increment ImageCounter
            newImageCount = self.imageCounter + 1
            if newImageCount >= len(self.idle_anim):
                if self.dyingCounter:
                    newImageCount = self.imageCounter
                else:
                    newImageCount = 0
            self.imageCounter = newImageCount

            # Set new Image
            if self.dyingCounter:
                self.image = self.death_anim[self.imageCounter]
            elif self.movex == 0 and self.movey == 0:
                self.image = self.idle_anim[self.imageCounter]
            else:
                self.image = self.sprint_anim[self.imageCounter]

            # Reset SubFrameCounter
            self.subFrameCounter = 0
        else:
            self.subFrameCounter += 1

        # Check if already dying
        if self.dyingCounter:
            # If yes, decrement counter and skip movement etc.
            self.dyingCounter = self.dyingCounter - 1
            return

        # Move Character
        if not self.movex == 0 and not self.movey == 0:
            self.movex = round(int(self.movex / 1.4))
            self.movey = round(int(self.movey / 1.4))
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
        self._calcRect()

        # Update layer
        self._layer = int(self.realRect.top / BLOCK_SIZE)

        # Decrement protect counter if greater 0
        if self.deathProtectCounter:
            self.deathProtectCounter = self.deathProtectCounter - 1

        # Let character blink if he is protected
        if (self.deathProtectCounter % 8) in range(5, 8):
            self.image = pygame.Surface((0, 0))
    logging.debug("Updating player animation was successful")
