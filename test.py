from pctheory import pcseg, pcset, pseg, pset, pitch, transformations
from pctheory.pcseg import transform

pcseg1 = pcseg.make_pcseg12(0, 3, 5, 1, 5, 0, 3)
pcseg2 = pcseg.make_pcseg12(0, 1, 5, 3, 0, 3, 5)

transf = [
    "T5Ir5",
    "T5Ir5",
]

for t in transf:
    print(t, transform(pcseg1, t))

for t in transf:
    print(t, transform(pcseg2, t))
