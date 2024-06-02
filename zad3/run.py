import argparse
import function
import time
import pso_with_pattern.pso_alg as pso
import sma_with_pattern.sma_alg as sma

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--function', type=int, help='Function number (1-6)')
parser.add_argument('--dim_number', type=int, help='Number of dimensions')
parser.add_argument('-p_sma', '--population_sma', type=int, help='Population size for sma')
parser.add_argument('-p_pso', '--population_pso', type=int, help='Population size for pso')
parser.add_argument('-i_sma', '--iterations_sma', type=int, help='Number of iterations for sma')
parser.add_argument('-i_pso', '--iterations_pso', type=int, help='Number of iterations for pso')
parser.add_argument('-w', '--w', type=float, help='W parameter for sma')
parser.add_argument('-vb', '--vb', type=float, help='Vb parameter for sma')
parser.add_argument('-m_sma', '--mutation_sma', type=float, help='Mutation probability for sma')
parser.add_argument('-s_sma', '--swarms_sma', type=int, help='Number of swarms for sma')
parser.add_argument('-in', '--inertion', type=float, help='Inertion factor for pso')
parser.add_argument('-c', '--cognitive', type=float, help='Cognitive const for pso')
parser.add_argument('-s_c', '--social', type=float, help='Social const for pso')
parser.add_argument('-m_pso', '--mutation_pso', type=float, help='Mutation probability for pso')
parser.add_argument('-s_pso', '--swarms_pso', type=int, help='Number of swarms for pso')


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

pso_values = []
sma_values = []

pso_time_ms = 0
sma_time_ms = 0

print("RUNNING PSO WITH PARAMETERS: ")
print("Iterations: " + str(args.iterations_pso) + " | Population: " + str(args.population_pso) + " | Inertion: " + str(args.inertion) + " | Cognitive: " + str(args.cognitive) + " | Social: " + str(args.social) + " | Mutation: " + str(args.mutation_pso) + " | Swarms: " + str(args.swarms_pso))
print("RUNNING SMA WITH PARAMETERS: ")
print("Iterations: " + str(args.iterations_sma) + " | Population: " + str(args.population_sma) + " | W: " + str(args.w) + " | Vb: " + str(args.vb) + " | Mutation: " + str(args.mutation_sma) + " | Swarms: " + str(args.swarms_sma))

for i in range(30):
    print(str(i+1) + " | " + "==" * 20)
    start = time.time()
    best_pos, best_fit = pso.run_pso(
        func,
        args.iterations_pso,
        args.population_pso,
        args.inertion,
        args.cognitive,
        args.social,
        args.mutation_pso,
        args.swarms_pso)
    end = time.time()
    pso_time_ms += (end - start) * 1000
    pso_values.append(best_fit)
    print("PSO: " + str(best_fit) + " | " + str((end - start) * 1000) + " ms")

    start = time.time()
    best_pos, best_fit = sma.run_alg(
        func,
        args.iterations_sma,
        args.population_sma,
        args.w,
        args.vb,
        args.mutation_sma,
        args.swarms_sma)
    end = time.time()
    sma_time_ms += (end - start) * 1000
    sma_values.append(best_fit)
    print("SMA: " + str(best_fit) + " | " + str((end - start) * 1000) + " ms")


avg_pso = sum(pso_values) / 30
pso_standard_deviation = 0
for value in pso_values:
    pso_standard_deviation += (value - avg_pso) ** 2
pso_standard_deviation = (pso_standard_deviation / 30) ** 0.5

avg_sma = sum(sma_values) / 30
sma_standard_deviation = 00
for value in sma_values:
    sma_standard_deviation += (value - avg_sma) ** 2
sma_standard_deviation = (sma_standard_deviation / 30) ** 0.5


print("==" * 30)
print("PSO: " + str(round(avg_pso, 3)) + " std: " + str(round(pso_standard_deviation, 3)) + " | " + str(round(pso_time_ms / 30, 0)) + " ms")
print("SMA: " + str(round(avg_sma, 3)) + " std: " + str(round(sma_standard_deviation, 3)) + " | " + str(round(sma_time_ms / 30, 0)) + " ms")

