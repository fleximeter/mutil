"""
Name: linear_congruential.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 9/25/21

This file contains a linear congruential generator.
"""


class LinearCongruential:
    def __init__(self):
        """
        Creates a LinearCongruential engine
        """
        self._seed = 0
        self._mod = 99989
        self._mul = 51
        self._increment = 83

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    @property
    def mod(self):
        return self._mod

    @mod.setter
    def mod(self, value):
        self._mod = value

    @property
    def mul(self):
        return self._mul

    @mul.setter
    def mul(self, value):
        self._mul = value

    @property
    def increment(self):
        return self._increment

    @increment.setter
    def increment(self, value):
        self._increment = value

    def next(self):
        self._seed = (self._mul * self._seed + self._increment) % self._mod
        return self._seed

    def next_with_bounds(self, lower_bound, upper_bound):
        self._seed = (self._mul * self._seed + self._increment) % self._mod
        return self._seed % (upper_bound - lower_bound) + lower_bound
