import logging
import pygame
from PIL import Image
import os
from loadsources import load_image
from gameObject import GameObject
from gameConstants import *


def load_level(levelNum):
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

    # TODO: Make class with asset attributes
    wallAsset, _ = load_image("game_objects/wall.png", scale=(BLOCK_SIZE, WALL_HEIGHT))
    exitAsset, _ = load_image("game_objects/door.png", scale=(BLOCK_SIZE, WALL_HEIGHT))

    # Get RGBA data as list of pixel values
    levelData = levelMap.getdata()

    # Create empty sprite and realRect list
    wallSprites = []
    realWallRects = []
    realStartPos = None

    # Loop over every pixel
    for i, pix in enumerate(levelData):
        # If map pixel is black, draw wall
        if pix == (0, 0, 0, 255):
            x = i % 32
            y = int(i / 32)
            realWallPosition = (x * BLOCK_SIZE, y * BLOCK_SIZE)
            newWall = GameObject(wallAsset, realWallPosition)
            wallSprites.append(newWall)
            realWallRects.append(newWall.realRect)
        # If map pixel is green, draw exit
        if pix == (0, 255, 0, 255):
            x = i % 32
            y = int(i / 32)
            realExitPosition = (x * BLOCK_SIZE, y * BLOCK_SIZE)
            exit = GameObject(exitAsset, realExitPosition)
            wallSprites.append(exit)
        # If map pixel is blue, set player start position
        elif pix == (0, 0, 255, 255):
            x = i % 32
            y = int(i / 32)
            realStartPos = [c * BLOCK_SIZE for c in [x, y]]

    # Check if start pixel was found, abort if not
    if realStartPos == None:
        logging.error(
            "Level " + str(levelNum) + " has no starting (blue) pixel for player"
        )
        raise SystemExit("Map Parse Error")

    # Close level map image
    levelMap.close()

    logging.info("Loading level " + str(levelNum) + " from image file was successful")

    return wallSprites, realWallRects, realStartPos


def load_npc_paths(levelNum):
    logging.info(
        "Loading NPC paths for level " + str(levelNum) + " from image files..."
    )

    # Get path to level directory
    levelPath = os.path.join(ASSETS_LOCATION, LEVEL_LOCATION, "level_" + str(levelNum))

    npcPaths = []
    npcStartPoss = []
    # Get list of all files in level directory
    filesList = os.listdir(levelPath)
    # Sort by name
    filesList.sort()
    # Load all npc path images, parse the paths and add them to array
    for file in filesList:
        filename = os.fsdecode(file)
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
        trace_and_append_pixels(pathData, pixPath, startPixPos)

        # Translalte pixle path and start pos to real npc path according to BLOCK_SIZE
        npcPath = pix_to_real_path(pixPath)
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


def trace_and_append_pixels(
    pathData, listToAppend, pixPos, ignorePixels=[], appendBackwards=True
):
    # Traces a path of pixels from prePixelPos and appends them to listToAppend

    # Check every neighboring pixel if it's part of the path
    neighborsPos = []
    for x in range(pixPos[0] - 1, pixPos[0] + 2):
        for y in range(pixPos[1] - 1, pixPos[1] + 2):
            if (
                not (x, y) == pixPos
                and not (x, y) in ignorePixels
                and pathData.getpixel((x, y)) == (0, 0, 0, 255)
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
        trace_and_append_pixels(
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
            trace_and_append_pixels(
                pathData,
                listToAppend,
                neighborsPos[0],
                ignorePixels=ignorePixels + [pixPos],
                appendBackwards=True,
            )
            listToAppend.append(pixPos)
            trace_and_append_pixels(
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
            trace_and_append_pixels(
                pathData,
                path0,
                neighborsPos[0],
                ignorePixels=ignorePixels + [pixPos],
                appendBackwards=appendBackwards,
            )
            trace_and_append_pixels(
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


def pix_to_real_path(pixPath):
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
