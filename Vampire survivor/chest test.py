import pygame
import sys
from os.path import join

pygame.init()

# Tile settings
TILE_SIZE = 50
TILE_COLS = 16  # 800 / 50
TILE_ROWS = 12  # 600 / 50

screen_width = TILE_COLS * TILE_SIZE
screen_height = TILE_ROWS * TILE_SIZE
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tilemap Example")

# Colors
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)

# Load images for all directions
player_imgs = {
    'down': [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)],
    'up': [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(4)],
    'left': [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(4)],
    'right': [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range(4)]
}
chest_img = pygame.image.load(join('images', 'Chest.png')).convert_alpha()

# Player position (pixel-based)
player_x = 2 * TILE_SIZE
player_y = 2 * TILE_SIZE
player_speed = 3  # pixels per frame
player_direction = 'down'
player_anim_index = 0
player_anim_timer = 0
player_anim_interval = 80  # ms per frame

# Chest tile position (center of grid)
chest_tile_x = TILE_COLS // 2
chest_tile_y = TILE_ROWS // 2

def draw_grid():
    for x in range(0, screen_width, TILE_SIZE):
        pygame.draw.line(screen, gray, (x, 0), (x, screen_height))
    for y in range(0, screen_height, TILE_SIZE):
        pygame.draw.line(screen, gray, (0, y), (screen_width, y))

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
    # Normalize diagonal movement
    if dx != 0 and dy != 0:
        dx *= 0.7071
        dy *= 0.7071
    moved = False
    if dx != 0 or dy != 0:
        # Determine intended direction for animation
        if abs(dx) > abs(dy):
            player_direction = 'right' if dx > 0 else 'left'
        elif abs(dy) > 0:
            player_direction = 'down' if dy > 0 else 'up'
        # Calculate new pixel position
        new_x = player_x + dx * player_speed
        new_y = player_y + dy * player_speed
        # Calculate the tile the player's feet would be in
        feet_x = new_x + TILE_SIZE // 2
        feet_y = new_y + TILE_SIZE - 10  # feet near bottom of sprite
        tile_x = int(feet_x // TILE_SIZE)
        tile_y = int(feet_y // TILE_SIZE)
        # Check bounds and chest collision
        if 0 <= tile_x < TILE_COLS and 0 <= tile_y < TILE_ROWS:
            if not (tile_x == chest_tile_x and tile_y == chest_tile_y):
                player_x = new_x
                player_y = new_y
                moved = True
    # Animation update
    if moved:
        player_anim_timer += dt
        if player_anim_timer > player_anim_interval:
            player_anim_index = (player_anim_index + 1) % 4
            player_anim_timer = 0
        # Print the player's current tile position
        feet_x = player_x + TILE_SIZE // 2
        feet_y = player_y + TILE_SIZE - 10
        tile_x = int(feet_x // TILE_SIZE)
        tile_y = int(feet_y // TILE_SIZE)
        print(f"Player is in tile: ({tile_x}, {tile_y})  Pixel: ({int(player_x)}, {int(player_y)})")
    else:
        player_anim_index = 0
        player_anim_timer = 0

    screen.fill(white)
    draw_grid()
    # Draw chest image in the chest tile
    chest_rect = pygame.Rect(chest_tile_x * TILE_SIZE, chest_tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    chest_img_scaled = pygame.transform.scale(chest_img, (TILE_SIZE, TILE_SIZE))
    screen.blit(chest_img_scaled, chest_rect)
    # Draw player animation frame at pixel position, feet anchored to tile
    player_draw_x = int(player_x + TILE_SIZE // 2 - 40)
    player_draw_y = int(player_y + TILE_SIZE - 80)
    player_rect = pygame.Rect(player_draw_x, player_draw_y, 80, 80)
    player_img_scaled = pygame.transform.scale(player_imgs[player_direction][player_anim_index], (80, 80))
    screen.blit(player_img_scaled, player_rect)
    pygame.display.flip()
