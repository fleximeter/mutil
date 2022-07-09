from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

pcs = pcseg.generate_random_pcseg12(12, True, 0)
print(pcs)
print(pcseg.imb_n(pcs, 3))
print(pcseg.bip_n(pcseg.imb_n(pcs, 2)))