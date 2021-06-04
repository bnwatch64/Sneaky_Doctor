import logging
import pygame
from pygame.font import SysFont
from game import Game
from gameConstants import *
from loadsources import *


# Dummy variables
changedLvl = 4
numMasks = 100
numDeaths = 20


class GameView:
    def __init__(self, screenSize):
        self.game = Game()
        self.screen = pygame.display.get_surface()
        self.caption = pygame.display.set_caption("Sneaky Doctor")
        self.clock = pygame.time.Clock()
        self.homeIconImg, _ = load_image("HomeIcon_Bar.png", scale=BUTTON_SIZE)
        self.speakerIconImg, _ = load_image("speaker_bar.png", scale=BUTTON_SIZE)
        self.speakerMuteIconImg, _ = load_image(
            "speaker_muted_bar.png", scale=BUTTON_SIZE
        )
        self.scullIconImg, _ = load_image("skull_bar.png", scale=ICON_SIZE)
        self.maskIconImg, _ = load_image("corona_mask.png", scale=ICON_SIZE)

    def game_loop(self):
        """Game loop
        * Background sound is set here
        * Game screen is drawn
        * while loop handles the events
        * Changed areas on screen are updated

        Args:
            None

        Return:
            None
        """
        self.game.init_game()
        self.drawBars(changedLvl)
        self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
        pygame.display.flip()
        load_sound("music.wav.mid")
        pygame.mixer.music.play(-1)
        musicplayer = True

        going = True
        while going:
            self.clock.tick(FRAMERATE)

            # Callback for the house icon
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    going = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    going = False

                if event.type == pygame.KEYUP and event.key in [
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_s,
                    pygame.K_d,
                ]:
                    self.game.pressedKeys.remove(event.key)

                if event.type == pygame.KEYDOWN and event.key in [
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_s,
                    pygame.K_d,
                ]:
                    self.game.pressedKeys.append(event.key)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.rectHome.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        going = False

                    elif self.rectSpeaker.collidepoint(mouse_pos):

                        if musicplayer:
                            pygame.mixer.music.stop()

                        else:
                            pygame.mixer.music.play(-1)

                        musicplayer = not musicplayer

            gameDirtyAreas = self.game.update_game()
            screenDirtyAreas = [x.move(0, BAR_HEIGHT) for x in gameDirtyAreas]
            self.screen.blit(self.game.screen, (0, BAR_HEIGHT))

            rectListDirty = self.updateBars(changedLvl, musicplayer)
            for rectDirty in rectListDirty:
                screenDirtyAreas.append(rectDirty)

            # Update the display
            pygame.display.update(screenDirtyAreas)

    def updateBars(self, currentLvl, musicplayer=None):
        """Update bars
            * Top and bottom bars are updated after change

        Args:
            currentLvl (int): Changed game level
            musicplayer (bool, optional): Clicking on speaker icon changes musicplayer boolean. Defaults to None.

        Returns:
            (list): List of rects which were changed

        # TODO: if condition has to be defined properly
        """

        if currentLvl != changedLvl:
            self.drawBars(currentLvl)
            return pygame.Rect(0, 0, GAME_SIZE[0], BAR_HEIGHT), pygame.Rect(
                0, BAR_HEIGHT + GAME_SIZE[1], GAME_SIZE[0], BAR_HEIGHT
            )

        elif musicplayer == True or musicplayer == False:
            self.drawBars(currentLvl, musicplayer)
            return [pygame.Rect(0, 0, GAME_SIZE[0], BAR_HEIGHT)]

        else:
            return []

    # TODO: Size of icon/Schrift abhängig von BarHeight
    def drawBars(self, currentLvl, musicplayer=True):
        """Draw bars
            * Top and bottom bars are drawn
            * At beginning of this function both bars are resetted
            * All icons and text fields within the bars are drawn here through blit function

        Args:
            currentLvl (int): Changed game level
            musicplayer (bool, optional): Clicking on speaker icon changes musicplayer boolean. Defaults to True.
        """
        self.screen.fill(BAR_COLOR, (0, 0, GAME_SIZE[0], BAR_HEIGHT))
        self.screen.fill(
            BAR_COLOR, (0, BAR_HEIGHT + GAME_SIZE[1], GAME_SIZE[0], BAR_HEIGHT)
        )

        # Level information
        # levelText = pygame.font.SysFont("None", FONT_SIZE)
        # textImg = levelText.render(
        #     f"Level: {currentLvl}/{NUM_LEVELS}", False, (0, 0, 0)
        # )
        # rect = textImg.get_rect()
        # pygame.draw.rect(textImg, (255, 255, 255, 128), rect, 1)
        # self.screen.blit(
        #     textImg, ((GAME_SIZE[0] - rect[2]) / 2, (BAR_HEIGHT - rect.height) / 2)
        # )

        # Home icon
        self.rectHome = pygame.Rect(
            X_PADDING,
            (BAR_HEIGHT - self.homeIconImg.get_height()) / 2,
            BUTTON_SIZE[0],
            BUTTON_SIZE[1],
        )
        self.screen.blit(
            self.homeIconImg, (X_PADDING, (BAR_HEIGHT - self.rectHome.height) / 2)
        )

        # Speaker Icon
        self.rectSpeaker = pygame.Rect(
            GAME_SIZE[0] - 2 * X_PADDING,
            (BAR_HEIGHT - self.homeIconImg.get_height()) / 2,
            BUTTON_SIZE[0],
            BUTTON_SIZE[1],
        )

        if musicplayer:
            self.screen.blit(
                self.speakerIconImg,
                (
                    GAME_SIZE[0] - 2 * X_PADDING,
                    (BAR_HEIGHT - self.rectSpeaker.height) / 2,
                ),
            )

        else:
            self.screen.blit(
                self.speakerMuteIconImg,
                (
                    GAME_SIZE[0] - 2 * X_PADDING,
                    (BAR_HEIGHT - self.rectSpeaker.height) / 2,
                ),
            )

        # Mask Icon
        rectMask = self.maskIconImg.get_rect()
        self.screen.blit(
            self.maskIconImg,
            (X_PADDING, BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectMask.height) / 2),
        )

        # Mask Text
        # numMaskText = pygame.font.SysFont("None", FONT_SIZE_BOTTOM_BAR)
        # textImgMask = numMaskText.render(f": {numMasks}", False, (0, 0, 0))
        # rectNum = textImgMask.get_rect()
        # pygame.draw.rect(textImgMask, (255, 255, 255, 128), rectNum, 1)
        # self.screen.blit(
        #     textImgMask,
        #     (
        #         1.5 * X_PADDING + rectMask.width,
        #         BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectMask.height) / 2,
        #     ),
        # )

        # Scull Icon
        rectScull = self.scullIconImg.get_rect()
        self.screen.blit(
            self.scullIconImg,
            (
                GAME_SIZE[0] - 5 * X_PADDING,
                BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectScull.height) / 2,
            ),
        )

        # Death Text
        # numDeathText = pygame.font.SysFont("None", FONT_SIZE_BOTTOM_BAR)
        # textImgDeath = numDeathText.render(f": {numDeaths}", False, (0, 0, 0))
        # rectNumDeath = textImgDeath.get_rect()
        # pygame.draw.rect(textImgDeath, (255, 255, 255, 128), rectNum, 1)
        # self.screen.blit(
        #     textImgDeath,
        #     (
        #         GAME_SIZE[0] - 3 * X_PADDING,
        #         BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectNumDeath.height) / 2,
        #     ),
        # )
