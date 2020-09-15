import numpy as np
import math
# from sklearn.linear_model import LinearRegression
import random

class Brain:

    def __init__(self):
        self.X = np.empty([6, 1])                    # 5 by 1 (col)
        self.w = (np.random.rand(6) - 0.5) * 4       # 1 by 5 (row)
        self.output = None

        # Very good weights for gap size 250 (scored 110,000 on training run)!
        self.w = [0.72593628, 0.37446651, 0.15006522, -0.49957209, -0.04326722, -0.18375715]
        # Also very good also for 250 gap size
        # [0.72593628, 0.04545670477313318, 0.12927089355371196, -0.49957209, -0.08502709757797351, -0.20044314999476975]

    def think(self, observations):
        """
        :param observations: numpy array giving [y position of bird, top of gap, bottom of gap, x distance of pipe]
        :return: True if jump, False if not
        """

        self.X = observations                       # const, y position of bird, y velocity of bird, top of gap, bottom of gap, x distance of pipe
        self.output = self.sigmoid(np.dot(self.w, self.X))
        # print(np.dot(self.w, self.X))
        return self.output > 0.7

    def mutate(self, p_mutation, size_mutation):
        no_mutations = 0
        for i in range(0, len(self.w)):
            if random.random() < p_mutation:                                 # add the change
                # print('Old weight: ', self.w[i])
                change = np.random.normal(0, size_mutation)
                # print('Old weight: ', weight)
                self.w[i] += change
                # print('New weight: ', self.w[i])
                # print('New weight: ', weight)
                # if weight > 1:                                              # cap weights to -1 < w < 1
                #     weight = 1
                # if weight < -1:
                #     weight = -1
                no_mutations += 1
        # if no_mutations > 0:
            # print('Mutated ', no_mutations, ' times.')
        # print('No. mutations: ', no_mutations)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
