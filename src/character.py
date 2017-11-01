import pygame
from enum import Enum


class Direction(Enum):
    """Directions a Character could go"""
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    BACK = 4
    FRONT = 5


class Character(pygame.sprite.Sprite):
    """This class represents a character. It derives from the "Sprite" class in Pygame."""

    # fixed attributes
    jump_height = 0  # How high can the character jump in a single jump?
    max_possible_jumps = 0  # Number of possible jumps. 1 for single jump, 2 for double ...
    max_health = 0  # maximum health
    armor = 0  # factor for protection (1x damage @ 100)
    strength = 0  # factor for damage dealing
    critical_chance = 0  # possibility for critical hits
    walk_speed = 0  # the speed, the character can walk each update
    image = None  # visual representation, should be drawable
    rect = None  # rectangle surrounding the character

    # changed by functions
    remaining_jumps = 0  # Number of jumps currently remaining
    vertical_velocity = 0  # the current jumping/falling speed
    health = 0  # current health
    level = 1  # characters level, should be used for some calculations

    def __init__(self):
        raise NotImplementedError("Should have implemented this. Also use super().__init__()")

    def move(self, direction, pixels, screen_size):
        """Moves the sprite pixels to the direction (enum), if he doesn't leave the screen.
        Else stays where he is."""
        raise NotImplementedError("Should have implemented this")

    def jump(self):
        """Jumps the character based on it's jump specs."""
        raise NotImplementedError("Should have implemented this")

    def stick_to_ground(self, ground_level):
        """Sets the sprite to ground_level given, all velocities set to 0."""
        raise NotImplementedError("Should have implemented this")

    def damage(self, amount):
        """Damages amount of the health of the sprite."""
        raise NotImplementedError("Should have implemented this")

    def attack(self, other):
        """Attacks an other sprite."""
        raise NotImplementedError("Should have implemented this")

    def update(self):
        """Update function of Sprite, overwritten"""
        raise NotImplementedError("Should have implemented this")
