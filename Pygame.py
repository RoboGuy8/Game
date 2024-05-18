import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Colors
BG = (150, 150, 150)
RED = (50, 50, 50)

# Dictionary to store the boxes with additional attributes
boxes = {}

# Load the texture image
texture = pygame.image.load('texture.png')
texture = pygame.transform.scale(texture, (45, 45))

# Populate the boxes dictionary
box_id = 0
for y in range(0, 720, 45):
    for x in range(0, 1080, 45):
        rect = pygame.Rect(x, y, 45, 45)
        color = (255, 255, 255)  # Default color (white)
        boxes[box_id] = {'rect': rect, 'color': color}
        box_id += 1

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PvP Shooter')

clock = pygame.time.Clock()
FPS = 60
gravity = 0.7

# Load bullet image
bullet_image = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_image, (int(bullet_image.get_width() * 0.05), int(bullet_image.get_height() * 0.05)))

def draw_bg():
    screen.fill(BG)
    pygame.draw.rect(screen, RED, (0, 560, SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self, type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.type = type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        img = pygame.image.load(f"soldier{type}.png").convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        death_img = pygame.image.load(f"soldier_dead{type}.png").convert_alpha()
        self.death_image = pygame.transform.scale(death_img, (int(death_img.get_width() * scale), int(death_img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.moving_left = False
        self.moving_right = False
        self.shoot = False
        self.shoot_cooldown = 0
        self.health = 5

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump:  # Adjusted condition for jump
            self.vel_y = -15
            self.jump = False

        if self.jump == True:
            self.vel_y = -15
            self.jump = False

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 675 + 40:
            dy = 675 + 40 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 15
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(player_1, bullet_group, False):
            if player_1.alive:
                player_1.health -= 1
                self.kill()
        if pygame.sprite.spritecollide(player_2, bullet_group, False):
            if player_2.alive:
                player_2.health -= 1
                self.kill()

# Create groups
bullet_group = pygame.sprite.Group()

# Create players
player_1 = Player(1, 600, 600, 0.10, 10)
player_2 = Player(2, 400, 200, 0.10, 10)

# Main game loop
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    
    # Draw the texture on the last row of boxes
    for box_id, box_info in boxes.items():
        if box_info['rect'].y == 675:  # Last row y-coordinate
            screen.blit(texture, box_info['rect'].topleft)
        else:
            pygame.draw.rect(screen, box_info['color'], box_info['rect'])
    
    # Draw the players
    player_1.draw()
    player_2.draw()

    # Update and draw the bullets
    bullet_group.update()
    bullet_group.draw(screen)

    player_1.move(player_1.moving_left, player_1.moving_right)
    player_2.move(player_2.moving_left, player_2.moving_right)

    if player_1.alive:
        if player_1.shoot:
            if player_1.shoot_cooldown == 0:
                player_1.shoot_cooldown = 25
                bullet = Bullet(player_1.rect.centerx + (player_1.rect.size[0] * 0.9 * player_1.direction), player_1.rect.centery, player_1.direction)
                bullet_group.add(bullet)
        if player_1.shoot_cooldown > 0:
            player_1.shoot_cooldown -= 1
    if player_1.alive == False:
        player_1.image = player_1.death_image
    if player_2.alive:
        if player_2.shoot:
            if player_2.shoot_cooldown == 0:
                player_2.shoot_cooldown = 25
                bullet = Bullet(player_2.rect.centerx + (player_2.rect.size[0] * 0.9 * player_2.direction), player_2.rect.centery, player_2.direction)
                bullet_group.add(bullet)
        if player_2.shoot_cooldown > 0:
            player_2.shoot_cooldown -= 1
    if player_2.alive == False:
        player_2.image = player_2.death_image

    player_1.check_alive()
    player_2.check_alive()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN and player_1.alive:
            if event.key == pygame.K_a:
                player_1.moving_left = True
            if event.key == pygame.K_d:
                player_1.moving_right = True
            if event.key == pygame.K_w and player_1.vel_y > 12:
                player_1.jump = True
            if event.key == pygame.K_q:
                player_1.shoot = True
        if event.type == pygame.KEYDOWN and player_2.alive:
            if event.key == pygame.K_j:
                player_2.moving_left = True
            if event.key == pygame.K_l:
                player_2.moving_right = True
            if event.key == pygame.K_i and player_2.vel_y > 12:
                player_2.jump = True
            if event.key == pygame.K_p:
                player_2.shoot = True
        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_1.moving_left = False
            if event.key == pygame.K_d:
                player_1.moving_right = False
            if event.key == pygame.K_w:
                player_1.jump = False
            if event.key == pygame.K_q:
                player_1.shoot = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                player_2.moving_left = False
            if event.key == pygame.K_l:
                player_2.moving_right = False
            if event.key == pygame.K_i:
                player_2.jump = False
            if event.key == pygame.K_p:
                player_2.shoot = False

    pygame.display.update()
pygame.quit()
