from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, transformations, util

"""
p1 = pcseg.make_pcseg(6, 9, 5, 8, 4, 7, 1, 10, 2, 11, 3, 0)
p2 = pcseg.make_pcseg(8, 4, 7, 6, 9, 5, 11, 3, 0, 1, 10, 2)

mx1 = pcseg.TwelveToneMatrix(p1)
mx2 = pcseg.TwelveToneMatrix(p2)

t7i = transformations.RO(7, 0, 11)

a1 = [p1, t7i.transform(p1), p2, t7i.transform(p2)]
print(array.str_array(a1))
"""

r = transformations.get_ros()

p1 = pcseg.make_pcseg(4, 9, 7, 11, 8, 6, 2, 0, 3, 5, 10, 1)
m1 = pcseg.TwelveToneMatrix(p1)
# print(m1)

"""
T0   0 5 3 7 4 2 a 8 b 1 6 9
T6   6 b 9 1 a 8 4 2 5 7 0 3
T0R  9 6 1 B 8 A 2 4 7 3 5 0
T6R  3 0 7 5 2 4 8 A 1 9 B 6
T7I  7 2 4 0 3 5 9 B 8 6 1 A
T1I  1 8 A 6 9 B 3 5 2 0 7 4
T7RI A 1 6 8 B 9 5 3 0 4 2 7
T1RI 4 7 0 2 5 3 B 9 6 A 8 1
"""

a1 = [r["T8"].transform(p1), r["T2"].transform(p1), r["T11I"].transform(p1), r["T5I"].transform(p1)]
print(array.str_array(a1))

