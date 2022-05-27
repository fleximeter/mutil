from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, transformations, util

"""
p1 = pcseg.make_pcseg(6, 9, 5, 8, 4, 7, 1, 10, 2, 11, 3, 0)
p2 = pcseg.make_pcseg(8, 4, 7, 6, 9, 5, 11, 3, 0, 1, 10, 2)

mx1 = pcseg.TwelveToneMatrix(p1)
mx2 = pcseg.TwelveToneMatrix(p2)

t7i = transformations.RO(7, 0, 11)

a1 = [p1, t7i.transform(p1), p2, t7i.transform(p2)]
print(array.str_array(a1))

pcs1 = pcset.make_pcset24(4, 8, 9, 15, 18)
pcs2 = pcset.make_pcset24(4, 8, 10, 16, 18)
sc1 = pcset.SetClass24(pcs1)
sc2 = pcset.SetClass24(pcs2)
print(sc1.name_prime)
print(sc2.name_prime)
"""

sc1 = pcset.SetClass12()
sc1.load_from_name("[012345]")
p = list(sc1.get_partition2_subset_classes())
p.sort()
for i in p:
    print(i)

