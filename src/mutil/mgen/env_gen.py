from typing import Literal
import matplotlib.pyplot as plt
import numpy as np

"""
File: env_gen.py

This file contains tools for creating envelope splines.
"""

class NthPowerEnvelope:
    """
    Represents an n-th power envelope.
    """
    def __init__(self, p1: tuple, p2: tuple, power: int, shape: Literal["concave", "convex"]):
        self.power = power
        self.shape = shape
        if (shape == "concave" and p2[1] > p1[1]) or (shape == "convex" and p2[1] < p1[1]):
            self.m = (p2[1] - p1[1]) / (p2[0] - p1[0]) ** power
            self.a = p1[0]
            self.b = p1[1]
        else:
            self.m = (p2[1] - p1[1]) / ((-1) ** (power + 1) * (p2[0] - p1[0]) ** power)
            self.a = p2[0]
            self.b = p2[1]
    
    def __call__(self, x) -> float:
        """
        Applies the envelope to an input x-value
        :param x: The x-value
        :return: The output y-value
        """
        return self.m * (x - self.a) ** self.power + self.b

if __name__ == "__main__":
    point1 = (3, 11)
    point2 = (7, 20)
    power = 4
    env = NthPowerEnvelope(point1, point2, power, "concave")

    NUM = 100
    xvals = np.linspace(point1[0], point2[0], NUM)
    yvals = np.zeros(NUM)
    for i, xval in enumerate(xvals):
        yvals[i] = env(xval)
    
    fig, ax = plt.subplots()
    ax.plot(xvals, yvals)
    ax.plot(point1[0], point1[1], "ro")
    ax.plot(point2[0], point2[1], "ro")
    plt.show()
