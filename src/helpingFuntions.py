import pygame
import os.path
from PIL import Image
import colors as c


def pic_to_sprite_group_rec(pic):
    """Recursive part of sprite group making"""
    sprite = pygame.sprite.Sprite()
    sprite_group = pygame.sprite.Group()
    sprite.image = pygame.image.load(pic).convert_alpha()
    start_x = -1
    start_y = -1

    im = Image.open(pic)  # Can be many different formats.
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

    if start_x == -1:
        # no black pixel found, recursion stop
        return sprite_group

    # assume until end of picture, if not, change in break
    end_y = im.size[1] - 1
    for y in range(start_y, im.size[1]):
        if not pix[start_x, y] == (0, 0, 0, 255):
            # until there are not one more black pixel direct under this one
            end_y = y-1
            break

    exit_now = False
    for x in range(start_x, im.size[0]):
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

    # write new data to the file
    im.save(pic)

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
    sprite_group.add(pic_to_sprite_group_rec(pic))
    return sprite_group


def pic_to_sprite_group(picture):
    """Takes a picture and finds all black pixels.
    Collects them in a sprite group and returns it"""
    sprite_group = pygame.sprite.Group()
    if os.path.isfile(picture):
        pic = Image.open(picture)
        name, extension = os.path.splitext(picture)
        pic_path = name + "_temp" + extension
        pic.save(pic_path)
        sprite_group.add(pic_to_sprite_group_rec(pic_path))
    return sprite_group


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
