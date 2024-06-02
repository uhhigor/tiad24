# Slime Mould algorithm implementation
import math
import random

DIM_NUMBER = 20
SG = 20


def run_alg(function: (), iterations: int, pop_size: int, w: float, vb: float, mutation_prob=0.1, number_of_swarms=1):
    global_positions = [
        [random.uniform(function.x_min, function.x_max) for _ in range(DIM_NUMBER)] for _ in range(pop_size)
    ]

    individuals_per_swarm = int(pop_size / number_of_swarms)
    swarm_positions = []
    last_individual_index = 0
    for i in range(number_of_swarms):
        swarm_positions.append(global_positions[last_individual_index:(last_individual_index + individuals_per_swarm)])
        last_individual_index += individuals_per_swarm

    swarm_exemplars = []
    for swarm_no in range(number_of_swarms):
        swarm_exemplars.append(swarm_positions[swarm_no].copy())
    swarm_exemplars_i_last = []
    for swarm_no in range(number_of_swarms):
        swarm_exemplars_i_last.append([[] for _ in range(int(individuals_per_swarm))])

    for i in range(iterations):
        for swarm_no in range(number_of_swarms):
            positions = swarm_positions[swarm_no]
            fitness = [function(position) for position in positions]
            positions = [position for _, position in sorted(zip(fitness, positions))]

            exemplars = swarm_exemplars[swarm_no]
            exemplars_i_last = swarm_exemplars_i_last[swarm_no]

            w = w * math.exp(-i / iterations)

            swarm_population = len(positions)
            for j in range(swarm_population):
                # PATTERN
                # crossover
                child = [0] * DIM_NUMBER
                for dim in range(DIM_NUMBER):
                    r_d = random.uniform(0, 1)
                    k = random.randint(0, swarm_population - 1)
                    random_particle = positions[k]
                    if fitness[i] < fitness[k]:
                        child[dim] = r_d * positions[i][dim] + (1 - r_d) * random_particle[dim]
                    else:
                        child[dim] = random_particle[dim]

                # mutation
                for dim in range(DIM_NUMBER):
                    r_d = random.uniform(0, 1)
                    if r_d < mutation_prob:
                        child[dim] = random.uniform(function.x_min, function.x_max)

                # selection
                child_fitness = function(child)
                if child_fitness < function(exemplars[i]):
                    exemplars[i] = child

                exemplars_i_last[i].append(child_fitness)
                # stagnation check
                if len(exemplars_i_last[i]) == SG:
                    if max(exemplars_i_last[i]) - min(exemplars_i_last[i]) <= 0.01:
                        # Select exemplar_i by the 20% tournament selection
                        tournament = []
                        for _ in range(int(pop_size * 0.2)):
                            k = random.randint(0, pop_size - 1)
                            tournament.append((k, fitness[k]))
                        min_tournament = float('inf')
                        for t in tournament:
                            if t[1] < min_tournament:
                                min_tournament = t[1]
                                exemplars[i] = positions[t[0]]
                    exemplars_i_last[i].pop(0)

                # PATTERN END
                # update position
                if random.uniform(0, 1) < w:
                    # approach food
                    #best_position = positions[0]
                    r = random.uniform(0, 1)
                    for k in range(DIM_NUMBER):
                        #positions[j][k] = positions[j][k] + r * (best_position[k] - positions[j][k])
                        positions[j][k] = positions[j][k] + r * (exemplars[j][k] - positions[j][k])
                else:
                    # move randomly
                    random_position = positions[random.randint(0, swarm_population - 1)]
                    r = random.uniform(0, 1)
                    for k in range(DIM_NUMBER):
                        positions[j][k] = positions[j][k] + r * (random_position[k] - positions[j][k])
                # vibrate
                for k in range(DIM_NUMBER):
                    positions[j][k] = positions[j][k] + random.uniform(-vb, vb)

                # check boundaries
                for k in range(DIM_NUMBER):
                    if positions[j][k] < function.x_min:
                        positions[j][k] = function.x_min
                    elif positions[j][k] > function.x_max:
                        positions[j][k] = function.x_max

        global_best_fitness = float('inf')
        global_best_position = []
        for swarm_no in range(number_of_swarms):
            current_swarm_positions = swarm_positions[swarm_no]
            current_swarm_fitness = [function(position) for position in current_swarm_positions]
            best_swarm_fitness = min(current_swarm_fitness)
            best_swarm_position = current_swarm_positions[current_swarm_fitness.index(best_swarm_fitness)]
            if best_swarm_fitness < global_best_fitness:
                global_best_fitness = best_swarm_fitness
                global_best_position = best_swarm_position
        return global_best_position, global_best_fitness
