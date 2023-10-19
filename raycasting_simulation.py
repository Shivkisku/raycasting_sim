import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 30

# create a pygame window, constants
HEIGHT = 750
WIDTH = 1200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("raycasting")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (150, 150, 150)
RAY_COLOR = (222, 222, 35)

FOV = math.pi / 3  # ~ 60 deg.
CASTED_RAYS = 150
STEP_ANGLE = FOV / CASTED_RAYS  # space between rays
MAX_DEPTH = WIDTH  # maximum length of a ray
player_angle = 0  # the starting angle
WALL_WIDTH = WIDTH // CASTED_RAYS
MAP_SIZE = 240
SQUARE_SIZE = MAP_SIZE / 20

player_x = MAP_SIZE / 2
player_y = MAP_SIZE / 2

direction = 'f'  # for collision detection: f(forwards) or b (backwards) or fs (forwards with shift)

MAP = (
    # 20x20
    '####################',
    '#                  #',
    '#                  #',
    '#          ###     #',
    '#          # #     #',
    '#          ###     #',
    '#   ####           #',
    '#   #  #           #',
    '#   #  #           #',
    '#   #  #           #',
    '#   #  #           #',
    '#   ####           #',
    '#               # ##',
    '#          #    #  #',
    '#          #    #  #',
    '#        ###    #  #',
    '#               #  #',
    '#                  #',
    '#                  #',
    '####################'
)


def update_player_pos():
    # player movement

    global player_angle, player_x, player_y, direction

    last_key_pressed = None  # for collision detection purposes

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_angle -= .1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_angle += .1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        direction = 'f'
        player_x += -math.sin(player_angle) * 1.5
        player_y += math.cos(player_angle) * 1.5
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            direction = 'fs'
            player_x += -math.sin(player_angle)
            player_y += math.cos(player_angle)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direction = 'b'
        player_x -= -math.sin(player_angle) * 1.5
        player_y -= math.cos(player_angle) * 1.5


def check_collision():
    global player_x, player_y

    col = int(player_x / SQUARE_SIZE)
    row = int(player_y / SQUARE_SIZE)
    if MAP[row][col] == '#':
        if direction == 'f':  # going forwards
            player_x -= -math.sin(player_angle) * 3
            player_y -= math.cos(player_angle) * 3
        elif direction == 'fs':  # going forwards with shift
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:  # going backwards
            player_x += -math.sin(player_angle) * 3
            player_y += math.cos(player_angle) * 3


def draw_wall(wall_height, ray, color):
    pygame.draw.rect(WIN, color, (ray * WALL_WIDTH, HEIGHT / 2 - wall_height / 2, WALL_WIDTH, wall_height))


def cast_rays():
    start_angle = player_angle - FOV / 2
    rays_to_draw = []

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # convert x, y coordinates to col, row
            col = int(target_x / SQUARE_SIZE)
            row = int(target_y / SQUARE_SIZE)

            if MAP[row][col] == '#':
                rays_to_draw.append((target_x, target_y))

                shade = 255 / (1 + depth * .02)  # the further away the ray goes, the darker the shade gets
                depth *= math.cos(player_angle - start_angle)  # to prevent the fish eye effect
                wall_height = 21_000 / (depth + 0.0001)
                draw_wall(wall_height, ray, (shade, shade, shade))

                break

        start_angle += STEP_ANGLE

    draw_map(rays_to_draw)


def draw_map(rays):
    # the map
    for row in range(20):
        for col in range(20):
            # if it's a wall
            if MAP[row][col] == '#':
                pygame.draw.rect(WIN, BLACK, (SQUARE_SIZE * col, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(WIN, LIGHT_GREY, (SQUARE_SIZE * col, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))

    # the player
    pygame.draw.circle(WIN, BLACK, (int(player_x), int(player_y)), 5)

    # the rays
    for ray in rays:
        pygame.draw.line(WIN, RAY_COLOR, (int(player_x), int(player_y)), (int(ray[0]), int(ray[1])))


def draw_floor():
    n_of_layers = 100
    step = HEIGHT / 2 / n_of_layers
    shade_step = 255 // n_of_layers
    shade = 0
    y_pos = HEIGHT / 2
    for tyle in range(n_of_layers):
        pygame.draw.rect(WIN, (shade, shade, shade), (0, int(y_pos), WIDTH, int(y_pos)))
        shade += shade_step
        y_pos += step


def update():
    WIN.fill(BLACK)

    draw_floor()
    update_player_pos()
    check_collision()
    cast_rays()  # also calls draw_map

    clock.tick(FPS)
    pygame.display.update()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        update()

    pygame.quit()


if __name__ == '__main__':
    main()
