import logging
import os
import json
import pygame
import random
from gameConstants import *




def load_animation(folder, scale=None, colorkey=None):
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

    return images


def load_enemy_animations(scale=None, colorkey=None):
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

    return animsDict


def load_image(name, scale=None, colorkey=None):
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
    return image, image.get_rect()


def load_sound(filename):
    fullname = os.path.join(ASSETS_LOCATION, filename)
    try:
        sound = pygame.mixer.music.load(fullname)
    except pygame.error as message:
        logging.error("Cannot load sound: " + filename)
        raise SystemExit(message)


def load_game_save():
    saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
    with open(saveFilePath, "r") as saveFile:
        jsonString = saveFile.read()
    return json.loads(jsonString)


def save_game(gameStats):
    saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
    with open(saveFilePath, "w") as saveFile:
        jsonString = json.dumps(gameStats)
        saveFile.write(jsonString)

def check_save_file_exists():
        saveFilePath = os.path.join(ASSETS_LOCATION, SAVEFILE_NAME)
        return os.path.exists(saveFilePath)
