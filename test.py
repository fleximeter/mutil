from pctheory import pcseg, pcset, pseg, pset, pitch, transformations

ros = transformations.get_otos12()
otos24 = transformations.get_otos24()

x = pcseg.generate_random_all_trichord_row()
print(x)
print(otos24["T5I"].transform(x))
