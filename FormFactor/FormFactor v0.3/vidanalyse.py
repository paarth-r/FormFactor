import cv2 
import matplotlib.pyplot as plt
import csv
from scipy import stats
import numpy as np

def sign(n):
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        return 1

pointlist = []
captured = []
captured_x_vals = []
captured_y_vals = []

def read_captured(file):
    with open(file, newline="") as captured:
        read = csv.reader(captured)
        captured = list(read)
        for n in range(len(captured)):
            captured[n] = list(map(int, captured[n]))
    for n in captured:
        captured_x_vals.append(n[0])
        captured_y_vals.append(n[1])
    return captured

intervals = [[0]]
intervaleqs = []

def graph(sectlen, file):
    read_captured(file)
    slope, intercept, r, p, std_err = stats.linregress(captured_x_vals[0:10], captured_y_vals[0:10])

    curslope = sign(slope)

    for n in range(sectlen, len(captured_x_vals)):
        i = n-sectlen
        slope, _, _, _, _ = stats.linregress(captured_x_vals[i:n], captured_y_vals[i:n])
        if sign(slope) != sign(curslope):
            intervals[-1].append(n)
            intervals.append([n])
            print(slope)
            curslope *= -1
        
    intervals.pop(-1)

    for n in intervals:
        plt.axvline(x = n[1], label = 'axvline - full height')
    plt.plot(captured_x_vals, captured_y_vals)
    plt.ylabel("stuff")
    plt.show()



    