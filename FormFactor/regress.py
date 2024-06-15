from sympy import S, symbols, printing
from matplotlib import pyplot as plt
import numpy as np
import csv

with open("somebozo.csv", newline="") as benchbozo:
    read = csv.reader(benchbozo)
    bozopoints = list(read)
    for n in range(len(bozopoints)):
        bozopoints[n] = list(map(int, bozopoints[n]))

print(bozopoints)
x_data = []
y_data = []
for n in bozopoints:
    x_data.append(n[0])
    y_data.append(n[1])

print(np.polyfit(x_data, y_data, 3))
