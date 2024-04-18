import function
import math
from bat.bat_algorithm import run_algorithm


# Najlepiej dzialalo na parametrach:
# alpha: 0.9
# gamma: 0.9
# f_min: 0
# f_max: 2
# pop_size: 1000
# iterations: 1000

best_pos, best_fit = run_algorithm(20, 1000, 1000, function.Levy(), 0, 2, 0.9, 0.9)
print(round(best_fit, 4))
print(best_pos)
