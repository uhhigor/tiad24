import random

from zad2.bat.bat import Bat
from zad2.function import Function


class BatAlgorithm:
    def __init__(self, n, dim_number, f_min, f_max, alpha, gamma, fitness: Function):
        self.n = n
        self.dim_number = dim_number
        self.x_min = fitness.x_min
        self.x_max = fitness.x_max
        self.f_min = f_min
        self.f_max = f_max

        self.alpha = alpha
        self.gamma = gamma

        self.fitness = fitness

        self.population = self.init_population()

    def init_population(self) -> list:
        population = []
        for i in range(self.n):
            x = []
            v = []
            for j in range(self.dim_number):
                x.append(random.uniform(self.x_min, self.x_max))
                v.append(random.uniform(0, 1))
            population.append(Bat(x, v, self.f_min, self.f_max, self.alpha, self.gamma))
        return population

    def update_bat_fitness(self, bat: Bat):
        bat.fitness = self.fitness(bat.x)

    def update_fitness(self):
        for bat in self.population:
            self.update_bat_fitness(bat)

    def get_best(self) -> Bat:
        best_bat = self.population[0]
        for bat in self.population:
            if bat.fitness < best_bat.fitness:
                best_bat = bat
        return best_bat

    def avg_loudness(self):
        return sum([bat.loudness for bat in self.population]) / self.n

    def run(self, iterations: int) -> float:
        for it in range(iterations):
            best_bat = self.get_best()
            for bat in self.population:
                bat.update_position()
                bat.update_velocity(best_bat.x)
                if random.uniform(0, 1) < bat.emission:
                    for i in range(self.dim_number):
                        bat.x[i] = bat.x[i] + random.uniform(-1, 1) * self.avg_loudness()
                    self.update_bat_fitness(bat)
                if random.uniform(0, 1) < bat.emission:
                    bat.update_loudness()
                    bat.update_emission()
                self.update_bat_fitness(bat)
        return self.get_best().fitness
