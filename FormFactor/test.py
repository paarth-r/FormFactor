import matplotlib.pyplot as plt
import numpy as np
import vidanalyse
ints = vidanalyse.intervals
vidanalyse.graph(40)
for i in range(len(ints)-1):
    plt.plot(vidanalyse.captured_x_vals[ints[i][0]:ints[i][1]],vidanalyse.captured_y_vals[ints[i][0]:ints[i][1]])
plt.show()