import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from copy import copy

def plot_splin(t, data):
    splin = interp1d(t, data, kind='quadratic')
    t_new = np.linspace(t[0], t[-1], 1000)
    plt.plot(t_new, splin(t_new), '-', t, data, '--')
    plt.show()


def gl(t, data):
    data_new = np.zeros(len(data))
    T = t[-1] - t[0]
    dT = T/len(data)
    for i in range(len(t)-1):
        dt = t[i+1] - t[i]
        if dt < dT:
            q = dt/dT
            a = data[i]
            b = data[i+1]
            data_new[i] = a - (a-b)*(1-q)
            data_new[i+1] = b + (a-b)*(1-q)
    return data_new


def plot_gl(t, data):
    y = gl(t, data)
    plt.plot(t, y, '-', t, data, '--')
    plt.show()
