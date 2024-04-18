import function
import math
from bat.bat_algorithm import run_algorithm

best_pos, best_fit = run_algorithm(20, 1000, 1000, function.Levy(), 0, 2, 0.9, 0.9)
print(round(best_fit, 4))
print(best_pos)
