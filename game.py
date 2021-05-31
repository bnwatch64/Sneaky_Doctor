import pygame
from player import Player
from loadsources import load_image

FRAMERATE = 30
WINDOW_SIZE = [720, 720]
ASSETS_LOCATION = "assets"


class Game():
    def __init__(self):
        pygame.init()
        self.window_size = [720, 720]
        self.screen = pygame.display.set_mode(self.window_size)
        self.caption = pygame.display.set_caption("Sneaky Doctor")
        self.background,_ = load_image("bg.png")
        self.player = Player()
        self.clock = pygame.time.Clock()
        self.allsprites = pygame.sprite.RenderUpdates()
        self.allsprites.add(self.player)

    def game_loop(self):
        self.screen.blit(self.background, (0,0))
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
                if event.type == pygame.KEYUP and event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
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
        dirty_areas = self.allsprites.draw(self.screen)
        pygame.display.update(dirty_areas)