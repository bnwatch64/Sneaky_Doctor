import os
import pygame
import random
from gameConstants import *


def load_animation(folder, scale=None, colorkey=None):
    directory = os.path.join(ASSETS_LOCATION, folder)

    images = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if not filename.endswith(".png"):
            continue
        fullname = os.path.join(directory, filename)

        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print("Cannot load image:", name)
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
    randEnemyNum = random.randint(0, ENEMY_SAMPLES_COUNT)
    randEnemyFolder = "npc" + str(randEnemyNum) + "_anim"
    baseDirectory = os.path.join(ASSETS_LOCATION, randEnemyFolder)

    # Get all images for animation from all 4 angles
    animsDict = {"front": [], "right": [], "left": [], "back": []}
    for side in animsDict:
        sideDirectory = os.path.join(baseDirectory, side)
        for file in os.listdir(sideDirectory):
            filename = os.fsdecode(file)
            if not filename.endswith(".png"):
                continue
            fullname = os.path.join(sideDirectory, filename)

            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print("Cannot load image:", name)
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


# functions to create our resources
def load_image(name, scale=None, colorkey=None):
    fullname = os.path.join(ASSETS_LOCATION, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    image = image.convert_alpha()
    return image, image.get_rect()
