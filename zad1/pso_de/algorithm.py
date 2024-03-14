import zad1.pso_de.swarm as swarm


def check_stagnation(last_10: list):
    if max(last_10) - min(last_10) <= 0.0001:
        return True
    return False


def run_algorithm(function: (), d: int, n_particle: int, iterations: int, F: float, pc: float,
                  inertion_factor: float, cognitive_const: float, social_const: float):
    swarm.fitness_function = function

    s = swarm.init_population(n_particle, d, function.x_min, function.x_max, inertion_factor, cognitive_const,
                              social_const)

    last_10 = [0] * 10
    while True:
        swarm.update_swarm(s, F, pc)

        last_10.append(swarm.get_best(s).best_fitness)
        if len(last_10) > 10:
            last_10.pop(0)
        if check_stagnation(last_10):
            break

    return swarm.get_best(s)
