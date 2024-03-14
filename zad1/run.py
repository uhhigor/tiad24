import argparse
import pso.algorithm as algorithm
import zad1.function as function
import zad1.pso_de.algorithm as pso_de
import zad1.de.differential_evolution as de
import time

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--function', type=int, help='Function number (1-2)')
parser.add_argument('--dim_number', type=int, help='Number of dimensions')
parser.add_argument('-n', '--n_particle', type=int, help='Number of particles (PSO)')
parser.add_argument('--inertion_factor', type=float, help='Inertion factor (PSO)')
parser.add_argument('--cognitive_const', type=float, help='Cognitive constant (PSO)')
parser.add_argument('--social_const', type=float, help='Social constant (PSO)')
parser.add_argument('--iterations', type=int, help='Number of iterations (DE)')
parser.add_argument('--pc', type=float, help='Crossover probability (DE)')
parser.add_argument('--F', type=float, help='Amplification factor (DE)')

args = parser.parse_args()

func_dict = {
    1: function.Ackley(),
    2: function.Griewank(),
    3: function.Levy(),
    4: function.Rastrigin(),
    5: function.Schwefel(),
    6: function.Sphere()
}

func = func_dict[args.function]

sum_pso = 0
sum_de = 0
sum_pso_de = 0

pso_time_ms = 0
de_time_ms = 0
pso_de_time_ms = 0

for i in range(30):
    print(str(i) + " | " + "==" * 20)
    start = time.time()
    result_pso = algorithm.run_algorithm(
        func,
        args.dim_number,
        args.n_particle,
        args.iterations,
        args.inertion_factor,
        args.cognitive_const,
        args.social_const)
    end = time.time()
    pso_time_ms += (end - start) * 1000
    print('PSO: Best value: ' + str(round(result_pso.best_fitness, 3)) + ' for [', end='')
    for r in result_pso.best_x:
        print(round(r, 3), end='; ')
    print(']')

    start = time.time()
    result_de_best, result_de_value = de.differential_evolution(args.iterations, func, args.dim_number, args.pc, args.F, args.n_particle)
    end = time.time()
    de_time_ms += (end - start) * 1000
    print('DE: Best value: ' + str(round(result_de_value, 3)) + ' for [', end='')
    for r in result_de_best:
        print(round(r, 3), end='; ')
    print(']')

    start = time.time()
    result_pso_de = pso_de.run_algorithm(
        func,
        args.dim_number,
        args.n_particle,
        args.iterations,
        args.F,
        args.pc,
        args.inertion_factor,
        args.cognitive_const,
        args.social_const)
    end = time.time()
    pso_de_time_ms += (end - start) * 1000
    print('PSO+DE: Best value: ' + str(round(result_pso_de.best_fitness, 3)) + ' for [', end='')
    for r in result_pso_de.best_x:
        print(round(r, 3), end='; ')
    print(']')

    sum_pso += result_pso.best_fitness
    sum_de += result_de_value
    sum_pso_de += result_pso_de.best_fitness

print("==" * 20)
print('Function: ' + func.name() + ", Global minimum: " + str(func.global_min_value))
print('PSO: Average value: ' + str(round(sum_pso / 30, 3)) + ", Average time: " + str(round(pso_time_ms / 30, 0)) + " ms")
print('DE: Average value: ' + str(round(sum_de / 30, 3)), ", Average time: " + str(round(de_time_ms / 30, 0)) + " ms")
print('PSO+DE: Average value: ' + str(round(sum_pso_de / 30, 3)), ", Average time: " + str(round(pso_de_time_ms / 30, 0)) + " ms")
