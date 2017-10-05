import pygame
import math
import colors as c
import person

# init game
pygame.init()

# init screen
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Parelia")


# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

sun_rotation = 0

# create the character
player_character = person.Person(c.BLACK, 20, 30)
player_character.rect.x = 20
player_character.rect.y = 380

# add character for later drawing
all_spirits = pygame.sprite.Group()
all_spirits.add(player_character)

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carryOn = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_character.move_left(5)
    if keys[pygame.K_RIGHT]:
        player_character.move_right(5)

    # update with game logic
    all_spirits.update()

    # draw background
    # grass and sky
    pygame.draw.rect(screen, c.GRASS, [0, 300, 700, 200], 0)
    pygame.draw.rect(screen, c.SKY, [0, 0, 700, 300], 0)

    # draw sun
    pygame.draw.ellipse(screen, c.SUN, [70, 40, 100, 100], 0)
    for i in range(8):
        length_correction = math.fabs(0.2 * math.sin(sun_rotation) + 0.2 * math.sin(2*sun_rotation)) + 0.8
        start_x = 120 + math.cos(sun_rotation) * 55
        start_y = 90 + math.sin(sun_rotation) * 55
        end_x = 120 + math.cos(sun_rotation) * 85 * length_correction
        end_y = 90 + math.sin(sun_rotation) * 85 * length_correction
        pygame.draw.line(screen, c.SUN, [start_x, start_y], [end_x, end_y], 3)
        sun_rotation += math.pi / 4

    sun_rotation -= math.pi*2
    sun_rotation += math.pi/360

    # draw tree
    pygame.draw.rect(screen, c.TREE_STOMP, [550, 200, 30, 150], 0)
    pygame.draw.ellipse(screen, c.LEAF, [500, 100, 130, 180], 0)

    # Draw The Road
    pygame.draw.rect(screen, c.GRAY, [0, 400, 700, 50])
    # Draw Line painting on the road
    pygame.draw.line(screen, c.WHITE, [0, 420], [700, 420], 2)

    # Draw all the sprites in one go.
    all_spirits.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()