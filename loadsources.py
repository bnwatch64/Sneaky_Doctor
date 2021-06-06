"""loadsources
    * Contains all load functions needed in project

    Attributes:
        authors: Benjamin Ader & Sujan Kanapathipillai
        date: 06.06.2021
        version: 0.0.1
"""
import logging
import os
import json
import pygame
import random
import time
from gameConstants import *


def load_animation(folder, scale=None, colorkey=None):
    """load animation
        * images of an animation are loaded 

        Args:
            folder (string): Name of folder which contains images
            scale (tuple, optional): The size of the animation. Defaults to None.
            colorkey (tuple, optional): The color as rgb value. Defaults to None.

        Raises:
            SystemExit: [description]

        Return:
            images (list): List of pygame.Surfaces is returned
        
        Test: 
            * Checking number of images within folder and number of elements within returned list 
            * Wrong folder name should result in exception
    """
    logging.info("Loading animation...")
    directory = os.path.join(ASSETS_LOCATION, folder)

    images = []
    # Get every animation frame of list
    filesList = os.listdir(directory)
    # Sort by name
    filesList.sort()
    # Load all animtion frames and add them to array
    for file in filesList:
        filename = os.fsdecode(file)
        if not filename.endswith(".png"):
            continue
        fullname = os.path.join(directory, filename)

        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            logging.error("Cannot load image: " + filename)
            raise SystemExit(message)
        if scale is not None:
            image = pygame.transform.scale(image, scale)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        image = image.convert_alpha()

        images.append(image)
    logging.info("Loading animation was successful")
    
    return images


def load_enemy_animations(scale=None, colorkey=None):
    """load enemy animations
        * images of enemy animation is loaded 

        Args:
            scale (tuple, optional): The size of the animation. Defaults to None.
            colorkey (tuple, optional): The color as rgb value. Defaults to None.

        Raises:
            SystemExit: [description]

        Return:
            animsDict (dictionary): Dictionary of pygame.Surfaces
        
        Test: 
            * Checking number of images within folder and number of elements within returned dictionary 
            * Wrong folder name should result in exception
    """
    logging.info("Loading enemy animation...")
    # Get random enemy assets
    randEnemyNum = random.randint(1, ENEMY_SAMPLES_COUNT)
    randEnemyFolder = "npc" + str(randEnemyNum) + "_anim"
    baseDirectory = os.path.join(ASSETS_LOCATION, randEnemyFolder)

    # Get all images for animation from all 4 angles
    animsDict = {"front": [], "right": [], "left": [], "back": []}
    for side in animsDict:
        sideDirectory = os.path.join(baseDirectory, side)

        # Get every animation frame of list
        filesList = os.listdir(sideDirectory)
        # Sort by name
        filesList.sort()
        # Load all animtion frames and add them to array
        for file in filesList:
            filename = os.fsdecode(file)
            if not filename.endswith(".png"):
                continue
            fullname = os.path.join(sideDirectory, filename)

            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                logging.error("Cannot load image: " + filename)
                raise SystemExit(message)
            if scale is not None:
                image = pygame.transform.scale(image, scale)
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            image = image.convert_alpha()

            animsDict[side].append(image)
    logging.info("Loading enemy animation was successful")

    return animsDict


def load_image(name, scale=None, colorkey=None):
    """load image 
        * image is loaded 

        Args:
            name (string): File name argument as string
            scale (tuple, optional): The size of the animation. Defaults to None.
            colorkey (tuple, optional): The color as rgb value. Defaults to None.

        Raises:
            SystemExit: [description]

        Returns:
            image (pygame.Surface): Loaded image is returned as pygame.Surface
            image.get_rect() (pygame.Rect): Loaded image is returned as pygame.Rect

        Test: 
            * Returned image has the scale size that is passed in the function call
            * Wrong file name results in exception
    """
    logging.info("Loading image...")
    fullname = os.path.join(ASSETS_LOCATION, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        logging.error("Cannot load image: " + name)
        raise SystemExit(message)
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    image = image.convert_alpha()
    logging.info("Loading image was successful")
    return image, image.get_rect()


def load_sound(filename):
    """load sound 

    Args:
        filename (string): Filename of the sound that is loaded

    Raises:
        SystemExit: [description]
    
    Return:
        None

    Test:
        * Check whether loaded sound can be played
        * Wrong filename results in exeption
    """
    logging.info("Loading sound")
    fullname = os.path.join(ASSETS_LOCATION, filename)
    try:
        sound = pygame.mixer.music.load(fullname)
    except pygame.error as message:
        logging.error("Cannot load sound: " + filename)
        raise SystemExit(message)
    logging.info("Loading sound was successful")


def load_collect_sound(filename):
    """load collect sound

        Args:
            filename (string): Filename of the sound that is loaded

        Return:
            sound (Sound): Sound object is returned
        
        Test:
            * Check whether loaded sound can be played
            * Wrong filename results in exeption
    """
    logging.info("Loading collect sound...")
    fullname = os.path.join(ASSETS_LOCATION, filename)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        logging.error("Cannot load sound: " + filename)
    logging.info("Loading collect sound was successful")
    return sound


def load_game_save():
    """load game save 
        * save.json with the game stats is loaded 

        Args:
            None

        Return:
            [type]: [description]
        
        Test:
            * Load existing save.json file 
            * By pressing continue in main menu, the saved game stats appear in top and bottom bars
            * save.json does not exist, function results in exception TODO
    """
    logging.info("Loading saved game...")
    saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
    with open(saveFilePath, "r") as saveFile:
        jsonString = saveFile.read()
    logging.info("Loading saved game was successful")
    return json.loads(jsonString)


def save_game(gameStats):
    """save game 
        * game stats are written to save.json


        Args:
            gameStats (dict): Dictionary contains current level, number of collected masks and number of deaths 
        
        Return: 
            None

        Test:
            * Start new game, play one level, collect masks and die after pressing esc this data can be found in save.json
            * 
    """
    logging.info("Saving game stats...")
    saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
    with open(saveFilePath, "w") as saveFile:
        jsonString = json.dumps(gameStats)
        saveFile.write(jsonString)
    logging.info("Saving game stats was successful")


def check_save_file_exists():
    """check save file exists
        * Checking if there is the save.json file in the current directory

        Args:
            None

        Returns:
            (bool): If file exists True is returned, otherwise False

        Test:
            * Create save.json, call function it should return True
            * Delete save.json file within this directory and call function, False should be returned 
    """
    saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
    return os.path.exists(saveFilePath)


def delete_game_save():
    """delete game save
        * save.json is deleted 

        Args:
            None

        Return:
            None
        
        Test:
            * Create save.json file, by calling this function save.json should be removed from directory
            * 
    """
    saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
    os.remove(saveFilePath)
    # Wait for file deletion
    # TODO levelPath ? 
    while os.path.exists(levelPath):
        time.sleep(0.0001)


def check_level_exists(levelNum):
    """check level exists 
        * check if certain folder with level_x (x -> 1,...,10) exists

        Args:
            levelNum (int): levelNum contains the number of the level

        Returns:
            (bool): If level exists True is returned, otherwise False
        
        Test:
            * Call function with existing level folder, True should be returned
            * Call function with not existing level folder, False should be returned
    """
    levelPath = os.path.join(ASSETS_LOCATION, LEVEL_LOCATION, "level_" + str(levelNum))
    return os.path.exists(levelPath)
