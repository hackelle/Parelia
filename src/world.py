import os.path
import pygame
import colors as c
from PIL import Image


class World(pygame.sprite.Sprite):
    """A representation of a map"""
    accessable_blocks = []  # double array of all accessable blocks

    def __init__(self, picture):
        super().__init__()
        """Creates a block map, depending on the picture. All black-non transparent pixels are not accessable."""

        if os.path.isfile(picture):
            self.image = pygame.image.load(picture).convert_alpha()
            im = Image.open(picture)  # Can be many different formats.
            pix = im.load()
            # find the first black pixel going column by column from the left
            exit_now = False
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    if pix[i, j] == (0, 0, 0, 255):
                        start_x = i
                        start_y = j
                        # that's the start of the rectangle
                        exit_now = True
                        break
                if exit_now:
                    break

            # find the last black pixel going column by column from the left
            exit_now = False
            for i in reversed(range(im.size[0])):
                for j in reversed(range(im.size[1])):
                    if pix[i, j] == (0, 0, 0, 255):
                        end_x = i
                        end_y = j
                        # that's the end of the rectangle
                        exit_now = True
                        break
                if exit_now:
                    break

            # create rectangle in correct proportions
            self.image = pygame.Surface([end_x-start_x+1, end_y-start_y+1])

            # Draw the character (a rectangle!) on the surface (only black rectangle)
            pygame.draw.rect(self.image, c.BLACK, [0, 0, end_x-start_x, end_y-start_y])
        else:
            # Pass in the color of the character, and its x and y position, width and height.
            # Set the background color and set it to be transparent
            self.image = pygame.Surface([50, 10])

            start_x = 0
            start_y = 0

            # Draw the character (a rectangle!) on the surface
            pygame.draw.rect(self.image, c.WHITE, [0, 0, 50, 10])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

