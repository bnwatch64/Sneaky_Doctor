"""gameLoader
    * .png files loaded which contain enemy path, map design
    * functionalities added to loaded .png files

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""
import logging
import pygame
from PIL import Image
import os
from loadsources import load_image, load_animation
from gameObject import GameObject, AnimatedGameObject
from gameConstants import *


class GameLoader:
    """GameLoader class
        * Map of level and enemy paths is constructed

        Public Methods:
        * def load_level(self, levelNum))
        * def load_npc_paths(self)
    """

    def __init__(self):
        # Load all gameObject assets once for better performance
        self.wallAsset, _ = load_image(
            "game_objects/wall.png", scale=(BLOCK_SIZE, WALL_HEIGHT)
        )
        self.exitTopAsset, _ = load_image(
            "game_objects/door_top.png", scale=(BLOCK_SIZE, WALL_HEIGHT)
        )
        self.exitBottomAsset, _ = load_image(
            "game_objects/door_bottom.png", scale=(BLOCK_SIZE, WALL_HEIGHT)
        )
        self.maskAnim = load_animation(
            "game_objects/mask_anim", scale=(BLOCK_SIZE, WALL_HEIGHT)
        )


    def load_level(self, levelNum):
        """load level
            * .png level file is loaded with the map
            * From the pixels of the .png the building blocks for the map are constructed

        Args:
            levelNum (int): Number of the level that needs to be loaded 

        Raises:
            SystemExit: [description]
            SystemExit: [description]
            SystemExit: [description]

        Returns:
           wallSprites (list): Each black pixel of the .png is part of the wall and is added to sprites, all sprites in wallSprites list
           realWallRects (list): List of all wall rectangles
           maskSprites (list): List of all mask sprites
           realStartPos (tuple): Real start position is calculated
           realExitRect (pygame.Rect): Exit rectangle with real sizes
        
        Test:
            * Create .png with black lines, wallsprites list and realWallRects list should be filled according to the .png file
            * Create .png file without blue pixel this results in exception
        """
        logging.info("Loading level " + str(levelNum) + " from image file...")

        # Get path to level map file
        levelPath = os.path.join(
            ASSETS_LOCATION,
            LEVEL_LOCATION,
            "level_" + str(levelNum),
            "map" + str(levelNum) + ".png",
        )
        # Open level map image
        levelMap = Image.open(levelPath)
        # Interpret as RGBA image
        levelMap = levelMap.convert("RGBA")

        # Check if size fits requirements (32x31)
        if not levelMap.size == (32, 31):
            logging.error(
                "Level "
                + str(levelNum)
                + " could not be loaded, as the map image file is of unexpected dimensions"
            )
            raise SystemExit("Map Load Error")

        # Get RGBA data as list of pixel values
        levelData = levelMap.getdata()

        # Create empty sprite and realRect list
        wallSprites = []
        realWallRects = []
        maskSprites = []
        realStartPos = None
        realExitRect = None

        # Loop over every pixel
        for i, pix in enumerate(levelData):
            # If map pixel is black, draw wall
            if pix == (0, 0, 0, 255):
                x = i % 32
                y = int(i / 32)
                realWallPosition = (x * BLOCK_SIZE, y * BLOCK_SIZE)
                newWall = GameObject(self.wallAsset, realWallPosition)
                wallSprites.append(newWall)
                realWallRects.append(newWall.realRect)
            # If map pixel is green, draw exit
            if pix == (0, 255, 0, 255):
                x = i % 32
                y = int(i / 32)
                realExitPos = (x * BLOCK_SIZE, y * BLOCK_SIZE)
                exitBottom = GameObject(self.exitBottomAsset, realExitPos)
                exitTop = GameObject(self.exitTopAsset, realExitPos)
                # Display top of exit one layer higher for right perspective
                exitTop.moveLayer(1)
                wallSprites.append([exitBottom, exitTop])
                realExitRect = pygame.Rect(realExitPos, (BLOCK_SIZE, BLOCK_SIZE))
            # If map pixel is red, draw mask
            elif pix == (255, 0, 0, 255):
                x = i % 32
                y = int(i / 32)
                realMaskPos = (x * BLOCK_SIZE, y * BLOCK_SIZE)
                newMask = AnimatedGameObject(self.maskAnim, realMaskPos)
                maskSprites.append(newMask)
            # If map pixel is blue, set player start position
            elif pix == (0, 0, 255, 255):
                x = i % 32
                y = int(i / 32)
                realStartPos = [c * BLOCK_SIZE for c in [x, y]]

        # Check if start (blue) pixel was found, abort if not
        if realStartPos == None:
            logging.error(
                "Level "
                + str(levelNum)
                + " map has no starting (blue) pixel for player"
            )
            raise SystemExit("Map Parse Error")
        # Check if exit (green) pixel was found, abort if not
        if realStartPos == None:
            logging.error("Level " + str(levelNum) + " map has no exit (green) pixel")
            raise SystemExit("Map Parse Error")

        # Close level map image
        levelMap.close()

        logging.info(
            "Loading level " + str(levelNum) + " from image file was successful"
        )

        return (
            wallSprites,
            realWallRects,
            maskSprites,
            realStartPos,
            realExitRect,
        )

    def load_npc_paths(self, levelNum):
        """load npc paths 
            * Enemy paths are determined by .png file with black lines 

            Args:
                levelNum (int): Number of the level that needs to be loaded

            Raises:
                SystemExit: [description]
                SystemExit: [description]

            Returns:
               npcPaths (list): List of all path blocks
               npcStartPoss (list): Enemy starting point
            
            Test:
                * Create .png file with enemy path, path should be saved in npcPaths
                * On enemy path mark one block with green color, npcStartPoss should contain the position of the colored block
        """
        logging.info(
            "Loading NPC paths for level " + str(levelNum) + " from image files..."
        )

        # Get path to level directory
        levelPath = os.path.join(
            ASSETS_LOCATION, LEVEL_LOCATION, "level_" + str(levelNum)
        )

        npcPaths = []
        npcStartPoss = []
        # Get list of all files in level directory
        filesList = os.listdir(levelPath)
        # Sort by name
        filesList.sort()
        # Load all npc path images, parse the paths and add them to array
        for file in filesList:
            filename = os.fsdecode(file)

            logging.debug("Loading " + filename)

            if not filename.startswith("npc"):
                continue
            fullname = os.path.join(levelPath, filename)

            # Open npc path image
            npcPathImg = Image.open(fullname)
            # Interpret as RGBA image
            npcPathImg = npcPathImg.convert("RGBA")

            # Check if size fits requirements (32x31)
            if not npcPathImg.size == (32, 31):
                logging.error(
                    "NPC path "
                    + str(filename)
                    + " could not be loaded, as the NPC path file is of unexpected dimensions"
                )
                raise SystemExit("NPC Path Load Error")

            # Get RGBA data as list of pixel values
            pathData = npcPathImg.getdata()

            # Search for start pixel (green)
            startPixPos = None
            for i, pix in enumerate(pathData):
                # If start (green) pixel is found, safe it and break
                if pix == (0, 255, 0, 255):
                    x = i % 32
                    y = int(i / 32)
                    startPixPos = (x, y)
                    break

            # Check if start pixel was found, abort if not
            if startPixPos == None:
                logging.error(
                    "NPC path " + str(filename) + " has no starting (green) pixel"
                )
                raise SystemExit("NPC Path Load Error")

            # Trace the pixel path, starting from startPixPos
            pixPath = []
            self._trace_and_append_pixels(pathData, pixPath, startPixPos)

            # Translalte pixle path and start pos to real npc path according to BLOCK_SIZE
            npcPath = self._pix_to_real_path(pixPath)
            npcStartPos = (
                startPixPos[0] * BLOCK_SIZE,
                startPixPos[1] * BLOCK_SIZE,
            )

            # Append all npc data
            npcPaths.append(npcPath)
            npcStartPoss.append(npcStartPos)

            npcPathImg.close()

        logging.info(
            "Loading NPC paths for level "
            + str(levelNum)
            + " from image files was successful"
        )

        return npcPaths, npcStartPoss

    def _trace_and_append_pixels(
        self, pathData, listToAppend, pixPos, ignorePixels=[], appendBackwards=True
    ):
        """trace and append pixels
            * Traces a path of pixels and appends them to listToAppend

            Args:
                pathData (ImagineCore): [description]
                listToAppend (list): listToAppend contains the whole enemy path as list of tuples
                pixPos (tuple): [description]
                ignorePixels (list, optional): [description]. Defaults to [].
                appendBackwards (bool, optional): [description]. Defaults to True.

            Raises:
                SystemExit: [description]

            Return:
                None

            Test:
                *  
                * 
        """

        # Check every neighboring pixel if it's part of the path
        neighborsPos = []
        for x in range(pixPos[0] - 1, pixPos[0] + 2):
            if x > 31:
                continue
            for y in range(pixPos[1] - 1, pixPos[1] + 2):
                if y > 30:
                    continue
                if (
                    not (x, y) == pixPos
                    and not (x, y) in ignorePixels
                    and pathData.getpixel((x, y)) in [(0, 0, 0, 255), (0, 0, 255, 255)]
                ):
                    neighborsPos.append((x, y))

        # Check if end of path is reached
        if len(neighborsPos) == 0:
            listToAppend.append(pixPos)
            return

        # Trace further path, append to listToAppend
        elif len(neighborsPos) == 1:
            if not appendBackwards:
                listToAppend.append(pixPos)
            self._trace_and_append_pixels(
                pathData,
                listToAppend,
                neighborsPos[0],
                ignorePixels=ignorePixels + [pixPos],
                appendBackwards=appendBackwards,
            )
            if appendBackwards:
                listToAppend.append(pixPos)

        # If there's more than one neighbor...
        elif len(neighborsPos) == 2:
            # ...because we are the start pixel, trace both paths
            if len(ignorePixels) == 0:
                self._trace_and_append_pixels(
                    pathData,
                    listToAppend,
                    neighborsPos[0],
                    ignorePixels=ignorePixels + [pixPos],
                    appendBackwards=True,
                )
                listToAppend.append(pixPos)
                self._trace_and_append_pixels(
                    pathData,
                    listToAppend,
                    neighborsPos[1],
                    ignorePixels=ignorePixels + [pixPos],
                    appendBackwards=False,
                )
            # ...because there is a corner, trace both paths and choose longer one
            else:
                if not appendBackwards:
                    listToAppend.append(pixPos)

                # Set up counters for length determination
                path0 = []
                path1 = []
                self._trace_and_append_pixels(
                    pathData,
                    path0,
                    neighborsPos[0],
                    ignorePixels=ignorePixels + [pixPos],
                    appendBackwards=appendBackwards,
                )
                self._trace_and_append_pixels(
                    pathData,
                    path1,
                    neighborsPos[1],
                    ignorePixels=ignorePixels + [pixPos],
                    appendBackwards=appendBackwards,
                )

                # Choose longer path
                if len(path0) >= len(path1):
                    listToAppend.extend(path0)
                else:
                    listToAppend.extend(path1)

                if appendBackwards:
                    listToAppend.append(pixPos)

        # If there's more than 2 neighbors, error!
        else:
            logging.error(
                "Pixel with position "
                + str(pixPos)
                + " has more than two neighbors, can't parse path"
            )
            raise SystemExit("NPC Path Parse Error")

    def _pix_to_real_path(self, pixPath):
        """pix to real path
            * 

            Args:
                pixPath ([type]): [description]

            Return:
                realPath (type): [description]

            Test:
                *
                *
        """
        # Creates a list of real positions from a list of pixel positions

        realPath = []
        for i in range(0, len(pixPath) - 1):
            xPix = pixPath[i][0]
            yPix = pixPath[i][1]
            xRealStart = BLOCK_SIZE * xPix
            yRealStart = BLOCK_SIZE * yPix
            xDiff = pixPath[i + 1][0] - xPix
            yDiff = pixPath[i + 1][1] - yPix
            # Calculate all in-between values for real path
            newRealPath = [
                (xRealStart + n * xDiff, yRealStart + n * yDiff)
                for n in range(0, BLOCK_SIZE)
            ]
            realPath.extend(newRealPath)

        lastXPix = pixPath[len(pixPath) - 1][0]
        lastYPix = pixPath[len(pixPath) - 1][1]
        lastXRealStart = BLOCK_SIZE * lastXPix
        lastYRealStart = BLOCK_SIZE * lastYPix
        lastRealPos = (lastXRealStart, lastYRealStart)
        realPath.append(lastRealPos)

        return realPath
