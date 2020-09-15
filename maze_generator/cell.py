import pygame, sys
from pygame.locals import *
# import numpy as np
import math
# import traceback
# import time
import random

WHITE = (255, 255, 255)


# BLACK = (0, 0, 0)


class Cell:

    def __init__(self, i, j, w):
        self.i = i
        self.j = j
        self.w = w
        self.cell_rect = None
        self.walls = [True, True, True, True]
        self.visited = False
        self.current = False

    def show(self, surface):
        x = self.j * self.w
        y = self.i * self.w
        width = 1
        if self.visited:
            self.cell_rect = pygame.Rect(x, y, self.w, self.w)
            pygame.draw.rect(surface, (150, 0, 150), self.cell_rect)
        # Top
        if self.walls[0]:
            pygame.draw.line(surface, WHITE, (x, y), (x + self.w, y), width)
        # Left
        if self.walls[1]:
            pygame.draw.line(surface, WHITE, (x, y), (x, y + self.w), width)
        # Bottom
        if self.walls[2]:
            pygame.draw.line(surface, WHITE, (x, y + self.w), (x + self.w, y + self.w), width)
        # Right
        if self.walls[3]:
            pygame.draw.line(surface, WHITE, (x + self.w, y), (x + self.w, y + self.w), width)

        # Highlight if current
        if self.current:
            self.cell_rect = pygame.Rect(x + width, y + width, self.w - width, self.w - width)
            pygame.draw.rect(surface, (60, 120, 60), self.cell_rect)

    def check_neighbours(self, grid, rows, cols):
        neighbours = []
        top = None
        left = None
        bottom = None
        right = None

        # If the index is valid, assign the neighbouring cells
        if index(self.i, self.j - 1, rows, cols) is not None:
            top = grid[index(self.i, self.j - 1, rows, cols)]
        if index(self.i - 1, self.j, rows, cols) is not None:
            left = grid[index(self.i - 1, self.j, rows, cols)]
        if index(self.i, self.j + 1, rows, cols) is not None:
            bottom = grid[index(self.i, self.j + 1, rows, cols)]
        if index(self.i + 1, self.j, rows, cols) is not None:
            right = grid[index(self.i + 1, self.j, rows, cols)]

        # If neighbouring cells exist and haven't yet been visited, append them to neighbours
        if top is not None and not top.visited:
            neighbours.append(top)
        if left is not None and not left.visited:
            neighbours.append(left)
        if bottom is not None and not bottom.visited:
            neighbours.append(bottom)
        if right is not None and not right.visited:
            neighbours.append(right)

        if len(neighbours) > 0:
            return neighbours[random.randint(0, len(neighbours) - 1)]
        else:
            return None


def index(i, j, rows, cols):
    # If the index is within the bounds of the grid
    if i < 0 or i > rows - 1 or j < 0 or j > cols - 1:
        return None
    else:
        return j + i * rows
