"""
Name: clarinet_tempo.py
Author: Jeff Martin
Date: 5/30/23

Description:
"""

import pctheory.tempo
from fractions import Fraction

ratios = [Fraction(3, 2), Fraction(5, 4)]

tempos = pctheory.tempo.make_metric_modulation_chain(72, ratios)
print([float(tempo) for tempo in tempos])

pctheory.tempo.plot_tempo_table([72, 90, 108])