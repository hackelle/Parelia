import pygame
import colors as c
import os.path
import character


class Dwarf(character.Character):
    """This class represents a character. It derives from the "Sprite" class in Pygame."""

    # fixed attributes
    jump_height = 15  # How high can the character jump in a single jump?
    max_possible_jumps = 2  # Number of possible jumps. 1 for single jump, 2 for double ...
    max_health = 100  # maximum health
    armor = 100  # factor for protection (1x damage @ 100)
    strength = 0  # factor for damage dealing
    critical_chance = 0  # possibility for critical hits
    walk_speed = 5  # the speed, the character can walk each update
    image = None  # visual representation, should be drawable
    rect = None  # rectangle surrounding the character

    # changed by functions
    remaining_jumps = 2  # Number of jumps currently remaining
    vertical_velocity = 0  # the current jumping/falling speed
    health = 100  # current health
    level = 1  # characters level, should be used for some calculations

    # variables for the next update
    next_x = -1
    next_y = -1

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the character, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([50, 10])
        self.image.fill(c.WHITE)
        self.image.set_colorkey(c.WHITE)

        # Draw the character (a rectangle!) on the surface
        pygame.draw.rect(self.image, c.WHITE, [0, 0, 50, 10])

        # Instead we could load a proper picture of a character
        # Overwrite self.image, if dwarf-picture found
        if os.path.isfile("../res/pics/dwarf-64.png"):
            self.image = pygame.image.load("../res/pics/dwarf-64.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move(self, direction, pixels, screen_size):
        if direction == character.Direction.RIGHT:
            if self.rect.x < screen_size[0] - self.walk_speed - self.rect.width:
                # going right and not at border
                self.next_x = self.rect.x + self.walk_speed
            else:
                self.next_x = screen_size[0] - self.rect.width
        elif direction == character.Direction.LEFT:
            if self.rect.x > 0 + self.walk_speed:
                # going left and not at border
                self.next_x = self.rect.x - self.walk_speed
            else:
                self.next_x = 0

    def jump(self):
        if self.remaining_jumps > 0:
            self.remaining_jumps -= 1
            self.vertical_velocity = self.jump_height

    def damage(self, amount):
        """Damages amount of the health of the sprite."""
        if self.health > 0:
            self.health -= amount
        else:
            self.health = 0

    def update(self, world):
        """Update function of Sprite, overwritten.
        Will move only, if there is no collision between the world-sprite group and self."""
        # try this y move
        # only move, if y is not colliding, else set velocity to 0 and reset jumps
        self.next_y = self.rect.y - self.vertical_velocity  # jumping up is y lower
        self.vertical_velocity -= 1
        old_y = self.rect.y
        self.rect.y = self.next_y
        if pygame.sprite.spritecollide(self, world, False):
            self.rect.y = old_y
            self.vertical_velocity = 0
            self.remaining_jumps = self.max_possible_jumps

        # try this x move
        # only move, if x is not colliding
        if not self.next_x == -1:
            old_x = self.rect.x
            self.rect.x = self.next_x
            if pygame.sprite.spritecollide(self, world, False):
                self.rect.x = old_x

        # healing
        if self.health < 100:
            self.health += .5
        else:
            self.health = 100

    def attack(self, other):
        if issubclass(character.Character, other):
            pass
        else:
            raise TypeError("other has to be a character")