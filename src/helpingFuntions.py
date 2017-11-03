import pygame
import os.path
from PIL import Image
import colors as c
import catofly


def pic_to_sprite_group_rec(image):
    """Recursive part of sprite group making"""
    sprite = pygame.sprite.Sprite()
    sprite_group = pygame.sprite.Group()
    start_x = -1
    start_y = -1

    pix = image.load()
    # find the first black pixel going column by column from the left
    exit_now = False
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pix[i, j] == (0, 0, 0, 255):
                start_x = i
                start_y = j
                # that's the start of the rectangle
                exit_now = True
                break
        if exit_now:
            break

    if start_x == -1:
        # no black pixel found, recursion stop
        return sprite_group

    # assume until end of picture, if not, change in break
    end_y = image.size[1] - 1
    for y in range(start_y, image.size[1]):
        if not pix[start_x, y] == (0, 0, 0, 255):
            # until there are not one more black pixel direct under this one
            end_y = y-1
            break

    exit_now = False
    for x in range(start_x, image.size[0]):
        for y in range(start_y, end_y+1):
            if not pix[x, y] == (0, 0, 0, 255):
                # until there are no more black pixel columns direct next to this one
                exit_now = True
                break
            else:
                # mark pixel green for next iterations
                pix[x, y] = (0, 255, 0, 255)
        if exit_now:
            end_x = x - 1
            break
        else:
            end_x = x

    # create rectangle in correct proportions
    sprite.image = pygame.Surface([end_x - start_x + 1, end_y - start_y + 1])
    color = c.OBSTACLE  # needs to be 4D including alpha for transparency
    sprite.image.set_alpha(color[3])

    # Draw the obstacle (a rectangle!) on the surface (only black rectangle)
    pygame.draw.rect(sprite.image, color, [0, 0, end_x - start_x, end_y - start_y])

    # Fetch the rectangle object that has the dimensions of the image.
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = start_x
    sprite.rect.y = start_y

    # add sprite to group
    sprite_group.add(sprite)
    # add all other sprites recursive
    sprite_group.add(pic_to_sprite_group_rec(image))
    return sprite_group


def add_surrounding_sprites(image):
    """Returns 4 sprites surrounding the picture in a group."""
    sprite_group = pygame.sprite.Group()

    color = c.OBSTACLE  # needs to be 4D including alpha for transparency

    top_sprite = pygame.sprite.Sprite()
    # create rectangle in correct proportions, 50 over at each side, 50 top
    top_sprite.image = pygame.Surface([image.size[0] + 100, 50])
    top_sprite.image.set_alpha(color[3])
    # Draw the obstacle (a rectangle!) on the surface
    pygame.draw.rect(top_sprite.image, color, [0, 0, image.size[0]+100, 50])
    # Fetch the rectangle object that has the dimensions of the image.
    top_sprite.rect = top_sprite.image.get_rect()
    top_sprite.rect.x = -50
    top_sprite.rect.y = -50

    bottom_sprite = pygame.sprite.Sprite()
    # create rectangle in correct proportions, 50 over at each side, 50 bottom
    bottom_sprite.image = pygame.Surface([image.size[0] + 100, 50])
    bottom_sprite.image.set_alpha(color[3])
    # Draw the obstacle (a rectangle!) on the surface
    pygame.draw.rect(bottom_sprite.image, color, [0, 0, image.size[0]+100, 50])
    # Fetch the rectangle object that has the dimensions of the image.
    bottom_sprite.rect = bottom_sprite.image.get_rect()
    bottom_sprite.rect.x = -50
    bottom_sprite.rect.y = image.size[1]

    right_sprite = pygame.sprite.Sprite()
    # create rectangle in correct proportions, 50 over at each side, 50 right
    right_sprite.image = pygame.Surface([50, image.size[1] + 100])
    right_sprite.image.set_alpha(color[3])
    # Draw the obstacle (a rectangle!) on the surface
    pygame.draw.rect(right_sprite.image, color, [0, 0, 50, image.size[1]+100])
    # Fetch the rectangle object that has the dimensions of the image.
    right_sprite.rect = right_sprite.image.get_rect()
    right_sprite.rect.x = image.size[0]
    right_sprite.rect.y = -50

    left_sprite = pygame.sprite.Sprite()
    # create rectangle in correct proportions, 50 over at each side, 50 left
    left_sprite.image = pygame.Surface([50, image.size[1] + 100])
    left_sprite.image.set_alpha(color[3])
    # Draw the obstacle (a rectangle!) on the surface
    pygame.draw.rect(left_sprite.image, color, [0, 0, 50, image.size[1]+1000])
    # Fetch the rectangle object that has the dimensions of the image.
    left_sprite.rect = left_sprite.image.get_rect()
    left_sprite.rect.x = -50
    left_sprite.rect.y = -50

    sprite_group.add(top_sprite)
    sprite_group.add(bottom_sprite)
    sprite_group.add(left_sprite)
    sprite_group.add(right_sprite)
    return sprite_group


def pic_to_sprite_group(picture):
    """Takes a picture and finds all black pixels.
    Collects them in a sprite group and returns it"""
    sprite_group = pygame.sprite.Group()
    if os.path.isfile(picture):
        image = Image.open(picture)
        sprite_group.add(pic_to_sprite_group_rec(image))
        # make a big surrounding sprite
        sprite_group.add(add_surrounding_sprites(image))
    print("terrain build")
    return sprite_group


def shift_group_x(sprite_list, amount):
    for sprite in sprite_list:
        if isinstance(sprite, catofly.Catofly):
            sprite.center[0] += amount
        else:
            sprite.rect.x += amount


def list_in_tuple(list_in, tuple_in):
    """list_in is a list of indexes for tuple_in.
    Returns True, if any of list_in indexes in tuple_in is True.
    Returns false otherwise or if Index out of Range
    """
    try:
        for l in range(len(list_in)):
            if tuple_in[list_in[l]]:
                return True
    except:
        return False
    return False
