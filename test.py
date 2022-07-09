from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

pc = pcset.make_pcset24(5,2,11,15,21,18)
s = pcset.SetClass24(pc)
t = s.get_abstract_subset_classes()
print(s.pcset)

tr = transformations.UTO(5, 13)
print(tr.transform(s.pcset))

