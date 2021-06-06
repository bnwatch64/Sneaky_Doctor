import logging
import pygame
from pygame.font import SysFont
import os
from game import Game
from gameLoader import GameLoader
from loadsources import *
from gameConstants import *


class GameView:
    """Game View Creation
    * Class draws the UI within the game (top, bottom bars, icons within bars)
    * Handles the user input during game
    * Updates the bars after a change

    Public Methods:
        * def game_loop(self)
        * def updateGameStats(self, playingMusicChanged=False)
        * def drawBars(self)


    """

    def __init__(self, newGame):
        self.gameLoader = GameLoader()
        if not newGame:
            # Load game from save file if not newGame
            self.gameStats = load_game_save()
        else:
            # Create new game else
            self.gameStats = {"currentLvl": 1, "maskCount": 0, "deathCount": 0}
        # Create game object
        self.game = Game(self.gameLoader, self.gameStats)
        self.screen = pygame.display.get_surface()
        self.caption = pygame.display.set_caption("Sneaky Doctor")
        self.clock = pygame.time.Clock()
        self.homeIconImg, _ = load_image("icons/HomeIcon_Bar.png", scale=BUTTON_SIZE)
        self.speakerIconImg, _ = load_image("icons/speaker_bar.png", scale=BUTTON_SIZE)
        self.speakerMuteIconImg, _ = load_image(
            "icons/speaker_muted_bar.png", scale=BUTTON_SIZE
        )
        self.scullIconImg, _ = load_image("icons/skull_bar.png", scale=ICON_SIZE)
        self.maskIconImg, _ = load_image("icons/corona_mask.png", scale=ICON_SIZE)
        self.winGameAnim = load_animation("win_anim", scale=GAME_SIZE)
        self.playingMusic = True

    def _winGame(self):
        going = True
        imageCounter = 0
        winAnimPos = (0, BAR_HEIGHT)
        while going:
            self.clock.tick(int(round(FRAMERATE / ANIMATION_REFRESH)))

            # Check game close conditions
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    going = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    going = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    going = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.rectHome.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        going = False

            # Increment ImageCounter
            newImageCount = imageCounter + 1
            if newImageCount >= len(self.winGameAnim):
                newImageCount = 0
            imageCounter = newImageCount

            # Blit new Image
            self.screen.blit(self.winGameAnim[imageCounter], winAnimPos)
            pygame.display.update(
                [(winAnimPos[0], winAnimPos[1], GAME_SIZE[0], GAME_SIZE[1])]
            )

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

        Test:
            * w, a, s, d, esc buttons have functionality
            * while loop interrupted when clicking on home icon
        """

        # Setup display of game
        self.drawBars()
        self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
        pygame.display.flip()
        # Setup sound
        load_sound("music.wav.mid")
        pygame.mixer.music.play(-1)

        # Start game loop
        won = False
        going = True
        while going:
            self.clock.tick(FRAMERATE)

            playingMusicChanged = False
            # Input handling
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

                        if self.playingMusic:
                            pygame.mixer.music.stop()

                        else:
                            pygame.mixer.music.play(-1)

                        self.playingMusic = not self.playingMusic
                        playingMusicChanged = True

            # Update the game
            gameDirtyAreas = self.game.update_game()
            screenDirtyAreas = [x.move(0, BAR_HEIGHT) for x in gameDirtyAreas]
            self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
            # Update the information bars
            barsDirtyAreas = self.updateGameStats(playingMusicChanged)
            screenDirtyAreas.extend(barsDirtyAreas)

            # Update the display
            pygame.display.update(screenDirtyAreas)

            # Restart level if player died
            if self.game.checkDeath():
                newGameStats = self.game.gameStats.copy()
                newGameStats["deathCount"] = newGameStats["deathCount"] + 1
                self.game = Game(self.gameLoader, newGameStats, self.game.pressedKeys)
                self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
                pygame.display.flip()
            # Load new level if win
            elif self.game.checkWin():
                newGameStats = self.game.gameStats.copy()
                newGameStats["currentLvl"] = newGameStats["currentLvl"] + 1
                if not check_level_exists(newGameStats["currentLvl"]):
                    self._winGame()
                    going = False
                    won = True
                else:
                    self.game = Game(
                        self.gameLoader, newGameStats, self.game.pressedKeys
                    )
                    self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
                    pygame.display.flip()

        if won:
            delete_game_save()
        else:
            save_game(self.gameStats)

    def updateGameStats(self, playingMusicChanged=False):
        """Update game stats
            * Local gameStats and info bars are updated if game stats changed

        Args:
            playingMusicChanged (bool, optional): Determines whether playingMusic icon should be updated

        Return:
            (list): List of dirty rects from info bar updates

        Test:
            * Values in Top and Bottom bars drawn with updated game stats
            * Only the changed areas within bars are updated not the full area of both bars
        """

        if self.gameStats != self.game.gameStats:
            # If gameStats changed, update them
            self.gameStats = self.game.gameStats.copy()
            # Redraw info bars
            self.drawBars()
            # Return new dirty areas from bars
            return [
                pygame.Rect(0, 0, GAME_SIZE[0], BAR_HEIGHT),
                pygame.Rect(0, BAR_HEIGHT + GAME_SIZE[1], GAME_SIZE[0], BAR_HEIGHT),
            ]

        elif playingMusicChanged:
            # If music player changed, update bars
            self.drawBars()
            # Return new dirty area from top bar
            return [pygame.Rect(0, 0, GAME_SIZE[0], BAR_HEIGHT)]

        else:
            # If there are no changes, return no new dirty areas
            return []

    # TODO: Size of icon/Schrift abhängig von BarHeight
    def drawBars(self):
        """Draw bars
        * Top and bottom bars are drawn
        * At beginning of this function both bars are resetted
        * All icons and text fields within the bars are drawn here through blit function

        Args:
            None

        Return:
            None

        Test:
            * Top and Bottom bars created (UI testing)
            * Home and speaker icon clickable
        """

        logging.info("Drawing info bars...")
        self.screen.fill(BAR_COLOR, (0, 0, GAME_SIZE[0], BAR_HEIGHT))
        self.screen.fill(
            BAR_COLOR, (0, BAR_HEIGHT + GAME_SIZE[1], GAME_SIZE[0], BAR_HEIGHT)
        )

        # Level information
        levelText = pygame.font.SysFont("None", FONT_SIZE)
        textImg = levelText.render(
            f"Level: {self.gameStats['currentLvl']}/{NUM_LEVELS}",
            False,
            (231, 231, 231),
        )
        rect = textImg.get_rect()
        pygame.draw.rect(textImg, BAR_COLOR, rect, 1)
        self.screen.blit(
            textImg,
            (
                (GAME_SIZE[0] - rect.width) / 2,
                (BAR_HEIGHT - rect.height - levelText.get_descent()) / 2,
            ),
        )

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

        if self.playingMusic:
            self.screen.blit(
                self.speakerIconImg,
                (
                    GAME_SIZE[0] - (self.rectSpeaker.width + X_PADDING),
                    (BAR_HEIGHT - self.rectSpeaker.height) / 2,
                ),
            )

        else:
            self.screen.blit(
                self.speakerMuteIconImg,
                (
                    GAME_SIZE[0] - (self.rectSpeaker.width + X_PADDING),
                    (BAR_HEIGHT - self.rectSpeaker.height) / 2,
                ),
            )

        # Mask Icon
        rectMask = self.maskIconImg.get_rect()
        maskPos = (
            X_PADDING,
            BAR_HEIGHT + GAME_SIZE[1] + round((BAR_HEIGHT - rectMask.height) / 2),
        )
        self.screen.blit(
            self.maskIconImg,
            maskPos,
        )

        # Mask Text
        numMaskText = pygame.font.SysFont("None", FONT_SIZE_BOTTOM_BAR)
        textImgMask = numMaskText.render(
            f": {self.gameStats['maskCount']}", False, (231, 231, 231)
        )
        rectNumMask = textImgMask.get_rect()
        pygame.draw.rect(textImgMask, BAR_COLOR, rectNumMask, 1)
        self.screen.blit(
            textImgMask,
            (
                maskPos[0] + rectMask.width + 5,
                BAR_HEIGHT
                + GAME_SIZE[1]
                + (BAR_HEIGHT - rectNumMask.height - numMaskText.get_descent()) / 2,
            ),
        )

        # Death Text
        numDeathText = pygame.font.SysFont("None", FONT_SIZE_BOTTOM_BAR)
        textImgDeath = numDeathText.render(
            f": {self.gameStats['deathCount']}", False, (231, 231, 231)
        )
        rectNumDeath = textImgDeath.get_rect()
        pygame.draw.rect(textImgDeath, BAR_COLOR, rectNumDeath, 1)
        numDeathPos = (
            GAME_SIZE[0] - (rectNumDeath.x + rectNumDeath.width + X_PADDING),
            BAR_HEIGHT
            + GAME_SIZE[1]
            + (BAR_HEIGHT - rectNumDeath.height - numDeathText.get_descent()) / 2,
        )
        self.screen.blit(
            textImgDeath,
            numDeathPos,
        )

        # Scull Icon
        rectScull = self.scullIconImg.get_rect()
        self.screen.blit(
            self.scullIconImg,
            (
                numDeathPos[0] - rectScull.width - 5,
                BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectScull.height) / 2,
            ),
        )

        logging.info("Drawing info bars was successful")
