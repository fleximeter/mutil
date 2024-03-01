from pctheory.pcseg import make_pcseg12, transform, transform_hstack

pcseg1 = make_pcseg12(0, 3, 5, 1, 5, 0, 3)
pcseg2 = make_pcseg12(0, 1, 5, 3, 0, 3, 5)

transf = [
    "T5Ir5",
    "T7Ir5",
]

for t in transf:
    print(t, transform(pcseg1, t))

for t in transf:
    print(t, transform(pcseg2, t))

print(transform_hstack(pcseg1, transf))
