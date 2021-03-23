# Import Modules
import os, sys
import pygame as pg
from pygame.locals import *
from random import randrange


# functions to create our resources
def load_image(name, scale=None, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if scale is not None:
        image = pg.transform.scale(image, scale)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    image = image.convert_alpha()
    return image, image.get_rect()

def load_animation(folder, scale=None, colorkey=None):
    directory = os.path.join('assets', folder)

    images = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if not filename.endswith(".png"):
            continue
        fullname = os.path.join(directory, filename)

        try:
            image = pg.image.load(fullname)
        except pg.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)
        if scale is not None:
            image = pg.transform.scale(image, scale)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        image = image.convert_alpha()

        images.append(image)


    return images

# ---------------------------------------------------------------------------

# classes for our game objects
class Ball(pg.sprite.Sprite):
    def __init__(self, movex, movey):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('intro_ball.gif', scale=(80, 80))
        self.area = pg.display.get_surface().get_rect()
        self.movex = movex
        self.movey = movey

    def update(self):
        newpos = self.rect.move((self.movex, self.movey))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.movex = -self.movex
                newpos = self.rect.move((self.movex, 0))
            if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                self.movey = -self.movey
                newpos = self.rect.move((0, self.movey))
        self.rect = newpos


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.idle_anim = load_animation('doctor_idle', scale=(80, 77))
        self.walk_anim = load_animation('doctor_walk', scale=(80, 77))
        self.sprint_anim = load_animation('doctor_sprint', scale=(80, 77))
        self.subFrameCounter = 0
        self.imageCounter = 0
        self.image = self.idle_anim[0]
        self.rect = self.idle_anim[0].get_rect()
        self.area = pg.display.get_surface().get_rect()
        self.movex = 0
        self.movey = 0
        self.facingRight = True

    def _turn(self):
        # Horizontaly flips all images
        for i in range(0, len(self.idle_anim)):
            self.idle_anim[i] = pg.transform.flip(self.idle_anim[i], True, False)
        for i in range(0, len(self.walk_anim)):
            self.walk_anim[i] = pg.transform.flip(self.walk_anim[i], True, False)
        for i in range(0, len(self.sprint_anim)):
            self.sprint_anim[i] = pg.transform.flip(self.sprint_anim[i], True, False)

    def update(self):
        # Animate Character
        if self.subFrameCounter == 2:
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
            if key == pg.K_w and not movedY:
                self.movey = -5
                movedY = True
            elif key == pg.K_a and not movedX:
                #Flip if direction changes
                if self.facingRight:
                    self._turn()
                    self.facingRight = False
                self.movex = -5
                movedX = True
            elif key == pg.K_s and not movedY:
                self.movey = 5
                movedY = True
            elif not movedX:
                #Flip if direction changes
                if not self.facingRight:
                    self._turn()
                    self.facingRight = True
                self.movex = 5
                movedX = True

            if movedX and movedY:
                break

        if not movedX:
            self.movex = 0
        if not movedY:
            self.movey = 0

# ---------------------------------------------------------------------------

def main():
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((720, 720))
    pg.display.set_caption("Sneaky Doctor")
    pg.mouse.set_visible(0)

    # Create The Backgound
    background, _ = load_image('bg.png')

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    allsprites = pg.sprite.RenderUpdates()
    balls = pg.sprite.Group()
    for _ in range(5):
        movex = randrange(2, 10)
        movey = randrange(2, 10)
        newBall = Ball(movex, movey)
        balls.add(newBall)
        allsprites.add(newBall)
    player = Player()
    allsprites.add(player)


    # Main Loop
    going = True
    pressedKeys = []
    while going:
        clock.tick(30)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            if event.type == pg.KEYUP and event.key in [pg.K_w, pg.K_a, pg.K_s, pg.K_d]:
                pressedKeys.remove(event.key)
            if event.type == pg.KEYDOWN and event.key in [pg.K_w, pg.K_a, pg.K_s, pg.K_d]:
                pressedKeys.append(event.key)
            player.move(pressedKeys)

        # Draw Everything
        allsprites.clear(screen, background)
        allsprites.update()
        dirty_areas = allsprites.draw(screen)
        pg.display.update(dirty_areas)

    pg.quit()

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
