import function
import math
from zad2.bat.bat_algorithm import BatAlgorithm

batalg = BatAlgorithm(100, 20, 0, 5, 0.2, 0.5, function.Sphere())
result = batalg.run(100)
print(round(result, 3))
