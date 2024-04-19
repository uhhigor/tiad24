import random
import numpy as np

from scipy.special import gamma


def levy_flight(dim: int) -> np.ndarray:
    beta = 1.5
    sigma = (gamma(1 + beta) * np.sin(np.pi * beta / 2) /
             (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    u = np.random.normal(loc=0, scale=sigma, size=dim)
    v = np.random.normal(loc=0, scale=1, size=dim)
    step = u / abs(v) ** (1 / beta)
    return step


def init_population(function, dim: int, pop_size: int) -> list:
    butterflies = []
    for i in range(pop_size):
        sensory_modality = random.uniform(0, 1)
        stimulus = random.uniform(0, 1)
        power_exponent = 0.0

        butterflies.append(Butterfly(sensory_modality, stimulus, power_exponent, dim, function))

    return butterflies


def run_algorithm(dim: int, pop_size: int, iterations: int, function, prob: float, levy: bool = False):
    butterflies = init_population(function, dim, pop_size)

    best_index = 0
    best_solution = butterflies[best_index]
    best_solution_value = function(best_solution.position)

    for it in range(iterations):
        for i in range(pop_size):
            fragrance = butterflies[i].sensory_modality * pow(butterflies[i].stimulus, butterflies[i].power_exponent)
            r = random.uniform(0, 1)
            step = levy_flight(dim)
            for j in range(dim):
                if r < prob:
                    butterflies[i].position[j] += fragrance * (pow(r, 2) * best_solution.position[j]
                                                               - butterflies[i].position[j])
                else:
                    rand1 = random.uniform(0, pop_size - 1)
                    rand2 = random.uniform(0, pop_size - 1)
                    butterfly1 = butterflies[int(rand1)]
                    butterfly2 = butterflies[int(rand2)]
                    butterflies[i].position[j] += fragrance * (pow(r, 2) * butterfly1.position[j]
                                                               - butterfly2.position[j])
                    if levy:
                        butterflies[i].position[j] += step[j]

            butterflies[i].power_exponent = 0.1 + (0.2 * it / iterations)
            if function(butterflies[i].position) < function(best_solution.position):
                best_solution = butterflies[i]
                best_solution_value = function(butterflies[i].position)
                # print("New best solution: ", best_solution_value)

        # print("New best solution: ", best_solution.position, best_solution_value)

    return best_solution.position, best_solution_value


class Butterfly:
    def __init__(self, sensory_modality, stimulus, power_exponent, dim: int, function):
        self.sensory_modality = sensory_modality
        self.stimulus = stimulus
        self.power_exponent = power_exponent
        self.position = [random.uniform(function.x_min, function.x_max) for _ in range(dim)]

