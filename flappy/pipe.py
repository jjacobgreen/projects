import pygame
from pygame import *
import random


class Pipe:

    def __init__(self, height, width, surface, colour):
        super().__init__()
        self.gap = 250
        self.gap_y = random.randint(0, height-self.gap)
        self.width = 40
        self.speed = 3

        self.height = height
        self.colour = colour
        self.x = width
        self.surface = surface

        self.top_rect = None
        self.bottom_rect = None
        # Seaweed
        # self.image_top = pygame.image.load("images/seaweed.png")
        # self.image_top = pygame.transform.rotozoom(self.image_top, 180, 0.5)
        # self.image_bottom = pygame.image.load("images/seaweed.png")
        # self.image_bottom = pygame.transform.rotozoom(self.image_bottom, 0, 0.5)

    def show(self):
        pygame.draw.rect(self.surface, self.colour, self.top_rect)
        pygame.draw.rect(self.surface, self.colour, self.bottom_rect)
        # Seaweed
        # self.surface.blit(self.image_top, self.top_rect)
        # self.surface.blit(self.image_bottom, self.bottom_rect)

    def update(self):
        self.x -= self.speed
        self.top_rect = Rect(self.x, 0, self.width, self.gap_y)
        self.bottom_rect = Rect(self.x, self.gap + self.gap_y, self.width, self.height - self.gap_y - self.gap)

    def offscreen(self):
        return self.x < -self.width

