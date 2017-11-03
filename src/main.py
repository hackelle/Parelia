import pygame
import math
import colors as c
import dwarf
import background
import character
import helpingFuntions as hF
import catofly
import random
import sparkledust

DRAW_OBSTACLES = True


def draw_health(color, health):
    """Draws a line according to health given at the health-bar position."""
    pygame.draw.line(screen, color, [size[0] - 50, 20], [size[0] - 50 - health * 1.5, 20], 10)


# init game
pygame.init()

you_lose_font = pygame.font.SysFont('Comic Sans MS', 100)
you_lose_surface = you_lose_font.render('You Lose!', False, (255, 0, 0))
health_font = pygame.font.SysFont('Comic Sans MS', 24)

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

#prepare random spawns
sparkledust.prepare_sparkledust_pictures()
# create the character
dwarf.prepare_dwarf_pictures()
player_character = dwarf.Dwarf()
player_character.rect.x = 20
player_character.rect.y = 470

# create the enemy
enemy_dwarf_1 = dwarf.Dwarf()
enemy_dwarf_1.rect.x = 450
enemy_dwarf_1.rect.y = 470

catofly.prepare_catofly_pictures()
enemy_catofly = pygame.sprite.Group()

for i in range(5):
    this_catofly = catofly.Catofly()
    this_catofly.center = [random.randint(100, 700), random.randint(200, 400)]
    this_catofly.radius = random.randint(30, 50)
    this_catofly.current_angle = random.random() * 2 * math.pi
    enemy_catofly.add(this_catofly)


# load a background in a sprite group
back_ground = background.Background('../res/world/simple_hills_big.png', [0, 0])
background_sprites = pygame.sprite.Group()
background_sprites.add(back_ground)

# add character for later drawing
all_sprites = pygame.sprite.Group()
all_sprites.add(player_character)
all_sprites.add(enemy_dwarf_1)
all_sprites.add(enemy_catofly)


# obstacles are in here
obstacles = pygame.sprite.Group()
obstacles.add(hF.pic_to_sprite_group("../res/world/simple_hills_big_terrain.png"))

# create an enemy group for damage
enemies = pygame.sprite.Group()
enemies.add(enemy_dwarf_1)
enemies.add(enemy_catofly)

# define control keys
jump_keys = [pygame.K_SPACE, pygame.K_w, pygame.K_UP, pygame.K_KP8]
left_keys = [pygame.K_LEFT, pygame.K_a, pygame.K_KP4]
right_keys = [pygame.K_RIGHT, pygame.K_d, pygame.K_KP6]

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
            elif event.key == pygame.K_o:
                DRAW_OBSTACLES = not DRAW_OBSTACLES
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                print("Mouse event at " + str(pygame.mouse.get_pos()))

        elif event.type == pygame.KEYUP:
            pass

    if game_running:

        keys = pygame.key.get_pressed()
        world_shift = 0  # amount, the world has to be shifted for movement

        if hF.list_in_tuple(left_keys, keys):
            world_shift = player_character.move(character.Direction.LEFT, 5, size)
        if hF.list_in_tuple(right_keys, keys):
            world_shift = player_character.move(character.Direction.RIGHT, 5, size)

        # shift the world
        if not world_shift == 0:
            back_ground.shift(world_shift)
            hF.shift_group_x(obstacles.sprites(), world_shift)
            hF.shift_group_x(all_sprites.sprites(), world_shift)

        collision_list = pygame.sprite.spritecollide(player_character, enemies, False)

        # create a random sparkledust about every second
        rand = random.random()
        if rand < 1/60:
            sparkle = sparkledust.Sparkledust()
            sparkle.rect.center = [random.randint(100, 700), 600]
            all_sprites.add(sparkle)
            enemies.add(sparkle)

        # damage for every collision
        for enemy in collision_list:
            enemy.attack(player_character)

        # update with game logic
        all_sprites.update(obstacles)

        # draw background
        background_sprites.draw(screen)

        # draw sun
        background.draw_sun(screen, sun_rotation)

        sun_rotation -= math.pi*2
        sun_rotation += math.pi/360

        # Draw all the sprites in one go.
        all_sprites.draw(screen)

        # draw health
        if player_character.health <= 0:
            # show red overlay
            red_surface = pygame.Surface(size)  # the size of your rect
            red_surface.set_alpha(200)  # alpha level out of 255. 255 is no transparency
            red_surface.fill(c.RED_DEAD)  # this fills the entire surface
            screen.blit(red_surface, (0, 0))
            # show message
            screen.blit(you_lose_surface, (size[0]/2-180, size[1]/2-50))
            # stop movement
            game_running = False
        if player_character.health < 20:
            health_surface = health_font.render(str(player_character.health), False, c.HEALTH_RED)
            screen.blit(health_surface, (size[0] - 40, 13))
            draw_health(c.HEALTH_RED, player_character.health)
        elif player_character.health < 50:
            health_surface = health_font.render(str(player_character.health), False, c.HEALTH_YELLOW)
            screen.blit(health_surface, (size[0] - 40, 13))
            draw_health(c.HEALTH_YELLOW, player_character.health)
        else:
            health_surface = health_font.render(str(player_character.health), False, c.HEALTH_GREEN)
            screen.blit(health_surface, (size[0] - 40, 13))
            draw_health(c.HEALTH_GREEN, player_character.health)

        # draw obstacles for debug
        if DRAW_OBSTACLES:
            # show red overlay
            obstacles.draw(screen)

        for sprite in all_sprites.sprites():
            if sprite.rect.y < -50 or sprite.rect.y > (size[1] + 50):
                sprite.kill()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
