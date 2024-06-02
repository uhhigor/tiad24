import function
import zad3.pso_with_pattern.pso_alg as pso_alg
import zad3.sma_with_pattern.sma_alg as sma_alg

best_pos, best_fit = pso_alg.run_pso(function.Sphere(), 1000, 500, 0.5, 0.9, 0.9, 0.5, 2)
print(round(best_fit, 4))

best_pos_sma, best_fit_sma = sma_alg.run_alg(function.Sphere(), 5000, 5000, 0.5, 0.0, 0.5, 1)
print(round(best_fit_sma, 4))