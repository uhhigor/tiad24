import function
import zad2.bat.bat_algorithm as bat
import zad2.boa.boa_algorithm as boa

# Najlepiej dzialalo na parametrach:
# alpha: 0.9
# gamma: 0.9
# f_min: 0
# f_max: 2
# pop_size: 1000
# iterations: 1000

best_pos, best_fit = bat.run_algorithm(20, 100, 100, function.Schwefel(), 0, 2, 0.9, 0.9)
print(round(best_fit, 4))
print(best_pos)

best_pos, best_value = boa.run_algorithm(20, 100, 100, function.Schwefel(), 0.8, False)
print(round(best_value, 4))
print(best_pos)

best_pos, best_value = boa.run_algorithm(20, 100, 100, function.Schwefel(), 0.8, True)
print(round(best_value, 4))
print(best_pos)
