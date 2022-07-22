from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

pcs = pcseg.generate_random_all_interval_row(0)
print(pcs)
