import function
import zad3.genetic_learning_pso.pso_alg as pso_alg

best_pos, best_fit = pso_alg.run_pso(function.Rastrigin(), 1000, 500, 0.5, 0.9, 0.9, 0.5)

print(round(best_fit, 4))
