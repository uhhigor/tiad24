import math


class Function:
    def __init__(self, x_min: float, x_max: float, global_min_value: float):
        self.x_min = x_min
        self.x_max = x_max
        self.global_min_value = global_min_value

    def __call__(self, x: list) -> float:
        pass


class Ackley(Function):
    def __init__(self):
        super().__init__(-32.768, 32.768, 0)

    def __call__(self, x: list) -> float:
        a = 20
        b = 0.2
        c = 2 * math.pi

        d = len(x)

        sum1 = 0
        sum2 = 0
        for xi in x:
            sum1 += xi ** 2
            sum2 += math.cos(c * xi)

        total = -a * math.exp(-b * math.sqrt(sum1 / d)) - math.exp(sum2 / d) + a + math.exp(1)

        return total

