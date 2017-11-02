import pygame
import math
import colors as c
import dwarf
import background
import character
import helpingFuntions as hf

DRAW_OBSTACLES = True

def draw_health(color, health):
    """Draws a line according to health given at the health-bar position."""
    pygame.draw.line(screen, color, [size[0] - 10, 20], [size[0] - 10 - health * 1.5, 20], 10)


# init game
pygame.init()

you_loose_font = pygame.font.SysFont('Comic Sans MS', 100)
you_loose_surface = you_loose_font.render('You Loose!', False, (255, 0, 0))

# init screen
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Parelia")


# The loop will carry on until the user exit the game (e.g. clicks the close button).
carry_on = True
game_running = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

sun_rotation = 0

# create the character
player_character = dwarf.Dwarf()
player_character.rect.x = 20
player_character.rect.y = 470

# create the enemy
enemy_1 = dwarf.Dwarf()
enemy_1.rect.x = 650
enemy_1.rect.y = 470

# load a background
back_ground = background.Background('../res/world/simple_hills_big.png', [0, 0])

# add character for later drawing
all_sprites = pygame.sprite.Group()
all_sprites.add(player_character)
all_sprites.add(enemy_1)


# obstacles are in here
obstacles = pygame.sprite.Group()
obstacles.add(hf.pic_to_sprite_group("../res/world/simple_hills_big_terrain.png"))

# create an enemy group for damage
enemies = pygame.sprite.Group()
enemies.add(enemy_1)

# define control keys
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
        if hf.list_in_tuple(left_keys, keys):
            player_character.move(character.Direction.LEFT, 5, size)
        if hf.list_in_tuple(right_keys, keys):
            player_character.move(character.Direction.RIGHT, 5, size)

    collision_list = pygame.sprite.spritecollide(player_character, enemies, False)

    # damage for every collision
    player_character.damage(2 * len(collision_list))

    # update with game logic
    if game_running:
        all_sprites.update(obstacles)

    # draw background
    screen.fill([255, 255, 255])
    screen.blit(back_ground.image, back_ground.rect)

    # draw sun
    back_ground.draw_sun(screen, sun_rotation)

    sun_rotation -= math.pi*2
    sun_rotation += math.pi/360

    # Draw all the sprites in one go.
    all_sprites.draw(screen)

    # draw health
    if player_character.health <= 0:
        # show red overlay
        gray_surface = pygame.Surface(size)  # the size of your rect
        gray_surface.set_alpha(200)  # alpha level out of 255. 255 is no transparency
        gray_surface.fill(c.RED_DEAD)  # this fills the entire surface
        screen.blit(gray_surface, (0, 0))
        # show message
        screen.blit(you_loose_surface, (180, 200))
        # stop movement
        game_running = False
    if player_character.health < 20:
        draw_health(c.HEALTH_RED, player_character.health)
    elif player_character.health < 50:
        draw_health(c.HEALTH_YELLOW, player_character.health)
    else:
        draw_health(c.HEALTH_GREEN, player_character.health)

    # draw obstacles for debug
    if DRAW_OBSTACLES:
        obstacles.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
