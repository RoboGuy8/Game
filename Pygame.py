import pygame
import csv


# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

ROWS = 16
COLUMS = 150

# Colors
BG = (150, 150, 150)
RED = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PvP Shooter')

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.55
TILE_SIZE = SCREEN_HEIGHT // ROWS

# Load bullet image
bullet_image = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_image, (int(bullet_image.get_width() * 0.05), int(bullet_image.get_height() * 0.05)))
texture_img = pygame.image.load('bricks.jpg')
texture_img = pygame.transform.scale(texture_img, (TILE_SIZE,TILE_SIZE))
background_image = pygame.image.load('background.jpg').convert_alpha()
background_img = pygame.transform.scale(background_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
fog_image = pygame.image.load('fog.png').convert_alpha()
fog_img = pygame.transform.scale(fog_image, (SCREEN_WIDTH,200))
fog_up = pygame.transform.flip(fog_img, False, True)
fog_left = pygame.transform.rotate(fog_img, 90)
fog_right = pygame.transform.rotate(fog_img, -90)
font = pygame.font.SysFont('Futura',30)

def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(img,(x,y))

def draw_bg():

    screen.blit(background_img, (0, 0))

    #gridline

    #for x in range(0, SCREEN_WIDTH, 45):
    #    pygame.draw.line(screen, (200,200,200), (x, 0), (x, SCREEN_HEIGHT))
    #for y in range(0, SCREEN_HEIGHT, 45):
    #    pygame.draw.line(screen, (200,200,200), (0, y), (SCREEN_WIDTH, y))

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
        self.in_air = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        # Move left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump and not self.in_air:
            self.vel_y = -13
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check for collision
        self.in_air = True
        for tile in world.obstacle_list:
            # Check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # Check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy + GRAVITY, self.width, self.height):
            # Check if the player is above the ground (falling)
                if self.vel_y > 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                # Check if the player is jumping (moving upwards)
                elif self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.y > 720:
            self.rect.y = 0



    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        #hitboxes

        #pygame.draw.rect(screen,(255,0,0),self.rect,1)

class World():
    def __init__(self):
        self.obstacle_list = []
    def process_data(self,data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile == 4:
                    img = texture_img
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img,img_rect)
                    self.obstacle_list.append(tile_data)
                elif tile != 4:
                    pass               
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0],tile[1])


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

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
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
player_1 = Player(1, 70, 350, 0.075, 4)
player_2 = Player(2, 1000, 350, 0.075, 4)

world_data = []
for row in range(ROWS):
	r = [-1] * COLUMS
	world_data.append(r)
#load in level data and create world
with open('map.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
world.process_data(world_data)



# Main game loop
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    world.draw()
    
    draw_text(f'GREEN HEALTH: {player_1.health}', font,(255,255,255),10,10)
    draw_text(f'BLUE HEALTH: {player_2.health}', font,(255,255,255),900,10)   
    # Draw the players
    player_1.update()
    player_2.update()


    # Update and draw the bullets
    bullet_group.update()
    bullet_group.draw(screen)
    player_1.draw()
    player_2.draw()
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

    screen.blit(fog_img, (0, 590))
    screen.blit(fog_up, (0, -75))
    screen.blit(fog_left, (950, 0))
    screen.blit(fog_right, (-75, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN and player_1.alive:
            if event.key == pygame.K_a:
                player_1.moving_left = True
            if event.key == pygame.K_d:
                player_1.moving_right = True
            if event.key == pygame.K_w:
                player_1.jump = True
            if event.key == pygame.K_SPACE:
                player_1.shoot = True
        if event.type == pygame.KEYDOWN and player_2.alive:
            if event.key == pygame.K_j:
                player_2.moving_left = True
            if event.key == pygame.K_l:
                player_2.moving_right = True
            if event.key == pygame.K_i:
                player_2.jump = True
            if event.key == pygame.K_RETURN:
                player_2.shoot = True
        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_1.moving_left = False
            if event.key == pygame.K_d:
                player_1.moving_right = False
            if event.key == pygame.K_w:
                player_1.jump = False
            if event.key == pygame.K_SPACE:
                player_1.shoot = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                player_2.moving_left = False
            if event.key == pygame.K_l:
                player_2.moving_right = False
            if event.key == pygame.K_i:
                player_2.jump = False
            if event.key == pygame.K_RETURN:
                player_2.shoot = False

    pygame.display.update()
pygame.quit()


   

