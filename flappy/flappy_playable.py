import pygame, sys
from pygame.locals import *

import brain
from brain import *

import bird
from bird import *
import pipe
from pipe import *

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
# BLUE = (0, 0, 255)
RED = (255, 0, 0)
# GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

# Create player
player = bird.Bird(SCREEN_HEIGHT, DISPLAYSURF, WHITE)

# Create pipe array
pipes = []
pipes.append(pipe.Pipe(SCREEN_HEIGHT, SCREEN_WIDTH, DISPLAYSURF, WHITE))

# Pipe spawner
pipe_delay = 2000  # 2 seconds
new_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(new_pipe, pipe_delay)

# Create brain
brain = brain.Brain()

# Sprite groups
# all_sprites = pygame.sprit

# Game Loop
while True:
    # Refresh background
    DISPLAYSURF.fill(BLACK)

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.up()
        if event.type == new_pipe:
            pipes.append(pipe.Pipe(SCREEN_HEIGHT, SCREEN_WIDTH, DISPLAYSURF, WHITE))
            # all_sprites.add(pipes[-1])

    player.update()
    player.show()

    for p in pipes:
        p.update()
        p.show()

        # Check if pipe hits bird
        if p.top_rect.colliderect(player.bird_rect) or p.bottom_rect.colliderect(player.bird_rect):
            p.colour = RED
        else:
            p.colour = WHITE
        if player.y == SCREEN_HEIGHT:
            DISPLAYSURF.fill(RED)
        if p.offscreen():
            # pipes.pop(pipes.index(p))
            pipes = [pipes[1]]

    pygame.display.flip()
    FramePerSec.tick(FPS)
