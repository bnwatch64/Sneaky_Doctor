"""game
    * Contains game functionalities

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""
import logging
import pygame
from gameLoader import GameLoader
from player import Player
from enemy import Enemy
from loadsources import load_collect_sound
from gameConstants import *


class Game:
    """Game class
    * Loads, blits and updates all game objects (Player, Enemies, Walls, Masks, etc.) of one level
    * Handles win, player collision with mask, death

    Public Methods:
    * def checkWin(self)
    * def checkDeath(self)
    * def update_game(self)
    """

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
        """handle mask collisions (private)
        * after collision mask is removed
        * mask counter increased by one after player - mask collsion

        Args:
            None

        Return:
            None

        Test:
            * Collision with mask removes mask on map
            * Collision with mask increases mask counter in bottom bar by one
        """
        soundCollect = load_collect_sound("Collect_Coin.wav")
        # Get all masks that collide with player
        collidedMasks = pygame.sprite.spritecollide(
            self.player, self.masks, True, collided=self._real_did_collide
        )
        for collidedMask in collidedMasks:
            # Remove mask from allsprites group
            self.allsprites.remove(collidedMask)
            # Coin sound after collecting mask
            soundCollect.play()
            # Increment mask count
            self.gameStats["maskCount"] = self.gameStats["maskCount"] + 1

    def _real_did_collide(self, sprite1, sprite2):
        """real did collide (private)
        * Replaces the normal sprite collision detection
        * Determines collision between two Sprites by their real rects (from virtual top down view)
        * Can be used by pygame.sprite.spritecollide method for real collision detection in 2.5D space

        Args:
            sprite1 (pygame.sprite.Sprite): One Sprite
            sprite2 (pygame.sprite.Sprite): The other Sprite

        Return:
            (bool): True if there is a collision, False if not

        Test:
            * Collision of real rects returns True
            * No Collision returns False
        """

        if sprite1.realRect.colliderect(sprite2.realRect):
            return True
        else:
            return False

    def checkWin(self):
        """check win
        * Check if player reached exit

        Args:
            None

        Return:
            (bool): True if player arrives destination, false if not

        Test:
            * Player walks into door function returns True
            * Player does not walk into door function returns False
        """

        if self.realExitRect.contains(self.player.realRect):
            return True
        else:
            return False

    def checkDeath(self):
        """check death
        * Check if player collided with an Enemy
        * Checks if player should die
        * Removes a mask if player had one and protects him
        * Initiates dying animation if player died
        * Checks if dying animation is finished if player is already dying

        Args:
            None

        Return:
            (bool): True if player finished dying, false if player survives or is still dying

        Test:
            * Colliding with enemy, player dying is initiated and function returns False
            * Colldiing with enemy(with mask), player survives and gets protected
        """

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
        """update game
        * Calls the players move method to update his speed
        * Calls update functions on all sprites
        * Handles mask collisions
        * Updates the layer of all movable game objects to keep right perspective
        * Draws changes to game Surface

        Args:
            None

        Returns:
            dirtyAreas(list): List with all updated areas in game for better performance when updating screen

        Test:
            * Collect mask and mask counter has to be changed
            * Move some game objects and check if perspective is right (because of the layers)
        """
        logging.info("Updating changed areas of game...")
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

        logging.info("Update changed areas of game successful")

        # Return dirty areas
        return dirtyAreas
