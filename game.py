import logging
import pygame
from gameLoader import *
from player import Player
from enemy import Enemy
from loadsources import load_image

from gameConstants import *


class Game:
    def __init__(self, gameStats, pressedKeys=[]):
        # Init attributes
        self.screen = pygame.Surface(GAME_SIZE)
        self.pressedKeys = pressedKeys
        self.allsprites = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.Group()
        self.gameStats = gameStats.copy()
        # Load level
        (
            walls,
            self.realWallRects,
            realPlayerStartPosition,
            self.realExitRect,
        ) = load_level(gameStats["currentLvl"])
        self.allsprites.add(walls)
        # Load all NPCs
        npcPaths, realNpcStartPositions = load_npc_paths(gameStats["currentLvl"])
        for i in range(0, len(npcPaths)):
            newEnemy = Enemy(realNpcStartPositions[i], npcPaths[i])
            self.npcs.add(newEnemy)
            self.allsprites.add(newEnemy)
        # Create Player
        self.player = Player(realPlayerStartPosition)
        self.allsprites.add(self.player)
        # Create floor (background)
        self.floor = pygame.Surface(GAME_SIZE)
        self.floor.fill(FLOOR_COLOR)
        self.screen.blit(self.floor, (0, 0))

    def checkWin(self):
        # Check if player reached exit
        if self.realExitRect.contains(self.player.realRect):
            return True
        else:
            return False

    def update_game(self):
        # Update movement based on pressed keys
        self.player.move(self.pressedKeys)

        # Clear the game Surface
        self.allsprites.clear(self.screen, self.floor)
        # Call update() methods on all sprites
        self.allsprites.update(self.realWallRects)
        # Update the layers of all movable game objects
        self.allsprites.change_layer(self.player, self.player.get_layer())
        for npc in self.npcs:
            self.allsprites.change_layer(npc, npc.get_layer())
        # Draw the new game Surface
        dirtyAreas = self.allsprites.draw(self.screen)

        # Return dirty areas
        return dirtyAreas
