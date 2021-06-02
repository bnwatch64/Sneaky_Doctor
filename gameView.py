import pygame
from pygame.font import SysFont
from game import Game
from gameConstants import *
from loadsources import *


# Dummy variables 

changedLvl = 4
numMasks = 5


class GameView:
    def __init__(self, screenSize):
        self.game = Game()
        self.screen = pygame.display.get_surface()
        self.caption = pygame.display.set_caption("Sneaky Doctor")
        self.clock = pygame.time.Clock()
        self.homeIconImg, _ = load_image("HomeIcon_Bar.png", scale=BUTTON_SIZE)
        self.speakerIconImg, _ = load_image("speaker_bar.png", scale=BUTTON_SIZE)
        self.scullIconImg, _ = load_image("skull_bar.png", scale=ICON_SIZE)
        self.maskIconImg, _ = load_image("corona_mask.png", scale=ICON_SIZE)
  

    def game_loop(self):
        self.game.init_game()
        # TODO: Avoid full path
        musicplayer = True
        mfxBackground = pygame.mixer.music.load("C:\\Users\\sujan\\Documents\\Duales Studium\\Theorie\\4.Semester\\Python\\Sneaky_Doctor\\assets\\music.wav.mid")
        pygame.mixer.music.play(-1)
        self.drawBars(changedLvl)
        self.screen.blit(self.game.screen, (0, BAR_HEIGHT))
        pygame.display.flip()

        going = True
        while going:
            self.clock.tick(FRAMERATE)
            # Callback for the house icon
            for event in pygame.event.get():                  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()                        
                    if self.rectHome.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        going = False

                    elif self.rectSpeaker.collidepoint(mouse_pos):
                        # TODO: Mute the sound
                        if musicplayer:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1)
                        musicplayer = not musicplayer
                        

            gameDirtyAreas, _ = self.game.update_game()
            screenDirtyAreas = [x.move(0, BAR_HEIGHT) for x in gameDirtyAreas]
            self.screen.blit(self.game.screen, (0, BAR_HEIGHT))

            # Update information bars

            # TODO: Delete 
            # Dummy level list
            currentLvl = [2, 3, 5, 6, 7]
            for i in currentLvl :
                rectListDirty = self.updateBars(i)
                for rectDirty in rectListDirty:
                    screenDirtyAreas.append(rectDirty)

            # Update the display
            pygame.display.update(screenDirtyAreas)

            


    def updateBars(self, currentLvl):
        # TODO: if condition has to be defined properly 
        if currentLvl != changedLvl:
            # This invoke results in bad performance --> Ask Benni
            #self.drawBars(currentLvl)
            return pygame.Rect(0,0, GAME_SIZE[0], BAR_HEIGHT), pygame.Rect(0, BAR_HEIGHT + GAME_SIZE[1], GAME_SIZE[0], BAR_HEIGHT)
        else:
            return []

    # TODO: Size of icon/Schrift abhängig von BarHeight
    def drawBars(self, currentLvl):
        self.screen.fill(BAR_COLOR, (0, 0, GAME_SIZE[0], BAR_HEIGHT))
        self.screen.fill(BAR_COLOR, (0, BAR_HEIGHT + GAME_SIZE[1], GAME_SIZE[0], BAR_HEIGHT))
   
        # Level information
        levelText = pygame.font.SysFont('None', FONT_SIZE)
        textImg = levelText.render(f"Level: {currentLvl}/{NUM_LEVELS}", False, (0,0,0))
        rect = textImg.get_rect()
        pygame.draw.rect(textImg, (255,255,255, 128), rect, 1)
        self.screen.blit(textImg, ((GAME_SIZE[0] - rect[2])/2, (BAR_HEIGHT - rect.height)/2))

        # Home icon
        self.rectHome = pygame.Rect(X_PADDING,(BAR_HEIGHT - self.homeIconImg.get_height())/2, BUTTON_SIZE[0], BUTTON_SIZE[1])
        self.screen.blit(self.homeIconImg, (X_PADDING, (BAR_HEIGHT - self.rectHome.height)/2))

        # Speaker Icon 
        self.rectSpeaker = pygame.Rect(GAME_SIZE[0]-2*X_PADDING,(BAR_HEIGHT - self.homeIconImg.get_height())/2, BUTTON_SIZE[0], BUTTON_SIZE[1])
        self.screen.blit(self.speakerIconImg, (GAME_SIZE[0]-2*X_PADDING, (BAR_HEIGHT - self.rectSpeaker.height)/2))

        # Mask Icon  
        rectMask = self.maskIconImg.get_rect()
        self.screen.blit(self.maskIconImg, (X_PADDING, BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectMask.height)/2))
        
        # Mask Text 
        numMaskText = pygame.font.SysFont('None', FONT_SIZE_MASK)
        textImgMask = numMaskText.render(f": {numMasks}", False, (0,0,0))
        rectNum = textImgMask.get_rect()
        pygame.draw.rect(textImgMask, (255,255,255, 128), rectNum, 1)
        self.screen.blit(textImgMask, (1.5 * X_PADDING + rectMask.width, BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectMask.height)/2))

        # Scull Icon
        rectScull = self.scullIconImg.get_rect()
        self.screen.blit(self.scullIconImg, (GAME_SIZE[0]-4*X_PADDING, BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectScull.height)/2))

        # Death Text
        numDeathText = pygame.font.SysFont('None', FONT_SIZE_MASK)
        textImgDeath = numDeathText.render(f": {numMasks}", False, (0,0,0))
        rectNumDeath = textImgDeath.get_rect()
        pygame.draw.rect(textImgDeath, (255,255,255, 128), rectNum, 1)
        self.screen.blit(textImgDeath, (GAME_SIZE[0]-2*X_PADDING, BAR_HEIGHT + GAME_SIZE[1] + (BAR_HEIGHT - rectNumDeath.height)/2)) 
