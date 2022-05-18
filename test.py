from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, transformations, util

p1 = pcseg.make_pcseg(6, 9, 5, 8, 4, 7, 1, 10, 2, 11, 3, 0)
p2 = pcseg.make_pcseg(8, 4, 7, 6, 9, 5, 11, 3, 0, 1, 10, 2)

mx1 = pcseg.TwelveToneMatrix(p1)
mx2 = pcseg.TwelveToneMatrix(p2)

t7i = transformations.RO(7, 0, 11)

a1 = [p1, t7i.transform(p1), p2, t7i.transform(p2)]
print(array.str_array(a1))
