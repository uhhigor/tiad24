# Slime Mould algorithm implementation
import math
import random

import numpy as np

DIM_NUMBER = 20
def run_alg(function: (), iterations: int, pop_size: int, w: float, vb: float):
    positions = [
        [random.uniform(function.x_min, function.x_max) for _ in range(DIM_NUMBER)] for _ in range(pop_size)
    ]

    for i in range(iterations):
        fitness = [function(position) for position in positions]
        positions = [position for _, position in sorted(zip(fitness, positions))]

        w = w * math.exp(-i / iterations)

        # update positions

        for j in range(pop_size):
            if random.uniform(0, 1) < w:
                # approach food
                best_position = positions[0]
                r = random.uniform(0, 1)
                for k in range(DIM_NUMBER):
                    positions[j][k] = positions[j][k] + r * (best_position[k] - positions[j][k])
            else:
                # move randomly
                random_position = positions[random.randint(0, pop_size - 1)]
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

    return positions[0], function(positions[0])
