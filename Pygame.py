import pygame

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('PvP shooter')

clock = pygame.time.Clock()
FPS = 60

gravity = 0.75

moving_right1 = False
moving_left1 = False
moving_right2 = False
moving_left2 = False

alive = True

BG = (144,201,120)
RED = (200,100,200)

def draw_bg():
    screen.fill(BG)
    pygame.draw.rect(screen,RED,(0, 540, SCREEN_WIDTH, SCREEN_HEIGHT))

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
        img = pygame.image.load(f"Soldier{type}.png")
        self.image = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

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
        if self.jump == True:
            self.vel_y = -11
            self.jump = False

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player_1 = Player(1,600,600,0.15,10)
player_2 = Player(2,400,200,0.15,10)


run = True
while run:          
    clock.tick(FPS)

    draw_bg()

    player_1.draw()
    player_2.draw()

    player_1.move(moving_left1,moving_right1)
    player_2.move(moving_left2,moving_right2)



    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left1 = True
            if event.key == pygame.K_d:
                moving_right1 = True
            if event.key == pygame.K_w and player_1.alive:
                player_1.jump = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                moving_left2 = True
            if event.key == pygame.K_l:
                moving_right2 = True
            if event.key == pygame.K_i:
                player_2.jump = True
        #keayboard realeased
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left1 = False
            if event.key == pygame.K_d:
                moving_right1 = False
            if event.key == pygame.K_w:
                player_1.jump = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j: 
                moving_left2 = False
            if event.key == pygame.K_l:
                moving_right2 = False
            if event.key == pygame.K_i:
                player_2.jump = False

    pygame.display.update()
pygame.quit()