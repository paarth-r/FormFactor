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
xvals = []
yvals = []
captured_x_vals = []
captured_y_vals = []
def populate_ideal():
    with open("ideal.csv", mode="w") as wbenchart:
        write = csv.writer(wbenchart)
        for n in range(0, 10, 1):
            write.writerow([n, n**2])
def read_ideal():
    with open("ideal.csv", newline="") as benchart:
        read = csv.reader(benchart)
        pointlist = list(read)
        for n in range(len(pointlist)):
            pointlist[n] = list(map(int, pointlist[n]))
    for n in pointlist:
        xvals.append(n[0])
        yvals.append(n[1])
    return pointlist

def read_captured():
    with open("captured.csv", newline="") as captured:
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

def graph(sectlen):
    read_captured()
    read_ideal()
    slope, intercept, r, p, std_err = stats.linregress(captured_x_vals[0:10], captured_y_vals[0:10])

    curslope = sign(slope)

    sectlen = 50
    for n in range(sectlen, len(captured_x_vals)):
        i = n-sectlen
        slope, _, _, _, _ = stats.linregress(captured_x_vals[i:n], captured_y_vals[i:n])
        if sign(slope) != sign(curslope):
            intervals[-1].append(n-5)
            intervals.append([n-4])
            curslope *= -1
        
    intervals.pop(-1)

    for n in intervals:
        plt.axvline(x = n[1], label = 'axvline - full height')
        intervaleqs.append(np.polyfit(captured_x_vals[n[0]:n[1]],captured_y_vals[n[0]:n[1]], 2))
    plt.plot(xvals, yvals)
    plt.plot(captured_x_vals, captured_y_vals)
    plt.ylabel("stuff")
    plt.show()



    