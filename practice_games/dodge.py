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

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((600, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Block(pygame.sprite.Sprite):
    def __init__(self, color, spawn_x, spawn_y):
        super().__init__()

        self.image = pygame.Surface([40, 80])
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.block_speed = SPEED

    def move(self):
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
            self.block_speed = -self.block_speed
        self.rect.move_ip(0, self.block_speed)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([60, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(50, SCREEN_HEIGHT / 2))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Setting up Sprites
P1 = Player()
B1 = Block(BLACK, SCREEN_WIDTH/2, 80)
B2 = Block(BLACK, SCREEN_WIDTH/2, 400)

# Creating Sprites Groups
blocks = pygame.sprite.Group()
blocks.add(B1)
blocks.add(B2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(B1)
all_sprites.add(B2)

# Game Loop
while True:

    # Refresh background
    DISPLAYSURF.fill(WHITE)

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, blocks):
        pygame.quit()
        sys.exit()

    # for block in blocks:
    #     if pygame.sprite.spritecollideany(block, blocks):
    #         block.block_speed = -block.block_speed

    for block in blocks:
        if any(block.rect.colliderect(x.rect) for x in blocks if x is not block):
            block.block_speed = -block.block_speed


    pygame.display.update()
    FramePerSec.tick(FPS)