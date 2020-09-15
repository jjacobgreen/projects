import pygame, sys
from pygame.locals import *
import numpy as np
import math
import traceback
import random
import scipy
from scipy import ndimage

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
frame = 0

# Other Variables for use in the program
WIDTH = 600
HEIGHT = 600

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
# DISPLAYSURF.fill(0)
pygame.display.set_caption("Game")

# Set drop strength (really has to be 1 in order to avoid negative water height values that are complicated to
# interpolate to RGB)
strength = 1

# Height arrays
previous = np.zeros((WIDTH, HEIGHT))
current = np.zeros((WIDTH, HEIGHT))

# Initial drop
# previous[int(WIDTH / 2), int(HEIGHT / 2)] = strength

# Convolution kernel
kernel = np.array([[0, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0]])

# Damping - interaction between damping and max interpolation value (strength / 4) is important in setting ripple
# durations
damping = 0.99

# Game Loop
try:
    while True:

        # Create droplets at mouse positions
        mouse_pos = pygame.mouse.get_pos()
        previous[mouse_pos[0], mouse_pos[1]] = strength
        # Random droplets every 'rate' frames
        rate = 2
        if frame % rate == 0:
            previous[random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)] = strength

        # Convolve with kernel, then subtract the old value from the result and dampen
        current_convolved = scipy.ndimage.convolve(previous, kernel, cval=0.0)
        current = np.subtract(current_convolved, current)
        current *= damping
        # If under threshold, set to 0 (optional optimisation)
        current[current < strength / 1000] = 0

        # Create buffer array to display and expand to h x w x 3 with RGB grayscale values between 0 and 255
        current_display = current
        # (strength / 4) can change maximum brightness of pixels
        current_display = np.rint(np.interp(current_display, (0, strength / 4), (0, 255)))
        current_display = np.expand_dims(current_display, axis=-1) * np.array([1, 1, 1])

        # Blit display array to display surface
        print(current_display.shape)
        pygame.surfarray.blit_array(DISPLAYSURF, current_display)

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

        # Increase frame count
        frame += 1
# Unnecessary here, really, but good practice (?)
except Exception:
    print(traceback.print_exc())
