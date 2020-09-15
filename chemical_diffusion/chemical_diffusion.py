import pygame, sys
from pygame.locals import *
import numpy as np
import math
import traceback
import random
import scipy
from scipy import ndimage
import time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
frame = 0

# Other Variables for use in the program
WIDTH = 200
HEIGHT = 200

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# 2D grid arrays each containing a dict

current_display = np.zeros((WIDTH, HEIGHT, 3))

current_a = np.ones((WIDTH, HEIGHT))
current_b = np.zeros((WIDTH, HEIGHT))

patch = 40
current_b[math.floor(WIDTH / 2) - patch:math.floor(WIDTH / 2) + patch,
          math.floor(HEIGHT / 2) - patch:math.floor(HEIGHT / 2) + patch] = 1

current_b[math.floor(WIDTH / 4) - patch:math.floor(WIDTH / 4) + patch,
          math.floor(HEIGHT / 4) - patch:math.floor(HEIGHT / 4) + patch] = 1

current_b[math.floor(3*WIDTH / 4) - patch:math.floor(3*WIDTH / 4) + patch,
          math.floor(3*HEIGHT / 4) - patch:math.floor(3*HEIGHT / 4) + patch] = 1

next_a = np.zeros((WIDTH, HEIGHT))
next_b = np.zeros((WIDTH, HEIGHT))

# Convolution kernel
kernel = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])

# Parameters
dA = 1
dB = 0.5
# feed = 0.0367
# k = 0.0649
feed = 0.055
k = 0.062

def laplace(input):
    return scipy.ndimage.convolve(input, kernel, cval=0.0)

# Game Loop
while True:

    t0 = time.time()
    # Update array
    # for i in range(0, ):
    next_a = np.add(
                np.add(
                    np.add(current_a, dA * laplace(current_a)),
                - (np.multiply(current_a, np.square(current_b)))),
             (feed * (1 - current_a)))
    next_b = np.add(
                np.add(
                    np.add(current_b, dB * laplace(current_b)),
                np.multiply(current_a, np.square(current_b))),
             - (k + feed) * current_b)
    # Swap buffers
    temp_a = current_a
    temp_b = current_b

    current_a = next_a
    current_b = next_b

    next_a = temp_a
    next_b = temp_b

    # Create pixel array
    # current_display = np.stack((np.floor(current_a * 255), np.floor(np.ones((WIDTH, HEIGHT))), np.floor(current_b) * 255), axis=2)
    # G = np.floor(np.add(current_a, current_b) / 2 * 255)
    # current_display = np.stack((np.floor(current_a * 255), G, np.floor(current_b) * 255), axis=2)
    c = np.floor(np.subtract(current_a, current_b) * 255)
    current_display = np.stack((c, c, c), axis=2)
    current_display = np.clip(current_display, 0, 255)

    # Blit pixel array to display surface
    pygame.surfarray.blit_array(DISPLAYSURF, current_display)
    t1 = time.time()
    # print(t1-t0)

    # Apply all pixel updates
    pygame.display.flip()
    FramePerSec.tick(FPS)

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Increase frame count
    frame += 1