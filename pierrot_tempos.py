"""
File: pierrot_tempos.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 2/23/22

This file contains functionality for working with arrays.
"""

from fractions import Fraction
tempi = [Fraction(60, 1)]
ratios = [Fraction(4, 3), Fraction(6, 5), Fraction(1, 2), Fraction(3, 2), Fraction(4, 3)]

for i in range(len(ratios)):
    tempi.append(tempi[i] * ratios[i])

# print(tempi)
print([float(t) for t in tempi])
