from pctheory import pcseg, pcset, pseg, pset, pitch, transformations
from mgen import xml_gen

base_sc = pcset.get_all_combinatorial_hexachord("C")
print(base_sc)
sc1 = pcset.SetClass()
sc1.load_from_name("01237")
print(sc1)