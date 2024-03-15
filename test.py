import pctheory.pitch as pitch
import pctheory.pcset as pcset
import pctheory.pcseg as pcseg
import pctheory.transformations as transformations

pcseg1 = pcseg.make_pcseg12(0, 3, 5, 1, 5, 0, 3)
pcseg2 = pcseg.make_pcseg12(0, 1, 5, 3, 0, 3, 5)

pcseg3 = pcseg.make_pcseg12(0, 3)

t = transformations.find_otos(pcseg1, pcseg3)
print(t)
