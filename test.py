from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

ttos = transformations.get_ttos24()
list1 = [5, 7, 11, 13, 17, 19, 23]

for i in range(0, 24, 2):
    for j in range(len(list1)):
        for k in range(0, 24, 2):
            for l in range(len(list1)):
                t = transformations.left_multiply_ttos(ttos[f"T{i}M{list1[j]}"], ttos[f"T{k}"], num_pcs=24)
                u = transformations.left_multiply_ttos(ttos[f"T{i}"], ttos[f"T{k}M{list1[l]}"], num_pcs=24)
                v = transformations.left_multiply_ttos(ttos[f"T{i}"], ttos[f"T{k}"], num_pcs=24)
                w = transformations.left_multiply_ttos(ttos[f"T{i}M{list1[j]}"], ttos[f"T{k}M{list1[l]}"], num_pcs=24)
                if t[0] % 2 != 0 or t[1] % 2 == 0:
                    print(t)
                if u[0] % 2 != 0 or u[1] % 2 == 0:
                    print(u)
                if v[0] % 2 != 0 or v[1] % 2 == 0:
                    print(v)
                if w[0] % 2 != 0 or w[1] % 2 == 0:
                    print(w)

# a test comment here
