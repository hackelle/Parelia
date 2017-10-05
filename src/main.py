import pygame
import math
import colors as c
import dwarf


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

# init game
pygame.init()

you_loose_font = pygame.font.SysFont('Comic Sans MS', 100)
you_loose_surface = you_loose_font.render('You Loose!', False, (255, 0, 0))

# init screen
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Parelia")


# The loop will carry on until the user exit the game (e.g. clicks the close button).
carry_on = True
game_running = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

sun_rotation = 0

# create the character
player_character = dwarf.Dwarf(c.BLACK, 20, 30)
player_character.rect.x = 20
player_character.rect.y = 380

# create the enemy
enemy_1 = dwarf.Dwarf(c.BLACK, 20, 30)
enemy_1.rect.x = 650
enemy_1.rect.y = 380

# add character for later drawing
all_spirits = pygame.sprite.Group()
all_spirits.add(player_character)
all_spirits.add(enemy_1)

enemies = pygame.sprite.Group()
enemies.add(enemy_1)

jump_keys = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
left_keys = [pygame.K_LEFT, pygame.K_a]
right_keys = [pygame.K_RIGHT, pygame.K_d]

# -------- Main Program Loop -----------
while carry_on:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carry_on = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carry_on = False
            elif event.key in jump_keys:
                if game_running:
                    player_character.jump()

        elif event.type == pygame.KEYUP:
            pass

    keys = pygame.key.get_pressed()
    if game_running:
        if list_in_tuple(left_keys, keys):
            player_character.move_left(5, size)
        if list_in_tuple(right_keys, keys):
            player_character.move_right(5, size)

    collision_list = pygame.sprite.spritecollide(player_character, enemies, False)
    if len(collision_list) > 0:
        player_character.damage(2)

    # update with game logic
    if game_running:
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

    # draw health
    if player_character.health <= 0:
        # show gray overlay
        gray_surface = pygame.Surface((700, 500))  # the size of your rect
        gray_surface.set_alpha(200)  # alpha level
        gray_surface.fill(c.GRAY_TRANSPARENT)  # this fills the entire surface
        screen.blit(gray_surface, (0, 0))
        # show message
        screen.blit(you_loose_surface, (180, 200))
        # stop movement
        game_running = False
    if player_character.health < 20:
        pygame.draw.line(screen, c.HEALTH_RED, [690, 20], [690 - player_character.health*1.5, 20], 5)
    elif player_character.health < 50:
        pygame.draw.line(screen, c.HEALTH_YELLOW, [690, 20], [690 - player_character.health*1.5, 20], 5)
    else:
        pygame.draw.line(screen, c.HEALTH_GREEN, [690, 20], [690 - player_character.health*1.5, 20], 5)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()