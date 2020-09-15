import pygame
from pygame import *
import brain
from brain import *
import bird
from bird import *
import random
import numpy as np

def nextGeneration(saved_bots, height, surface, colour):

    # print('\nNew generation')

    prev_pop_fitnesses = calculateFitness(saved_bots)

    p_mutation = 0.1
    size_mutation = 0.1

    # Pick new bots with higher probability based on fitness
    bots = []       # New bird
    children = []   # Old birds that brains are inherited from
    for bot in range(0, len(saved_bots)):

        new_bot = bird.Bird(height, surface, colour)
        children.append(pickOne(saved_bots, prev_pop_fitnesses))
        new_bot.brain = children[bot].brain
        bots.append(new_bot)

    # Children fitnesses
    new_pop_fitnesses = ([child.fitness for child in children])
    # print('Avg fitness old pop :', np.mean(prev_pop_fitnesses), 'Avg fitness new pop: ', np.mean(new_pop_fitnesses))

    # Mutate bots' brains
    for bot in bots:
        # print('Pre mutation: ', bot.brain.w)
        bot.brain.mutate(p_mutation, size_mutation)
        # print('Post mutation: ', bot.brain.w)

    return bots

def pickOne(list, prob):
    child = random.choices(list, prob)      # CHECK RANDOM CHOICES ARE GIVING MAINLY HIGH SCORING BIRDS !!!!!!!
    return child[0]                         # !!!!!!!!!!!

def calculateFitness(saved_bots):
    sum_scores = 0
    fitnesses = []
    for bot in saved_bots:
        sum_scores += bot.score
    for bot in saved_bots:
        bot.fitness = bot.score/sum_scores
        fitnesses.append(bot.fitness)
    return fitnesses
