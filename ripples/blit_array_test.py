import pygame

import pygame, sys
from pygame.locals import *
import numpy as np
import math
import traceback
import time
import random
import scipy
from scipy import ndimage

# Initializing
pygame.init()

# Setting up FPS
FPS = 20
FramePerSec = pygame.time.Clock()
frame = 0

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
WIDTH = 800
HEIGHT = 800

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(0)
pygame.display.set_caption("Game")
img = pygame.Surface((WIDTH, HEIGHT))

# SETUP
# Set drop strength
strength = 250

# Arrays
previous = np.zeros((WIDTH, HEIGHT))
current = np.zeros((WIDTH, HEIGHT))


previous[int(WIDTH/2), int(HEIGHT/2)] = strength

# Convolution
kernel = np.array([[0, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0]])
# kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
# print(previous, '\n', current)

damping = 0.9

start = time.process_time()
C = -10

# Game Loop
try:
    while True:

        # Refresh background
        # DISPLAYSURF.fill(51)

        R, G, B = 255, 255, 255
        C -= 1

        current_display = np.ones((WIDTH, HEIGHT, 3), dtype=int) * C
        # print(current_display)
        pygame.surfarray.blit_array(DISPLAYSURF, current_display)

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


