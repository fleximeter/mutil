from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources
import os.path

ro = transformations.get_otos12()
pc = [pitch.PitchClass12(i) for i in range(12)]

print(os.path.dirname(__file__))
print(os.path.join(os.path.dirname(__file__), "test.py"))