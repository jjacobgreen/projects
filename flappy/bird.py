import pygame
from pygame import *
import brain
from brain import *


class Bird:

    def __init__(self, height, surface, colour):
        super().__init__()
        self.y = height/2
        self.x = 100
        self.height = height
        self.surface = surface
        self.colour = colour
        self.flap_power = 12

        self.velocity = 0
        self.gravity = 1

        self.image = pygame.image.load("images/fish.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.image.set_alpha(128)
        self.bird_rect = self.image.get_rect()

        self.brain = brain.Brain()
        self.score = 0
        self.fitness = 0

    def show(self):
        # self.bird_rect = pygame.draw.circle(self.surface, self.colour, [int(self.x), int(self.y)], 16)
        self.surface.blit(self.image, self.bird_rect)

    def update(self):
        # Update velocity and position
        self.velocity += self.gravity
        self.y += self.velocity
        self.bird_rect.center = (self.x, self.y)

        # Increase score
        self.score += 1

        # Prevent going off screen
        if self.y > self.height:
            self.y = self.height
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity = -self.flap_power

    def get_closest_pipe(self, pipes):
        current_closest_distance = float('inf')
        current_closest_pipe = None
        for p in pipes:
            if - p.width < p.x - self.x < current_closest_distance:         # if not behind bird and newest smallest
                current_closest_distance = p.x - self.x
                current_closest_pipe = p
        return current_closest_pipe
