from pctheory import pcseg, pcset, pseg, pset, pitch, transformations

ros = transformations.get_otos12()

x = pcseg.generate_random_all_trichord_row()
print(x)
print(pcseg.imb_n(x, 3))
print(ros["T5I"].transform(x))
