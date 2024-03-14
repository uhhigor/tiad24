# pc - crossover probability
# F - amplification factor [0,1]
# N - population size
import random
from zad1 import function


def check_stagnation(last_10: list):
    if max(last_10) - min(last_10) <= 0.0001:
        return True
    return False


# DE/rand/1/bin
def mutation_2(population, F) -> list:
    v = []
    xr1, xr2, xr3 = random.sample(population, 3)
    for i in range(len(xr1)):
        v.append(xr1[i] + F * (xr2[i] - xr3[i]))
    return v


# DE/best/1/bin
def mutation_3(population, F, func: function.Function) -> list:
    v = []
    best = get_best(population, func)
    xr2, xr3 = random.sample(population, 2)
    for i in range(len(best)):
        v.append(best[i] + F * (xr2[i] - xr3[i]))
    return v


def get_best(population, func: function.Function) -> list:
    best = population[0]
    for individual in population:
        if func(individual) < func(best):
            best = individual
    return best


# binary crossover
def crossover(individual, mutated, pc) -> list:
    o = individual
    for i in range(len(individual)):
        if random.random() < pc:
            o[i] = mutated[i]
    return o


def selection(crossed, individual, func: function.Function) -> list:
    if func(crossed) < func(individual):
        return crossed
    else:
        return individual


def init_population(N, dim_number, x_min, x_max) -> list:
    population = []
    for i in range(N):
        individual = []
        for j in range(dim_number):
            individual.append(random.uniform(x_min, x_max))
        population.append(individual)
    return population


def differential_evolution(iterations, func: function.Function, dim_number, pc, F, N) -> [float]:
    last_10 = [0.0] * 10
    population = init_population(N, dim_number, func.x_min, func.x_max)
    while True:
        for i in range(N):
            individual = population[i]
            mutated = mutation_3(population, F, func)
            crossed = crossover(individual, mutated, pc)
            selected = selection(crossed, individual, func)
            population[i] = selected

        last_10.append(func(get_best(population, func)))
        if len(last_10) > 10:
            last_10.pop(0)
        if check_stagnation(last_10):
            break

        #iterations -= 1
        #if iterations == 0:
    best = get_best(population, func)
    return best, func(best)
