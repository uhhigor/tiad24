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


def update_swarm(swarm: list):
    best_particle = get_best(swarm)
    for particle in swarm:
        particle.update_particle(best_particle)
        update_fitness(particle)
