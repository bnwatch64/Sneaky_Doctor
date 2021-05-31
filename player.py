import pygame 
from loadsources import *

ANIMATION_REFRESH = 3
WINDOW_SIZE = [720, 720]
CHARACTER_SPEED = 7
PLAYER_SIZE = (80, 77)  # Always keep 200x230 ratio


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.idle_anim = load_animation("doctor_idle", scale=(80, 77))
        self.walk_anim = load_animation("doctor_walk", scale=(80, 77))
        self.sprint_anim = load_animation("doctor_sprint", scale=(80, 77))
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.image = self.idle_anim[0]
        self.rect = self.idle_anim[0].get_rect().move([x / 2 for x in WINDOW_SIZE])
        self.area = pygame.display.get_surface().get_rect()
        self.movex = 0
        self.movey = 0
        self.facingRight = True

    def _turn(self):
        # Horizontaly flips all images
        for i in range(0, len(self.idle_anim)):
            self.idle_anim[i] = pygame.transform.flip(self.idle_anim[i], True, False)
        for i in range(0, len(self.walk_anim)):
            self.walk_anim[i] = pygame.transform.flip(self.walk_anim[i], True, False)
        for i in range(0, len(self.sprint_anim)):
            self.sprint_anim[i] = pygame.transform.flip(self.sprint_anim[i], True, False)

    def update(self):
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