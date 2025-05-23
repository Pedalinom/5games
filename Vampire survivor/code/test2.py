import pygame 
from os.path import join 

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivor-test environment")
clock = pygame.time.Clock()
running = True

# Load images
down_walk = [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(0, 4)]
left_walk = [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(0, 4)]
right_walk = [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range(0, 4)]
up_walk = [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(0, 4)]

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = down_walk[0]
        self.rect = self.image.get_frect(center=(25, 25))
        self.direction = pygame.math.Vector2()
        self.speed = 100
        self.frame_index = 0
        self.animation_speed = 0.1
        self.current_direction = 'down'
        self.images = {
            'down': down_walk,
            'left': left_walk,
            'right': right_walk,
            'up': up_walk
        }
        # Animation timer for tap animation
        self.anim_timer = 0
        self.anim_duration = 0.15  # seconds to continue animating after tap
        

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if keys[pygame.K_RIGHT]:
            self.current_direction = 'right'
        elif keys[pygame.K_LEFT]:
            self.current_direction = 'left'
        elif keys[pygame.K_UP]:
            self.current_direction = 'up'
        elif keys[pygame.K_DOWN]:
            self.current_direction = 'down'
        else:
            self.moved = False

        # If movement key is pressed, reset animation timer
        if self.direction.length() > 0:
            self.anim_timer = self.anim_duration
            self.direction = self.direction.normalize()
            # Move and clamp x axis first with mask collision
            if self.direction.x != 0:
                self.rect.centerx += self.direction.x * self.speed * dt
            # Then move and clamp y axis with mask collision
            if self.direction.y != 0:
                self.rect.centery += self.direction.y * self.speed * dt
        else:
            # Decrease animation timer if not moving
            if self.anim_timer > 0:
                self.anim_timer -= dt
            else:
                self.anim_timer = 0

        # Animate if moving or animation timer is active
        if self.direction.length() > 0 or self.anim_timer > 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.images[self.current_direction]):
                self.frame_index = 0
            self.image = self.images[self.current_direction][int(self.frame_index)]
        else:
            self.frame_index = 0
            self.image = self.images[self.current_direction][int(self.frame_index)]
        

        if self.rect.left < -32:
            self.rect.left = -32
        if self.rect.right > 832:
            self.rect.right = 832
        if self.rect.top < -32:
            self.rect.top = -32
        if self.rect.bottom > 632:
            self.rect.bottom = 632


all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    all_sprites.update(dt)

    if player.direction.length() > 0:
        feet_x = player.rect.centerx + 20
        feet_y = player.rect.centery - 30
        tile_x = int(feet_x // 40)
        tile_y = int(feet_y // 40)
        print(f"Player is in tile: ({tile_x}, {tile_y})  Pixel: ({int(player.rect.centerx)}, {int(player.rect.centery)})")

    screen.fill((100, 100, 100))

    for row in range(15):
        for col in range(20):
            rect = pygame.Rect(col * 40, row * 40, 40, 40)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    all_sprites.draw(screen)

    pygame.display.update()
    

pygame.quit()

