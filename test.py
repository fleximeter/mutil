from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction

s1 = pcset.make_pcset24([n for n in range(24)])
sc1 = pcset.SetClass24(s1)
s_classes = sc1.get_subset_classes()
s_classes = list(s_classes)
s_classes.sort()
sorted(s_classes, key=lambda x: len(x))

data = "{\n  \"setPrimeForms24\": [\n"
for s in s_classes:
    data += f"    \"{s}\",\n"
data += "  ]\n}"
with open("temp.json", "w") as f:
    f.write(data)
