from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

ro = transformations.get_otos12()
pc = [pitch.PitchClass12(i) for i in range(12)]

