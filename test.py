from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

pcs = pcset.make_pcset12(0, 1, 2, 3, 4, 5)
print(type(next(iter(pcs))))
t = pcset.get_self_map_utos(pcs)
c = pcset.get_complement_map_utos(pcs)
print(t)
print(c)