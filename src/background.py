import pygame
import math
import colors as c


def draw_sun(screen, current_rotation):
    """Draws the sun on screen at the sun-location with the current_rotation"""
    pygame.draw.ellipse(screen, c.SUN, [70, 40, 100, 100], 0)
    for i in range(8):
        length_correction = math.fabs(0.2 * math.sin(current_rotation) + 0.2 * math.sin(2 * current_rotation)) + 0.8
        start_x = 120 + math.cos(current_rotation) * 55
        start_y = 90 + math.sin(current_rotation) * 55
        end_x = 120 + math.cos(current_rotation) * 85 * length_correction
        end_y = 90 + math.sin(current_rotation) * 85 * length_correction
        pygame.draw.line(screen, c.SUN, [start_x, start_y], [end_x, end_y], 3)
        current_rotation += math.pi / 4


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
