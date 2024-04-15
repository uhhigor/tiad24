import math
import random


class Bat:
    def __init__(self, x: list, v: list, f_min: float, f_max: float, alpha: float, gamma: float):
        self.x = x
        self.v = v
        self.f_min = f_min
        self.f_max = f_max
        self.frequency = 0
        self.fitness = float('inf')

        self.loudness = random.uniform(1, 2)  # A
        self.emission_0 = random.uniform(0, 1)  # r_0
        self.emission = self.emission_0  # r
        self.alpha = alpha
        self.gamma = gamma

        self.update_frequency()

    def update_frequency(self):
        self.frequency = self.f_min + (self.f_max - self.f_min) * random.uniform(0, 1)

    def update_velocity(self, best_x: list):
        for i in range(len(self.x)):
            self.v[i] += (best_x[i] - self.x[i]) * self.frequency

    def update_position(self):
        for i in range(len(self.x)):
            self.x[i] += self.v[i]

    def update_loudness(self):
        self.loudness *= self.alpha

    def update_emission(self):
        self.emission = self.emission_0 * (1 - math.exp(-self.gamma))

