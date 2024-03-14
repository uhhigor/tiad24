import math
import random


class Particle:
    def __init__(self, x: list, inertion_factor, cognitive_const, social_const, x_min, x_max):
        self.x = x
        self.best_x = x
        self.x_min = x_min
        self.x_max = x_max
        self.fitness = float('inf')
        self.best_fitness = float('inf')
        self.inertion_factor = inertion_factor
        self.cognitive_const = cognitive_const
        self.social_const = social_const

        self.velocity = [0] * len(x)

    def cognitive_acc(self):
        return self.cognitive_const * random.Random().uniform(0, 1)

    def social_acc(self):
        return self.social_const * random.Random().uniform(0, 1)

    def distance(self):
        return math.sqrt(sum((xi - yi) ** 2 for xi, yi in zip(self.best_x, self.x)))

    def update_particle(self, best_particle):
        cognitive_acc = self.cognitive_acc()
        cognitive_velocity = [cognitive_acc * (best_xi - xi) for best_xi, xi in zip(self.best_x, self.x)]

        social_acc = self.social_acc()
        social_velocity = [social_acc * (best_xi - xi) for best_xi, xi in zip(best_particle.x, self.x)]

        inertion = [self.inertion_factor * vi for vi in self.velocity]

        self.velocity = [inertion[i] + cognitive_velocity[i] + social_velocity[i] for i in range(len(self.x))]
        self.x = [xi + self.velocity[i] for i, xi in enumerate(self.x)]

        for i in range(len(self.x)):
            if self.x[i] < self.x_min:
                self.x[i] = self.x_min
            elif self.x[i] > self.x_max:
                self.x[i] = self.x_max
