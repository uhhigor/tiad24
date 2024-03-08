# pc - crossover probability
# F - amplification factor [0,1]
# N - population size
import random
import function


# base mutation
def mutation(population, F) -> list:
    v = []
    xr1, xr2, xr3 = random.sample(population, 3)
    for i in range(len(xr1)):
        v[i] = xr1[i] + F * (xr2[i] - xr3[i])
    return v


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


def differential_evolution(iterations, func: function.Function, dim_number, pc, F, N) -> float:
    population = init_population(N, dim_number, func.x_min, func.x_max)
    while True:
        for i in range(N):
            individual = population[i]
            mutated = mutation(population, F)
            crossed = crossover(individual, mutated, pc)
            selected = selection(crossed, individual, func)
            population[i] = selected
        if iterations == 0:
            return min(population)
