import pygame
from game import Game
from gameConstants import *


class GameView:
    def __init__(self, screenSize):
        self.game = Game()
        self.screen = pygame.display.get_surface()
        self.caption = pygame.display.set_caption("Sneaky Doctor")
        self.clock = pygame.time.Clock()

    def game_loop(self):
        self.game.init_game()
        self.screen.fill(BAR_COLOR)
        self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
        pygame.display.flip()

        going = True
        while going:
            self.clock.tick(FRAMERATE)

            gameDirtyAreas, going = self.game.update_game()
            screenDirtyAreas = [x.move(0, BAR_HEIGHT) for x in gameDirtyAreas]
            self.screen.blit(self.game.screen, (0, BAR_HEIGHT))

            # TODO: Update information bars

            # Update the display
            pygame.display.update(screenDirtyAreas)
