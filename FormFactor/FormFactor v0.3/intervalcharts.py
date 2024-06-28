import matplotlib.pyplot as plt
import numpy as np
import vidanalyse
vidanalyse.graph(50)
x = np.linspace(0, 10, 11)
print(vidanalyse.intervaleqs)
ints = vidanalyse.intervals
for i,n in enumerate(vidanalyse.intervaleqs):
    y = np.array([np.sum(np.array([n[i]*(j**i) for i in range(len(n))])) for j in x])
    plt.plot(x,y)
    plt.plot(vidanalyse.captured_x_vals[ints[i][0]:ints[i][1]],vidanalyse.captured_y_vals[ints[i][0]:ints[i][1]])
plt.show()