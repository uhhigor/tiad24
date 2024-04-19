import random

from zad2.boa.butterfly import Butterfly
from zad2.function import Function


def init_population(function: Function, dim: int, pop_size: int) -> list:
    butterflies = []
    for i in range(pop_size):
        sensory_modality = random.uniform(0, 1)
        stimulus = random.uniform(0, 1)
        power_exponent = 0.0

        butterflies.append(Butterfly(sensory_modality, stimulus, power_exponent, dim, function))

    return butterflies


def run_algorithm2(dim: int, pop_size: int, iterations: int, function: Function, prob: float):
    butterflies = init_population(function, dim, pop_size)

    best_index = 0
    best_solution = butterflies[best_index]
    best_solution_value = function(best_solution.position)

    for it in range(iterations):
        for i in range(pop_size):
            fragrance = butterflies[i].sensory_modality * pow(butterflies[i].stimulus, butterflies[i].power_exponent)
            r = random.uniform(0, 1)
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

            butterflies[i].power_exponent = 0.1 + (0.2 * it / iterations)
            if function(butterflies[i].position) < function(best_solution.position):
                best_solution = butterflies[i]
                best_solution_value = function(butterflies[i].position)
                # print("New best solution: ", best_solution_value)

        #print("New best solution: ", best_solution.position, best_solution_value)

    return best_solution.position, best_solution_value
