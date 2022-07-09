from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources


s = pcset.SetClass12()
s.load_from_name("7-1")
t = s.get_abstract_subset_classes()
print(t)
