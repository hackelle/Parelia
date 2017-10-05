import pygame
import colors as c
import os.path


class Dwarf(pygame.sprite.Sprite):
    # This class represents a character. It derives from the "Sprite" class in Pygame.
    in_air = False
    double_jump = False
    vertical_velocity = 0
    vertical_jump_height = 0
    jump_base_y = -1
    health = 100

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the character, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(c.WHITE)
        self.image.set_colorkey(c.WHITE)

        # Draw the character (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Instead we could load a proper picture of a character
        # Overwrite self.image, if dwarf-picture found
        if os.path.isfile("../res/pics/dwarf-64.png"):
            self.image = pygame.image.load("../res/pics/dwarf-64.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move_right(self, pixels, screen_size):
        if self.rect.x < screen_size[0]-self.rect.width-pixels:
            self.rect.x += pixels

    def move_left(self, pixels, screen_size):
        if 0 < self.rect.x-pixels:
            self.rect.x -= pixels

    def jump(self):
        if not self.double_jump:
            if self.in_air:
                self.double_jump = True
                self.vertical_velocity += 7
            else:
                self.in_air = True
                self.jump_base_y = self.rect.y
                self.vertical_velocity += 15

    def stick_to_ground(self):
        self.vertical_velocity = 0
        self.vertical_jump_height = 0
        self.double_jump = False
        self.in_air = False
        self.rect.y = self.jump_base_y
        self.jump_base_y = -1

    def damage(self, amount):
        if self.health > 0:
            self.health -= amount
        else:
            self.health = 0

    def update(self):
        if self.in_air:
            self.vertical_velocity -= 1

        if not self.vertical_velocity == 0:
            self.vertical_jump_height += self.vertical_velocity
            # going up is lower y
            self.rect.y = self.jump_base_y - self.vertical_jump_height

        # underground
        if self.vertical_jump_height < 0:
            self.stick_to_ground()

        if self.health < 100:
            self.health += .5
        else:
            self.health = 100
