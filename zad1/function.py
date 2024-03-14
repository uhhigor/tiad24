import math


class Function:
    def __init__(self, x_min: float, x_max: float, global_min_value: float):
        self.x_min = x_min
        self.x_max = x_max
        self.global_min_value = global_min_value

    def __call__(self, x: list) -> float:
        pass

    def name(self):
        pass


class Ackley(Function):
    def __init__(self):
        super().__init__(-32.768, 32.768, 0)

    def name(self):
        return 'Ackley'

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


class Griewank(Function):
    def __init__(self):
        super().__init__(-600, 600, 0)

    def name(self):
        return 'Griewank'

    def __call__(self, x: list) -> float:
        sum1 = 0
        mul1 = 1
        for i, xi in enumerate(x):
            sum1 += xi ** 2
            mul1 *= math.cos(xi / math.sqrt(i + 1))

        total = ((sum1 / 4000) - mul1) + 1
        return total


class Levy(Function):
    def __init__(self):
        super().__init__(-10, 10, 0)

    def name(self):
        return 'Levy'

    def __call__(self, x: list) -> float:
        w = 1 + (x[0] - 1) / 4
        sum1 = 0
        for i in range(len(x) - 1):
            sum1 += ((x[i] - 1) ** 2) * (1 + 10 * (math.sin(math.pi * (x[i] + 1)) ** 2))
        total = (math.sin(math.pi * w) ** 2) + sum1 + ((x[len(x) - 1] - 1) ** 2) * (
                1 + (math.sin(2 * math.pi * x[len(x) - 1]) ** 2))
        return total


class Rastrigin(Function):
    def __init__(self):
        super().__init__(-5.12, 5.12, 0)

    def name(self):
        return 'Rastrigin'

    def __call__(self, x: list) -> float:
        sum1 = 0
        for xi in x:
            sum1 += xi ** 2 - (10 * math.cos(2 * math.pi * xi))
        total = 10 * len(x) + sum1
        return total


class Schwefel(Function):
    def __init__(self):
        super().__init__(-500, 500, 0)

    def name(self):
        return 'Schwefel'

    def __call__(self, x: list) -> float:
        sum1 = 0
        for xi in x:
            try:
                sum1 += xi * math.sin(math.sqrt(abs(xi)))
            except ValueError:
                print(str(xi) + " " + str(ValueError), end=" | ")
        total = (418.9829 * len(x)) - sum1
        return total


class Sphere(Function):
    def __init__(self):
        super().__init__(-5.12, 5.12, 0)

    def name(self):
        return 'Sphere'

    def __call__(self, x: list) -> float:
        sum1 = 0
        for xi in x:
            sum1 += xi ** 2
        return sum1
