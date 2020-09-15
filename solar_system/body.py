import pygame, sys
from pygame.locals import *
import numpy as np
import math
# import traceback
# import time
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
G = 10


class Body:

    def __init__(self, x, y, v_x, v_y, radius, mass, fixed, colour, image, name):
        # self.r = r
        # self.theta = theta
        self.x = x
        self.y = -y
        self.radius = radius
        self.mass = mass

        # self.f_mag = 0
        self.f_x = 0
        self.f_y = 0

        self.omega = 0
        self.r_dot = 0

        self.v_x = v_x
        self.v_y = -v_y

        self.mv_x = mass * v_x
        self.mv_y = mass * v_y

        self.fixed = fixed
        self.history = []

        self.collided = False
        self.collided_body = None
        self.collision_offset = []

        self.colour = colour
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.original_image = self.image
        self.image_rect = self.image.get_rect()
        self.rotation = 0
        self.name = name

    def apply_gravity(self, bodies):
        f_mag = 0
        self.f_x = 0
        self.f_y = 0
        for b in bodies:
            if b != self:
                d = dist(self, b)
                # print('comparing, ', self.name, ' to ', b.name)
                f_mag = -G * self.mass * b.mass / (d ** 2)
                if self.x - b.x == 0:
                    co_angle = math.pi / 2
                else:
                    co_angle = math.atan2((self.y - b.y), (self.x - b.x))

                self.f_x += f_mag * math.cos(co_angle)
                self.f_y += f_mag * math.sin(co_angle)

    def force2acc(self, force):
        # TODO: Add direction
        return force / self.mass

    def update(self, bodies):
        # Get acceleration
        a_x = self.force2acc(self.f_x)
        a_y = self.force2acc(self.f_y)

        # Change velocities
        self.v_x += a_x
        self.v_y += a_y

        # Change positions
        if not self.fixed:
            self.x += self.v_x
            self.y += self.v_y

        # Find any bodies it has collided with
        if not self.collided:
            collided_body = self.check_collisions(bodies)
        # If it has collided this frame with a body of greater mass, set its collided flag to True
        if not self.collided:
            if collided_body is not None and collided_body.mass > self.mass:
                self.collided = True
                self.collided_body = collided_body
                self.coalesce(self.collided_body)
                self.collision_offset = [self.x - self.collided_body.x, self.y - self.collided_body.y]

        # If it has collided, coalesce it to its collidee
        if self.collided:
            self.stick(self.collided_body)

    def show(self, surface):
        # pygame.draw.circle(surface, self.colour,
        #                    to_centre([self.x, self.y], surface.get_width(), surface.get_height()),
        #                    # (self.x, self.y),
        #                    self.radius)

        self.image_rect.center = (to_centre((self.x, self.y), surface.get_width(), surface.get_height()))
        # self.image = pygame.transform.rotate(self.original_image, self.rotation)
        surface.blit(self.image, self.image_rect)
        # self.rotation += 1

    def show_path(self, surface, length):
        # If the body is allowed to move
        if not self.fixed:
            self.history.append([self.x, self.y])
        # Only record 'length' past locations
        if len(self.history) > length:
            self.history.pop(0)
        for point in self.history:
            pygame.draw.circle(surface, self.colour,
                               to_centre([point[0], point[1]], surface.get_width(), surface.get_height()),
                               # (self.x, self.y),
                               1)

    def check_collisions(self, bodies):
        for b in bodies:
            if b != self:
                if dist(self, b) < self.radius + b.radius:
                    return b

    def coalesce(self, body):
        body.v_x = (self.mass * self.v_x + body.mass * body.v_x) / (self.mass + body.mass)
        body.v_y = (self.mass * self.v_y + body.mass * body.v_y) / (self.mass + body.mass)

        self.v_x = body.v_x
        self.v_y = body.v_y

        body.mass += self.mass
        self.mass = 0.0001

    def stick(self, body):
        self.x = body.x + self.collision_offset[0]
        self.y = body.y + self.collision_offset[1]

    def __eq__(self, other):
        if not isinstance(other, Body):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.radius == other.radius and self.mass == other.mass

    def __ne__(self, other):
        if not isinstance(other, Body):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return not (self.x == other.x and self.y == other.y and self.radius == other.radius and self.mass == other.mass)


# Convert (x, y) to (r, theta)
def cart2pol(x, y):
    r = x ** 2 + y ** 2
    theta = math.atan2(y / x)
    return np.array([r, theta])


# Convert (r, theta) to (x, y)
def pol2cart(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return np.array([x, y])


# Get distance between two bodies
def dist(b1, b2):
    return math.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)


# Move cartesian coordinates to centre of window
def to_centre(pos_cart, width, height):
    x = pos_cart[0] + width / 2
    y = pos_cart[1] + height / 2
    return np.array([x, y])
