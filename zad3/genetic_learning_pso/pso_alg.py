import random

DIM_NUMBER = 20
SG = 20


def generate_population(n_particles: int, x_min: float, x_max: float) -> tuple:
    positions = []
    velocities = []
    for i in range(n_particles):
        position = [random.uniform(x_min, x_max) for _ in range(DIM_NUMBER)]
        velocity = [0 for _ in range(DIM_NUMBER)]
        positions.append(position)
        velocities.append(velocity)
    return positions, velocities


def run_pso(fitness_function: (), iterations: int,
            n_particles: int, inertion_factor: float, cognitive_const: float, social_const: float,
            mutation_prob: float):
    positions, velocities = generate_population(n_particles, fitness_function.x_min,
                                                fitness_function.x_max)

    fitness = [fitness_function(position) for position in positions]
    best_index = fitness.index(min(fitness))
    G = positions[best_index].copy()  # global best

    # main loop
    exemplars = positions.copy()
    exemplars_i_last = [[]] * n_particles
    for it in range(iterations):
        for i in range(n_particles):

            # crossover
            child = [0] * DIM_NUMBER
            for dim in range(DIM_NUMBER):
                r_d = random.uniform(0, 1)
                k = random.randint(0, n_particles - 1)
                random_particle = positions[k]
                if fitness[i] < fitness[k]:
                    child[dim] = r_d * positions[i][dim] + (1 - r_d) * random_particle[dim]
                else:
                    child[dim] = random_particle[dim]

            # mutation
            for dim in range(DIM_NUMBER):
                r_d = random.uniform(0, 1)
                if r_d < mutation_prob:
                    child[dim] = random.uniform(fitness_function.x_min, fitness_function.x_max)

            # selection
            child_fitness = fitness_function(child)
            if child_fitness < fitness_function(exemplars[i]):
                exemplars[i] = child

            # particle update
            for dim in range(DIM_NUMBER):
                velocities[i][dim] = inertion_factor * velocities[i][dim] + \
                                     cognitive_const * random.uniform(0, 1) * (exemplars[i][dim] - positions[i][dim]) + \
                                     social_const * random.uniform(0, 1) * (G[dim] - positions[i][dim])
                positions[i][dim] += velocities[i][dim]

                if positions[i][dim] < fitness_function.x_min:
                    positions[i][dim] = fitness_function.x_min
                elif positions[i][dim] > fitness_function.x_max:
                    positions[i][dim] = fitness_function.x_max

            current_fitness = fitness_function(positions[i])
            if current_fitness < fitness[i]:
                fitness[i] = current_fitness
                if current_fitness < fitness_function(G):
                    G = positions[i].copy()

            exemplars_i_last[i].append(child_fitness)
            # stagnation check
            if len(exemplars_i_last[i]) == SG:
                if max(exemplars_i_last[i]) - min(exemplars_i_last[i]) <= 0.01:
                    # Select exemplar_i by the 20% tournament selection
                    tournament = []
                    for _ in range(int(n_particles * 0.2)):
                        k = random.randint(0, n_particles - 1)
                        tournament.append((k, fitness[k]))
                    min_tournament = float('inf')
                    for t in tournament:
                        if t[1] < min_tournament:
                            min_tournament = t[1]
                            exemplars[i] = positions[t[0]]
                exemplars_i_last[i].pop(0)
    return G, fitness_function(G)
