import math
import random

from zad2.function import Function


def init_population(function: Function, dim: int, pop_size: int) -> tuple:
    positions = []
    velocities = []
    frequencies = []
    pulse_rates = []
    loudness = []
    for i in range(pop_size):
        position = [random.uniform(function.x_min, function.x_max) for _ in range(dim)]
        velocity = [0 for _ in range(dim)]
        frequency = 0
        pulse_rate = 1
        loud = 2

        positions.append(position)
        velocities.append(velocity)
        frequencies.append(frequency)
        pulse_rates.append(pulse_rate)
        loudness.append(loud)
    return positions, velocities, frequencies, pulse_rates, loudness


def run_algorithm(dim: int, pop_size: int, iterations: int,
                  function: Function, f_min: float, f_max: float,
                  alpha: float, gamma: float):
    positions, velocities, frequencies, pulse_rates, loudness = init_population(function, dim, pop_size)

    temp_positions = positions.copy()
    fitness = [function(position) for position in positions]

    best_index = fitness.index(min(fitness))
    best_solution = positions[best_index]
    best_fitness = fitness[best_index]
    for it in range(iterations):
        avg_loudness = sum(loudness) / pop_size
        for i in range(pop_size):
            frequencies[i] = f_min + ((f_max - f_min) * random.uniform(0, 1))
            for j in range(dim):
                velocities[i][j] += (positions[i][j] - best_solution[j]) * frequencies[i]
                temp_positions[i][j] = positions[i][j] + velocities[i][j]

            if random.uniform(0, 1) < pulse_rates[i]:
                beta = random.uniform(-1, 1)
                for j in range(dim):
                    temp_positions[i][j] = positions[i][j] + (beta * avg_loudness)

            for j in range(dim):
                if temp_positions[i][j] < function.x_min:
                    temp_positions[i][j] = function.x_min
                elif temp_positions[i][j] > function.x_max:
                    temp_positions[i][j] = function.x_max

            if random.uniform(0, 1) < loudness[i] and function(temp_positions[i]) < best_fitness:
                positions[i] = temp_positions[i]
                fitness[i] = function(positions[i])
                loudness[i] *= alpha
                pulse_rates[i] = (1 - math.exp(-gamma * it))*0.5
                #print(f"Bat {i} found better solution: {fitness[i]}")

            best_index = fitness.index(min(fitness))
            best_solution = positions[best_index]
            best_fitness = fitness[best_index]

        #print(f"Generation {it}: Best Fitness: {best_fitness}, Best Solution: {best_solution}")
    return best_solution, best_fitness
