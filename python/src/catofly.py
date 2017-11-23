import pygame
import colors as c
import os.path
import character
import math
import random

images = []


def prepare_catofly_pictures():
    """Prepares images for use in Catofly class.
    Static picture loading."""
    path = "../res/pics/catofly"
    if os.path.isdir(path):
        print("loading " + path)
        files = sorted(os.listdir(path))
        for file in files:
            file_path = path + '/' + file
            if os.path.isfile(file_path):
                # scale down to 40, 40
                image = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(), (40, 40))
                images.append(image)
                print("loading file " + file_path)


class Catofly(character.Character):
    """This class represents a character. It derives from the "Sprite" class in Pygame."""

    # fixed attributes
    jump_height = 0  # How high can the character jump in a single jump?
    max_possible_jumps = 0  # Number of possible jumps. 1 for single jump, 2 for double ...
    max_health = 0  # maximum health
    armor = 0  # factor for protection (1x damage @ 100)
    strength = 0  # factor for damage dealing
    critical_chance = 0  # possibility for critical hits
    walk_speed = 0  # the speed, the character can walk each update
    images = []  # array of animation images
    image = None  # visual representation, should be drawable
    image_index = 0  # index of current image
    rect = None  # rectangle surrounding the character

    # changed by functions
    remaining_jumps = 0  # Number of jumps currently remaining
    vertical_velocity = 0  # the current jumping/falling speed
    health = 0  # current health
    level = 1  # characters level, should be used for some calculations

    # variables for the next update
    center = [0, 0]  # center of circle
    radius = 10  # radius of circle
    current_angle = 0  # current fly around

    def __init__(self):
        global images
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the character, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([40, 50])
        self.image.fill(c.WHITE)
        self.image.set_colorkey(c.WHITE)

        # Draw the character (a rectangle!) on the surface
        pygame.draw.rect(self.image, c.BLACK, [0, 0, 40, 50])

        # Instead we could load a proper picture of a character
        # load images static
        self.images = images
        if len(self.images) > 0:
            self.image = self.images[0]
            self.image_index = 0

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move(self, direction, pixels, screen_size):
        return 0

    def jump(self):
        pass

    def damage(self, amount):
        """Damages amount of the health of the sprite."""
        pass

    def update(self, world):
        """Update function of Sprite, overwritten.
        Will move only, if there is no collision between the world-sprite group and self."""
        # animation, get next frame
        self.image_index += 0.2
        if self.image_index >= len(self.images):
            self.image_index = 0

        if len(self.images) != 0:
            self.image = self.images[round(math.floor(self.image_index))]  # round only for to_int

        # rotate picture and set position
        self.image = pygame.transform.rotate(self.image, -self.current_angle/math.pi * 180)
        self.rect.center = [self.center[0] + self.radius * math.cos(self.current_angle),
                            self.center[1] + self.radius * math.sin(self.current_angle)]
        self.current_angle -= math.pi/256 + random.random() * 0.02

    def attack(self, other):
        if isinstance(other, character.Character):
            if self.critical_chance > random.random():
                other.damage(self.strength * 2)
            else:
                other.damage(self.strength)
        else:
            raise TypeError("other has to be a character")
