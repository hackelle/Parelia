import pygame
import colors as c
import os.path
import items
import math
import random

images = []


def prepare_hammer_images():
    path = "../res/pics/hammer"
    if os.path.isdir(path):
        print("loading " + path)
        files = sorted(os.listdir(path))
        for file in files:
            file_path = path + '/' + file
            if os.path.isfile(file_path):
                images.append(pygame.image.load(file_path).convert_alpha())
                print("loading file " + file_path)


class Hammer(items.Item):

    damage = 100

    def __init__(self):
        global images
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the character, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([5, 20])
        self.image.fill(c.WHITE)
        self.image.set_colorkey(c.WHITE)

        # Draw the character (a rectangle!) on the surface
        pygame.draw.rect(self.image, c.BLACK, [0, 0, 5, 20])

        # Instead we could load a proper picture of a character
        # load images static
        self.images = images
        if len(self.images) > 0:
            self.image = self.images[0]
            self.image_index = 0

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


    def damage_sprite(self, other):
        # damage the other sprite
        other.damage(self.damage)

    def use(self):
        # not usable
        pass
