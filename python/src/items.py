import pygame
from abc import ABC, abstractmethod


class Item(ABC, pygame.sprite.Sprite):

    @abstractmethod
    def damage_sprite(self, other):
        """Attacks an other sprite."""
        pass

    @abstractmethod
    def use(self):
        """Uses the effect of the item."""
        pass
