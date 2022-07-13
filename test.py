from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources


pc1 = pcseg.generate_random_all_interval_row()
print(pc1)
print(pcseg.get_intervals(pc1))
print(pcseg.is_all_interval_row(pc1))
