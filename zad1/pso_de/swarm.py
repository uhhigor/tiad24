import random

from zad1.pso.particle import Particle


def fitness_function() -> float:  # need to be set by user
    pass


def init_population(N, dim_number, x_min, x_max, inertion_factor, cognitive_const, social_const) -> list:
    population = []
    for i in range(N):
        individual = []
        for j in range(dim_number):
            individual.append(random.uniform(x_min, x_max))
        population.append(Particle(individual, inertion_factor, cognitive_const, social_const, x_min, x_max))
    return population


def update_fitness(particle: Particle):
    particle.fitness = fitness_function(particle.x)
    if particle.fitness < particle.best_fitness:
        particle.best_fitness = particle.fitness
        particle.best_x = particle.x


def get_best(swarm: list) -> Particle:
    best_particle = swarm[0]
    for particle in swarm:
        if particle.best_fitness < best_particle.best_fitness:
            best_particle = particle
    return best_particle


def mutation(population, F, particle: Particle) -> Particle:
    v = []
    particle_x = particle.x
    xr2, xr3 = random.sample(population, 2)
    xr2 = xr2.x
    xr3 = xr3.x
    for i in range(len(particle_x)):
        v.append(particle_x[i] + F * (xr2[i] - xr3[i]))

    return Particle(v, particle.inertion_factor, particle.cognitive_const, particle.social_const, particle.x_min, particle.x_max)


def crossover(individual, mutated, pc) -> Particle:
    o = individual.x
    for i in range(len(individual.x)):
        if random.random() < pc:
            o[i] = mutated.x[i]
    return Particle(o, individual.inertion_factor, individual.cognitive_const, individual.social_const, individual.x_min, individual.x_max)


def selection(crossed, individual) -> Particle:
    if crossed.fitness < individual.fitness:
        return crossed
    else:
        return individual


def update_swarm(swarm: list, F, pc):
    for particle in swarm:
        update_fitness(particle)

    best_particle = get_best(swarm)
    F = 0.3
    pc = 0.5
    for i in range(len(swarm)):
        particle = swarm[i]

        mutant = mutation(swarm, F, particle)
        update_fitness(mutant)
        trial = crossover(particle, mutant, pc)
        update_fitness(trial)
        selected = selection(trial, particle)

        swarm[i] = selected

        swarm[i].update_particle(best_particle)
        update_fitness(swarm[i])


