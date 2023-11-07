import pctheory.pcset as pcset
import pctheory.pset as pset
import pctheory.pcseg as pcseg
import pctheory.pseg as pseg

base_pseg = pseg.make_pseg24(-10, -2, 11, 18, 19, 24, 12, 15, 16, 20, 4, 3, -3, -10)
base_pcseg = pcseg.make_pcseg24(-10, -2, 11, 18, 19, 24, 12, 15, 16, 20, 4, 3, -3, -10)
base_pcset = pcset.make_pcset24(-10, -2, 11, 18, 19, 24, 12, 15, 16, 20, 4, 3, -3, -10)
# base_sc = pcset.SetClass(base_pcset)
# print(base_sc.name_prime)
# subsets = base_sc.get_abstract_subset_classes()
# subsets = filter(lambda x: len(x) == 3, subsets)
# print(len(list(subsets)))

find_seg = pcseg.make_pcseg24(11, 10, 7)
seg_otos = pcseg.find_otos(base_pcseg, find_seg)
for oto in seg_otos:
    if oto.oto[2] == 1 or oto.oto[2] == 23:
        print(f"{oto}: {oto.transform(base_pcseg)}")
