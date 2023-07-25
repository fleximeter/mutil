from pctheory import pcseg, pcset, pseg, pset, pitch, transformations

utos24 = transformations.get_utos24()

base_sc = pcset.SetClass(pcset.make_pcset24(0, 2, 10, 14, 15), 24)

print(base_sc.pcset)
print(base_sc.mod)
print(base_sc.name_prime)
print(base_sc.ic_vector)
