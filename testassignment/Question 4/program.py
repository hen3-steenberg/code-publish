import matplotlib.pyplot as plt
import numpy as np


def func(x):
    return np.pow(x, 2)


X = np.linspace(0, 10, 100)
plt.plot(X, func(X))
plt.show()
