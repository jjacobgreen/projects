import pygame

import pygame, sys
from pygame.locals import *
import numpy as np
import math
import traceback

# Initializing
pygame.init()

# Setting up FPS
FPS = 1
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
unit_colour = [1, 1, 1]

# Set up font
font = pygame.font.SysFont("Verdana", 20)

# Other Variables for use in the program
WIDTH = 180
HEIGHT = 180

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(0)
pygame.display.set_caption("Game")
# Create 1D pixel array
pixels = []
output = []


# SETUP
previous = [[0 for j in range(0, WIDTH)] for i in range(0, HEIGHT)]
current = previous
previous[int(WIDTH/2)][int(HEIGHT/2)] = 20

print(previous)

damping = 1


# Colour 1 pixel
# def colour_pixel(surface, colour, position):
#     colour = [colour] * 3
#     surface.fill(colour, (position, (1, 1)))


def map_to_grey(pixels):
    # Map value to between 0 and 1 then multiple by 255
    # small = abs(min(pixels))
    # big = abs(max(pixels))
    # return [math.floor(255 * (value + small) / (big + small)) for value in pixels]

    # small = abs(min(map(min, pixels)))
    # big = abs(max(map(max, pixels)))
    small = 0.5
    big = 0.5

    return [[math.floor(255 * (value + small) / (big + small)) for value in row] for row in pixels]

# def get_RGB_from_float:


# Game Loop
try:
    while True:

        # Refresh background
        # DISPLAYSURF.fill(BLACK)

        for i in range(1, HEIGHT - 1):
            for j in range(1, WIDTH - 1):
                # current[i][j] = ((previous[i - 1][j] +
                #                  previous[i + 1][j] +
                #                  previous[i][j + 1] +
                #                  previous[i][j - 1]) / 2 -
                #                  current[i][j])
                current[i][j] = (previous[i - 1][j] +
                                previous[i + 1][j] +
                                previous[i][j - 1] +
                                previous[i][j - 1] / 2) - current[i][j]
                # current[i][j] = current[i][j] * damping

        # Map to grey
        # pixels = map_to_grey(current)
        # # Display
        # for i in range(1, WIDTH - 1):
        #     for j in range(1, HEIGHT - 1):
        #         colour_pixel(DISPLAYSURF, pixels[i][j], [i, j])
        display_current = np.asarray(current, dtype=float)

        # print(display_current)
        pygame.surfarray.blit_array(DISPLAYSURF, display_current)

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

except Exception:
    print(traceback.print_exc())


