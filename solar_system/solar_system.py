import pygame, sys
from pygame.locals import *
# import numpy as np
import math
# import traceback
# import time
import random
import body

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
frame = 0

# Creating colors
EARTH_BLUE = (36, 160, 255)
MARS_RED = (200, 50, 0)
SUN_YELLOW = (255, 219, 36)
STAR_WHITE = (255, 255, 220)
# GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
WIDTH = 800
HEIGHT = 800

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(0)
pygame.display.set_caption("Game")

# SETUP
# Images
sun_image = pygame.image.load('images/sun.png')
earth_image = pygame.image.load('images/earth.png')
mars_image = pygame.image.load('images/mars.png')

# x, y, v_x, v_y, radius, mass, fixed, colour
sun = body.Body(0, 0, 0, 0, 40, 100, False, SUN_YELLOW, sun_image, 'sun')
earth = body.Body(100, 100, -2, 2, 20, 2, False, EARTH_BLUE, earth_image, 'earth')
# mars = body.Body(200, -200, 1, 1, 10, 0.5, False, MARS_RED, mars_image)
mars = body.Body(200, 200, -1, 1, 10, 1.5, False, MARS_RED, mars_image, 'mars')

# List of bodies
bodies = [sun, earth, mars]


def generate_star_locations(n):
    locations = []
    for i in range(0, n):
        locations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    return locations


def show_stars(surface, star_locations):
    for star in star_locations:
        pygame.draw.circle(surface, STAR_WHITE, star, 1)


def dist(b1, b2):
    return math.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)


stars = generate_star_locations(500)

# Game Loop
while True:

    # Refresh background
    DISPLAYSURF.fill(BLACK)
    show_stars(DISPLAYSURF, stars)

    for body in bodies:
        body.apply_gravity(bodies)
        # print(body.name)
        body.update(bodies)
        body.show_path(DISPLAYSURF, 500)
        body.show(DISPLAYSURF)

    # print(dist(earth, mars))
    # Apply all pixel updates
    pygame.display.flip()
    FramePerSec.tick(FPS)

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
