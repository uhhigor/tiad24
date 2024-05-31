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
            mutation_prob: float, number_of_swarms=1):
    global_positions, global_velocities = generate_population(n_particles, fitness_function.x_min,
                                                              fitness_function.x_max)

    swarm_positions = []
    swarm_velocities = []
    particles_per_swarm = int(n_particles / number_of_swarms)
    last_particle_index = 0
    for swarm_no in range(number_of_swarms):
        swarm_positions.append(global_positions[last_particle_index:(last_particle_index + particles_per_swarm)])
        swarm_velocities.append(global_velocities[last_particle_index:(last_particle_index + particles_per_swarm)])
        last_particle_index += particles_per_swarm

    swarm_fitness = []
    for swarm_no in range(number_of_swarms):
        swarm_fitness.append([fitness_function(position) for position in swarm_positions[swarm_no]])

    G = []
    best_global_fitness = float('inf')
    for swarm_no in range(number_of_swarms):
        current_best_fitness = min(swarm_fitness[swarm_no])
        current_best_index = swarm_fitness[swarm_no].index(current_best_fitness)
        if current_best_fitness < best_global_fitness:
            best_global_fitness = current_best_fitness
            G = swarm_positions[swarm_no][current_best_index].copy()

    swarm_exemplars = []
    for swarm_no in range(number_of_swarms):
        swarm_exemplars.append(swarm_positions[swarm_no].copy())
    swarm_exemplars_i_last = []
    for swarm_no in range(number_of_swarms):
        swarm_exemplars_i_last.append([[] for _ in range(int(particles_per_swarm))])

    # main loop
    for it in range(iterations):
        for swarm_no in range(number_of_swarms):
            fitness = swarm_fitness[swarm_no]
            positions = swarm_positions[swarm_no]
            velocities = swarm_velocities[swarm_no]
            exemplars = swarm_exemplars[swarm_no]
            exemplars_i_last = swarm_exemplars_i_last[swarm_no]
            swarm_particles_no = len(positions)
            for i in range(swarm_particles_no):
                # crossover
                child = [0] * DIM_NUMBER
                for dim in range(DIM_NUMBER):
                    r_d = random.uniform(0, 1)
                    k = random.randint(0, swarm_particles_no - 1)
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
                                         cognitive_const * random.uniform(0, 1) * (
                                                 exemplars[i][dim] - positions[i][dim]) + \
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
            #print(f"Swarm {swarm_no} iteration {it} best fitness: {fitness_function(G)}")

    return G, fitness_function(G)
