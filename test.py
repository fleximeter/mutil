from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

s = pset.Sieve12(((3, 0), (4, 0)), 0)
print(s.ints)