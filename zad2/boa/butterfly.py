import random
from zad2.function import Function


class Butterfly:
    def __init__(self, sensory_modality, stimulus, power_exponent, dim: int, function: Function):
        self.sensory_modality = sensory_modality
        self.stimulus = stimulus
        self.power_exponent = power_exponent
        self.position = [random.uniform(function.x_min, function.x_max) for _ in range(dim)]
