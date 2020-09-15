import pygame

import pygame, sys
from pygame.locals import *
import numpy as np
import math
import traceback
import time
import random

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
frame = 0

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
unit_colour = [1, 1, 1]

# Other Variables for use in the program
WIDTH = 100
HEIGHT = 100

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(0)
pygame.display.set_caption("Game")
img = pygame.Surface((WIDTH, HEIGHT))

# SETUP
previous = np.zeros((WIDTH, HEIGHT))

current = np.zeros((WIDTH, HEIGHT))


# print(previous, '\n', current)

damping = 0.99

start = time.process_time()

# Game Loop
try:
    while True:

        loop_start = time.process_time()

        # Droplets at mouse positions
        mouse_pos = pygame.mouse.get_pos()
        previous[mouse_pos[0], mouse_pos[1]] = 200
        # Random droplets
        if frame % 2 == 0:
            previous[random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)] = 500

        # Refresh background
        DISPLAYSURF.fill(BLACK)

        pixelArray = pygame.PixelArray(img)

        iter_start = time.process_time()
        for i in range(1, WIDTH - 1):
            for j in range(1, HEIGHT - 1):
                    current[i, j] = ((previous[i, j + 1] +
                                    previous[i, j - 1] +
                                    previous[i - 1, j] +
                                    previous[i + 1, j]) / 2
                                    - current[i, j])
                    current[i, j] *= damping
        # print('time since iter start: ', time.process_time() - loop_start)
                    val = min(255, max(0, round(current[i][j])))
                    pixelArray[i, j] = (val, val, val)
        pixelArray.close()
        DISPLAYSURF.blit(img, (0, 0))

        # pygame.surfarray.blit_array(DISPLAYSURF, current)

        # Swap buffers
        temp = current
        current = previous
        previous = temp

        # Apply all pixel updates
        pygame.display.flip()
        FramePerSec.tick(FPS)

        # Cycles through all occurring events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # print('time since loop start: ', time.process_time() - loop_start)

        frame += 1
except Exception:
    print(traceback.print_exc())


