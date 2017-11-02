import pygame
from enum import Enum
from abc import ABC, abstractmethod


class Direction(Enum):
    """Directions a Character could go"""
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    BACK = 4
    FRONT = 5


class Character(ABC, pygame.sprite.Sprite):
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

    @abstractmethod
    def __init__(self):
        super().__init__()  # call Sprite init

    @abstractmethod
    def move(self, direction, pixels, screen_size):
        """Moves the sprite pixels to the direction (enum), if he doesn't leave the screen.
        Else stays where he is.
        Returns, how much the world is to be shifted"""
        pass

    @abstractmethod
    def jump(self):
        """Jumps the character based on it's jump specs."""
        pass

    @abstractmethod
    def damage(self, amount):
        """Damages amount of the health of the sprite."""
        pass

    @abstractmethod
    def attack(self, other):
        """Attacks an other sprite."""
        pass

    @abstractmethod
    def update(self, world):
        """Update function of Sprite, overwritten. World is a sprite group having all obstacles"""
        pass
