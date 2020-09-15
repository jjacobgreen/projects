import pygame, sys
from pygame.locals import *
import bird
import pipe
import ga
import numpy as np
import math
import traceback

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
# BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up font
font = pygame.font.SysFont("Verdana", 20)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Create a black screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

# Create bots, each with a randomly initialised brain
bots = []
saved_bots = []
for bot in range(0, 300):
    bots.append(bird.Bird(SCREEN_HEIGHT, DISPLAYSURF, WHITE))

# Create pipe array
pipes = []

# Pipe spawner (every x frames)
frame_no = 0
spawn_rate = 90
frame_skip = 1

# Generation setup
generation = 1
avg_score = 0
past_gen_scores = []

# Keep track of best performing none
best_bot = None
best_score = 0
show_best = False
train_or_best = "TRAINING"

# Game Loop
try:
    while True:

        for i in range(0, frame_skip):
        # Cycles through all occurring events
            for event in pygame.event.get():
                if event.type == QUIT:
                    print('Best weights: ', best_bot.brain.w)
                    for bot in bots:
                        print('Current weights: ', bot.brain.w)
                    pygame.quit()
                    sys.exit()
                # Frame skipper
                #     if event.key == pygame.K_UP and frame_skip <= 90:
                #         frame_skip += 10
                #     if event.key == pygame.K_DOWN and frame_skip >= 10:
                #         frame_skip -= 10
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        show_best = not show_best

            # Frame skipper set
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP] and frame_skip < 100:
                frame_skip += 1
            if pressed_keys[K_DOWN] and frame_skip > 1:
                frame_skip -= 1

            # Pipe spawner
            if frame_no % spawn_rate == 0:
                pipes.append(pipe.Pipe(SCREEN_HEIGHT, SCREEN_WIDTH, DISPLAYSURF, WHITE))
            # Frame counter
            frame_no += 1

            # Get closest pipe
            if len(bots) > 0:
                closest_pipe = bots[0].get_closest_pipe(pipes)
                # closest_pipe.colour = GREEN

            for p in pipes:
                p.update()

                # Check if pipe hits bird
                for bot in bots:
                    if p.top_rect.colliderect(bot.bird_rect) or p.bottom_rect.colliderect(bot.bird_rect) or bot.y == SCREEN_HEIGHT:
                        if not show_best:
                            saved_bots.append(bots.pop(bots.index(bot)))
                        else:
                            bots = [bird.Bird(SCREEN_HEIGHT, DISPLAYSURF, WHITE)]
                            bots[0].brain = best_bot.brain
                            pipes.clear()
                            frame_no = 0

                if p.offscreen():
                    pipes.pop(pipes.index(p))
                    # pipes = [pipes[1:-1]]

            for bot in bots:
                observations = np.array(np.array([1, bot.y/SCREEN_HEIGHT, bot.velocity / 10, closest_pipe.gap_y/SCREEN_HEIGHT, (closest_pipe.gap + closest_pipe.gap_y)/SCREEN_HEIGHT, closest_pipe.x/SCREEN_WIDTH]))
                if bot.brain.think(observations):
                    bot.up()
                bot.update()


            # When all bots die
            if len(bots) == 0 and not show_best:
                # Array of all scores this generation
                all_scores = [bot.score for bot in saved_bots]
                avg_score = math.floor(sum(all_scores)/len(all_scores))
                # Historical avg scores
                past_gen_scores.append(avg_score)
                # Store best ever score
                if max(all_scores) > best_score:
                    best_score = max(all_scores)
                    best_bot = saved_bots[all_scores.index(best_score)]
                # print(past_gen_scores)

                # Set up new generation
                bots = ga.nextGeneration(saved_bots, SCREEN_HEIGHT, DISPLAYSURF, WHITE)
                saved_bots.clear()
                pipes.clear()
                frame_no = 0
                generation += 1
                train_or_best = "TRAINING"
            # If show best is on, create a new bird with the best bird's brain and reset
            elif show_best and generation > 1:
                saved_bots = [bot for bot in saved_bots] + [bot for bot in bots]
                bots = [bird.Bird(SCREEN_HEIGHT, DISPLAYSURF, WHITE)]
                # Append all alive bots to saved bots
                bots[0].brain = best_bot.brain
                pipes.clear()
                frame_no = 0
                generation = 0
                train_or_best = "BEST"
                print('Saved no.: ', len(saved_bots))


        # Drawing
        # Refresh background
        DISPLAYSURF.fill(BLACK)

        for p in pipes:
            p.show()
        for bot in bots:
            bot.show()

        # Display generation no.
        gen = font.render('Generation ' + str(generation), 1, RED)
        DISPLAYSURF.blit(gen, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40))

        fishies = font.render('Fishies left: ' + str(len(bots)), 1, RED)
        DISPLAYSURF.blit(fishies, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 20))

        current_score = font.render('Score: ' + str(bots[0].score), 1, RED)
        DISPLAYSURF.blit(current_score, (10, SCREEN_HEIGHT - 20))

        top_score = font.render('Best score: ' + str(best_score), 1, RED)
        DISPLAYSURF.blit(top_score, (10, SCREEN_HEIGHT - 40))

        status = font.render(train_or_best, 1, RED)
        DISPLAYSURF.blit(status, (SCREEN_WIDTH/2 - 40, 40))

        pygame.display.flip()
        FramePerSec.tick(FPS)

except Exception:
    print(traceback.print_exc())
    if best_bot is not None:
        print('Best bot weights: ', best_bot.brain.w)
    else:
        print('No best bot defined.')
