import pctheory.pitch as pitch
import pctheory.pcset as pcset
import pctheory.pcseg as pcseg
import pctheory.transformations as transformations

pcseg1 = pcseg.make_pcseg12(0, 3, 5, 1, 5, 0, 3)
pcseg2 = pcseg.make_pcseg12(0, 1, 5, 3, 0, 3, 5)
pcs = pcset.make_pcset12(0, 1, 3, 5)

t = transformations.find_utos(pcs, pcset.make_pcset12(7, 10))
print(t)
for x in t:
    print(x, x.transform(pcs))

print(pitch.PitchClass(0) in pcs)

