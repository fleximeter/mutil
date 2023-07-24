"""
Name: clarinet_set_finder.py
Author: Jeff Martin
Date: 12/23/22

Description:
This program is a set finder that is limited to exploring
only the operators in a specific group.
"""

from pctheory import group, pcseg, pcset, pitch, set_complex, tables, transformations

# The root set from which subsets are extracted
root_set = pcset.make_pcset24(0, 1, 5, 9, 10, 11, 15, 19)
root_sc = pcset.SetClass24(root_set)
root_subset_classes = root_sc.get_abstract_subset_classes()

utos = transformations.get_utos24()

# Make the Tn/TnI group that maps U_e and U_o to themselves
utos_clarinet = {}
utos_clarinet_list = []
for i in range(0, 24, 2):
    utos_clarinet[f"T{i}"] = transformations.UTO(i)
    utos_clarinet[f"T{i}I"] = transformations.UTO(i, 23)
for u in utos_clarinet:
    utos_clarinet_list.append(utos_clarinet[u])
grp = group.OperatorGroup(utos_clarinet_list, 24)

print(grp.name)
print(utos["T5M1"] in grp)

for uto in grp:
    print(uto)
