import pygame, sys
from pygame.locals import *
# import numpy as np
import math
# import traceback
# import time
import random
import cell

# Initializing
pygame.init()

# Setting up FPS
FPS = 30
FramePerSec = pygame.time.Clock()
frame = 0

# Other Variables for use in the program
WIDTH = 600
HEIGHT = 600

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(0)
pygame.display.set_caption("Game")

# SETUP
w = 20
cols = math.floor(WIDTH / w)
rows = math.floor(HEIGHT / w)
grid = []

# Create cells in rows and cols
for i in range(0, rows):
    for j in range(0, cols):
        grid.append(cell.Cell(i, j, w))

current_cell = grid[0]
stack = []


# FUNCTIONS
def remove_walls(a, b):
    x = a.j - b.j
    y = a.i - b.i

    if x == 1:
        a.walls[1] = False
        b.walls[3] = False
    if x == -1:
        a.walls[3] = False
        b.walls[1] = False
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    if y == -1:
        a.walls[2] = False
        b.walls[0] = False


# Game Loop
while True:

    # Refresh background
    DISPLAYSURF.fill((51, 51, 51))

    # Mark current_cell as current
    current_cell.current = True
    # Show cells
    for n in grid:
        n.show(DISPLAYSURF)
    current_cell.current = False

    # Mark current_cell as visited
    current_cell.visited = True
    # Get next to visit
    next_cell = current_cell.check_neighbours(grid, rows, cols)
    # If valid, make current and remove walls
    if next_cell is not None:
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif len(stack) > 0:
        current_cell = stack.pop()

    pygame.display.flip()
    FramePerSec.tick(FPS)

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
