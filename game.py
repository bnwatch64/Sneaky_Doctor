import logging
import pygame
from gameLoader import GameLoader
from player import Player
from enemy import Enemy
from loadsources import load_image

from gameConstants import *


class Game:
    def __init__(self, gameLoader, gameStats, pressedKeys=[]):
        # Init attributes
        self.screen = pygame.Surface(GAME_SIZE)
        self.pressedKeys = pressedKeys
        self.allsprites = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.Group()
        self.masks = pygame.sprite.Group()
        self.gameStats = gameStats.copy()
        self.gameLoader = gameLoader
        # Load level
        (
            walls,
            self.realWallRects,
            masks,
            realPlayerStartPosition,
            self.realExitRect,
        ) = self.gameLoader.load_level(gameStats["currentLvl"])
        self.masks.add(masks)
        self.allsprites.add(masks)
        self.allsprites.add(walls)
        # Load all NPCs
        npcPaths, realNpcStartPositions = self.gameLoader.load_npc_paths(
            gameStats["currentLvl"]
        )
        for i in range(0, len(npcPaths)):
            newEnemy = Enemy(realNpcStartPositions[i], npcPaths[i])
            self.npcs.add(newEnemy)
            self.allsprites.add(newEnemy)
        # Create Player
        self.player = Player(realPlayerStartPosition)
        self.allsprites.add(self.player)
        self.playerDying = False
        # Create floor (background)
        self.floor = pygame.Surface(GAME_SIZE)
        self.floor.fill(FLOOR_COLOR)
        self.screen.blit(self.floor, (0, 0))

    def _handleMaskCollisions(self):
        # Get all masks that collide with player
        collidedMasks = pygame.sprite.spritecollide(
            self.player, self.masks, True, collided=self._real_did_collide
        )
        for collidedMask in collidedMasks:
            # Remove mask from allsprites group
            self.allsprites.remove(collidedMask)
            # Increment mask count
            self.gameStats["maskCount"] = self.gameStats["maskCount"] + 1

    def _real_did_collide(self, sprite1, sprite2):
        # Tests whether two sprites with realRects collide in real space
        if sprite1.realRect.colliderect(sprite2.realRect):
            return True
        else:
            return False

    def checkWin(self):
        # Check if player reached exit
        if self.realExitRect.contains(self.player.realRect):
            return True
        else:
            return False

    def checkDeath(self):
        # Check if player completed dying
        if self.playerDying and self.player.dyingCounter == 0:
            return True
        # Check if player touched an enemy
        collidedEnemies = pygame.sprite.spritecollide(
            self.player, self.npcs, False, collided=self._real_did_collide
        )
        if not len(collidedEnemies) == 0 and not self.playerDying:
            if self.player.deathProtectCounter > 0:
                # Ignore collision if player is protected
                return False
            elif self.gameStats["maskCount"] > 0:
                # If player has at least one mask, remove one mask and protect him
                self.gameStats["maskCount"] = self.gameStats["maskCount"] - 1
                self.player.deathProtect()
                return False
            else:
                # Else kill the player
                self.player.die()
                self.playerDying = True
                return False
        else:
            return False

    def update_game(self):
        # Update movement based on pressed keys
        self.player.move(self.pressedKeys)

        # Clear the game Surface
        self.allsprites.clear(self.screen, self.floor)
        # Call update() methods on all sprites
        self.allsprites.update(self.realWallRects)
        # Check if any collectibles were collected
        self._handleMaskCollisions()
        # Update the layers of all movable game objects
        self.allsprites.change_layer(self.player, self.player.get_layer())
        for npc in self.npcs:
            self.allsprites.change_layer(npc, npc.get_layer())
        # Draw the new game Surface
        dirtyAreas = self.allsprites.draw(self.screen)

        # Return dirty areas
        return dirtyAreas
