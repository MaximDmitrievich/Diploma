import numpy as np
import matplotlib.pyplot as plt
import sys
from math import floor, sqrt
import decimal
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten, LSTM, Conv1D, GlobalAveragePooling1D, MaxPooling1D, GlobalMaxPooling1D, AveragePooling1D
from keras import regularizers

def mathFilter(y):
    rng = range(1, len(y) - 1)
    res = []
    res.append(y[0])
    for j in rng:
        res.append((y[j - 1] / 4.0 + y[j] / 2.0 + y[j + 1] / 4.0))
    res.append(y[len(y) - 1])
    return res

def flooring(x):
    return floor(decimal.Decimal(x))

def main():
    data = np.fromfile("../../DataSets/I09.dat")
    a = 0
    b = len(data)

    x = np.linspace(a, b, num=b-a)
    y = []
    for j in range(a, b):
        y.append(0.0 - flooring(data[j]))
    

    y = mathFilter(mathFilter(mathFilter(mathFilter(y))))

    model = Sequential()

    model.add(Conv2D)

    plt.plot(x, y)
    plt.show()

if __name__ == "__main__":
    main()
