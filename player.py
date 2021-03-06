"""player
    * Holds the player class

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
    * Loads all animations (idle, sprint, death)
    * Initiates frame and image counter for animation handling
    * Initiates image, realRect, rect and _layer attributes for correct positioning and blitting
    * Initiates move and facing attributes for position and animation updates
    * Holds protect and death counter for special cases

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
        """get middle value (private)
            * Determines the value of a list with length 3, that is neither max nor min

        Args:
            valueList (list): Contains three values

        Returns:
            valuelist[0](int): Returns the the value of a list with length 3, that is neither max nor min

        Test:
            * Returned value is neither max nor min value of the valueList
            * Functions if e.g. all input values are the same
        """

        valueList.remove(max(valueList))
        valueList.remove(min(valueList))
        return valueList[0]

    def _turn(self):
        """turn (private)
        * horizontally flips all images if player changes orientation
        * gets skipped if player is dying (no more updates)

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
        """calc rect (private)
        * Calculates the display rect sizes (gamer view) from real rect sizes (top down view)

        Args:
            None

        Return:
            None

        Test:
            * Correct translation with different BLOCK_SIZE values
            * No going out of bonds (batch testing)
        """
        self.rect.x = self.realRect.x - int(round(0.5 * BLOCK_SIZE))
        self.rect.y = int(round(0.7 * self.realRect.y)) + WALL_HEIGHT - self.rect.height

    def _handleWallCollisions(self, realWallRects):
        """handle wall collisions (private)
        * Handles all possible collisions with stationary game objects
        * Pushes the player out of said objects if needed

        Args:
            realWallRects (Rect): List of all real rects (top down view) of stationary game objects (walls)

        Return:
            None

        Test:
            * All different possibilities of collissions with wall do not result in exception
            * Fast changing user inputs have no effect on functionality
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
        * Getter function for layer attribute for correct blitting in 2.5D space

        Args:
            None

        Return:
            _layer(int): Current layer number a certain object stands on is returned

        Test:
        * Actual value is returned
        * Value is in bonds
        """
        return self._layer

    def deathProtect(self):
        """death protect
        * Protects the player from dying for PROTECT_DURATION seconds
        * Sets the deathProtectCounter to respective value

        Args:
            None

        Return:
            None

        Test:
            * Player can't die when protected
            * Player gets protected when colliding with Enemy while having at least one mask
        """
        # Activate death protect for specified duration
        self.deathProtectCounter = int(round(PROTECT_DURATION * FRAMERATE))

    def die(self):
        """die
        * Change player animation to dying animation
        * Results in ignoring of all further user inputs

        Args:
            None

        Return:
            None

        Test:
            * Collide with enemy and observe animation
            * Player can't move while dying
        """
        # Play dying animation
        self.dyingCounter = int(round(DYING_DURATION * FRAMERATE))
        self.subFrameCounter = 0
        self.imageCounter = 0

    def move(self, keys):
        """move
        * Action handler for moving key presses (w, a, s, d, arrow keys)
        * Handles events where contradictory keys are pressed at the same time
        * Updates the movex, movey and facingRight properties accordingly

        Args:
            keys (list): List of all pressed keys

        Return:
            None

        Test:
            * all pressed keys (w, a, s, d, arrow keys) change player speed as expected
            * press two or more keys (e.g. w, d) at the same time
        """
        movedY = False
        movedX = False
        # Change Speed of Player according to all pressed keys regarding order, change orientation if necessary
        for key in reversed(keys):
            if key in [pygame.K_w, pygame.K_UP] and not movedY:
                self.movey = -PLAYER_SPEED
                movedY = True
            elif key in [pygame.K_a, pygame.K_LEFT] and not movedX:
                # Flip if direction changes
                if self.facingRight:
                    self._turn()
                    self.facingRight = False
                self.movex = -PLAYER_SPEED
                movedX = True
            elif key in [pygame.K_s, pygame.K_DOWN] and not movedY:
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
        * Sprite update function
        * Progresses animation
        * Cheks if player is dying
        * Moves the player with movex and movey in real 2.5D space
        * Handles wall and border collisions
        * Translates real (top down) rect into display rect
        * Updates the layer for right perspective blitting
        * Handles protected and dying events

        Args:
            realWallRects (Rect): List of real rectangles of walls (top down view sizes)

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
