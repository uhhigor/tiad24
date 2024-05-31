import argparse
import function
import time
import bat.bat_algorithm as bat
import boa.boa_algorithm as boa

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--function', type=int, help='Function number (1-6)')
parser.add_argument('--dim_number', type=int, help='Number of dimensions')
parser.add_argument('-p', '--population', type=int, help='Number of population')
parser.add_argument('--iterations', type=int, help='Number of iterations')
parser.add_argument('--f_min', type=float, help='f_min (BAT)')
parser.add_argument('--f_max', type=float, help='f_max (BAT)')
parser.add_argument('-a', '--alfa', type=float, help='Alfa (BAT)')
parser.add_argument('-b', '--beta', type=float, help='Beta (BAT)')
parser.add_argument('--probability', type=float, help='p (BOA)')


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

sum_bat = 0
sum_boa = 0
sum_boa_levy = 0

bat_time_ms = 0
boa_time_ms = 0
boa_levy_time_ms = 0

for i in range(30):
    print(str(i+1) + " | " + "==" * 20)
    start = time.time()
    best_pos, best_fit = bat.run_algorithm(
        args.dim_number,
        args.population,
        args.iterations,
        func,
        args.f_min,
        args.f_max,
        args.alfa,
        args.beta)
    end = time.time()
    bat_time_ms += (end - start) * 1000
    sum_bat += best_fit
    print("BAT: " + str(best_fit) + " | " + str((end - start) * 1000) + " ms")

    start = time.time()
    best_pos, best_fit = boa.run_algorithm(
        args.dim_number,
        args.population,
        args.iterations,
        func,
        args.probability,
        False)
    end = time.time()
    boa_time_ms += (end - start) * 1000
    sum_boa += best_fit
    print("BOA: " + str(best_fit) + " | " + str((end - start) * 1000) + " ms")

    start = time.time()
    best_pos, best_fit = boa.run_algorithm(
        args.dim_number,
        args.population,
        args.iterations,
        func,
        args.probability,
        True)
    end = time.time()
    boa_levy_time_ms += (end - start) * 1000
    sum_boa_levy += best_fit
    print("BOA+LEVY: " + str(best_fit) + " | " + str((end - start) * 1000) + " ms")

print("==" * 30)
print("BAT: " + str(round(sum_bat / 30, 3)) + " | " + str(round(bat_time_ms / 30, 0)) + " ms")
print("BOA: " + str(round(sum_boa / 30, 3)) + " | " + str(round(boa_time_ms / 30, 0)) + " ms")
print("BOA+LEVY: " + str(round(sum_boa_levy / 30, 3)) + " | " + str(round(boa_levy_time_ms / 30, 0)) + " ms")

