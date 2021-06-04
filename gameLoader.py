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

    # Get RGBA data as list of pixel values
    levelData = levelMap.getdata()

    # Create empty sprite group and filll with floor color
    allWalls = []
    wallRects = []

    for i, pixel in enumerate(levelData):
        # If map pixel is black, draw wall
        if pixel == (0, 0, 0, 255):
            col = i % 32
            row = int(i / 32)
            realWallPosition = (col * BLOCK_SIZE, row * BLOCK_SIZE)
            newWall = GameObject(wallAsset, realWallPosition, row)
            allWalls.append(newWall)
            wallRects.append(newWall.realRect)

    return allWalls, wallRects
