import pygame 
from os.path import join 

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Vampire Survivor-test environment")
clock = pygame.time.Clock()
running = True

# Load images
down_walk = [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(0, 3)]
left_walk = [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(0, 3)]
right_walk = [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range(0, 3)]
up_walk = [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(0, 3)]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 'down'
        self.walk_images = {
            'down': down_walk,
            'left': left_walk,
            'right': right_walk,
            'up': up_walk
        }
        self.frame = 0
        self.image = self.walk_images[self.direction][self.frame]
        self.speed = 4
        self.anim_counter = 0

    def update(self, keys):
        moved = False
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        if dx != 0 or dy != 0:
            moved = True
            self.x += dx
            self.y += dy
            # Set direction for animation
            if dx < 0:
                self.direction = 'left'
            elif dx > 0:
                self.direction = 'right'
            elif dy < 0:
                self.direction = 'up'
            elif dy > 0:
                self.direction = 'down'

        if self.x <0:
            self.x = 0
        if self.x > 800:
            self.x = 800
        if self.y < 0:
            self.y = 0
        if self.y > 600:
            self.y = 600

        if moved:
            self.anim_counter += 1
            if self.anim_counter % 8 == 0:
                self.frame = (self.frame + 1) % len(self.walk_images[self.direction])
        else:
            self.frame = 0  # Reset to standing frame

        self.image = self.walk_images[self.direction][self.frame]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

player = Player(400, 300)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill((0, 0, 0))

    for row in range(15):
        for col in range(20):
            rect = pygame.Rect(col * 40, row * 40, 40, 40)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

