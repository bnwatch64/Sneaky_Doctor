import pygame
from player import Player
from loadsources import load_image

from gameConstants import *


class Game:
    def __init__(self, screenSize):
        self.screen = pygame.display.get_surface()
        self.caption = pygame.display.set_caption("Sneaky Doctor")
        self.clock = pygame.time.Clock()
        self.screenSize = screenSize
        # TODO: Ab hier in game_loop
        self.background, _ = load_image("bg.png")
        self.player = Player()
        self.allsprites = pygame.sprite.RenderUpdates()
        self.allsprites.add(self.player)

    def game_loop(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        going = True
        pressedKeys = []
        while going:
            self.clock.tick(FRAMERATE)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    going = False
                if event.type == pygame.KEYUP and event.key in [
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_s,
                    pygame.K_d,
                ]:
                    pressedKeys.remove(event.key)
                if event.type == pygame.KEYDOWN and event.key in [
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_s,
                    pygame.K_d,
                ]:
                    pressedKeys.append(event.key)
                self.player.move(pressedKeys)

            self.draw_sprites()
        pygame.quit()

    def draw_sprites(self):
        self.allsprites.clear(self.screen, self.background)
        self.allsprites.update()
        dirtyAreas = self.allsprites.draw(self.screen)
        pygame.display.update(dirtyAreas)
