# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
BORDER = 10

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height, spawn_x, spawn_y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(spawn_x, spawn_y))

class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_color, radius, spawn_x, spawn_y):
        super().__init__()
        self.color = ball_color
        self.radius = radius
        self.x = spawn_x
        self.y = spawn_y
        self.vx = -2
        self.vy = 3

        self.image = pygame.Surface([radius*2, radius*2])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.circle_rect = pygame.draw.circle(self.image, self.color, [self.rect.width/2, self.rect.height/2], self.radius)
        print(self.rect, self.rect.topleft)
        # self.ball = self.image.get_rect(center=(spawn_x, spawn_y))

    def move(self):
        # self.rect.move_ip(0, 0)
        # self.x = self.x + self.vx
        # self.y = self.y + self.vy
        self.rect.x = self.rect.x + self.vx
        self.rect.y = self.rect.y + self.vy
        # pygame.draw.circle(self.image, self.color, [self.rect.x, self.rect.y], self.radius)

class Player(pygame.sprite.Sprite):
    def __init__(self, length, width):
        super().__init__()
        self.image = pygame.Surface([width, length])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH - length, SCREEN_HEIGHT / 2))
        self.score = 0
        self.motion = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,5)
        self.motion = 0

        if self.rect.top > 0 + BORDER:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -SPEED)
                self.motion = 1
        if self.rect.bottom < SCREEN_HEIGHT - BORDER:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, SPEED)
                self.motion = 2

# Setting up Sprites
P1 = Player(60, 15)
WT = Wall(WHITE, SCREEN_WIDTH, BORDER, 0, 0)
WL = Wall(WHITE, BORDER, SCREEN_WIDTH, 0, 0)
WB = Wall(WHITE, SCREEN_WIDTH, BORDER, 0, SCREEN_HEIGHT - BORDER)
B1 = Ball(WHITE, 10, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# Creating Sprites Groups
walls = pygame.sprite.Group()
walls.add(WT)
walls.add(WL)
walls.add(WB)
# walls.add(WS)

moving_objects = pygame.sprite.Group()
moving_objects.add(P1)
moving_objects.add(B1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(WT)
all_sprites.add(WL)
all_sprites.add(WB)
all_sprites.add(B1)

# Game Loop
while True:

    # Refresh background
    DISPLAYSURF.fill(BLACK)

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        if entity in moving_objects:
            entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)


    # To be run if collision occurs between Player and Enemy
    # if pygame.sprite.spritecollideany(P1, walls):
    #     #     pygame.quit()
    #     #     sys.exit()

    # for block in walls:
    #     if pygame.sprite.spritecollideany(block, walls):
    #         block.block_speed = -block.block_speed

    # for block in walls:
    #     if any(block.rect.colliderect(x.rect) for x in walls if x is not block):
    #         block.block_speed = -block.block_speed
    for wall in walls:
        if wall.rect.colliderect(B1.rect):
            if wall == WB or wall == WT:
                B1.vy = -B1.vy
            else:
                B1.vx = -B1.vx

    if P1.rect.colliderect(B1.rect):
        P1.score += 1
        if P1.motion == 0:
            B1.vx = -B1.vx
        if P1.motion == 1:
            B1.vx = -B1.vx
            B1.vy = B1.vy - 2
        if P1.motion == 2:
            B1.vx = -B1.vx
            B1.vy = B1.vy + 2

    if B1.rect.left > SCREEN_WIDTH:
        final_score = font.render("FINAL SCORE: " + str(P1.score), True, BLACK)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (300, 300))
        DISPLAYSURF.blit(final_score, (300, 400))

        pygame.display.update()
        # for entity in all_sprites:
        #     entity.kill()
        time.sleep(1.5)

    # SHOW SCORE
    font = pygame.font.Font(None, 50)
    text = font.render('SCORE: ' + str(P1.score), 1, WHITE)
    DISPLAYSURF.blit(text, (20, 20))

    pygame.display.flip()
    FramePerSec.tick(FPS)