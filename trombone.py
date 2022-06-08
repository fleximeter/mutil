from pctheory import pcseg, pcset, pitch, set_complex, tables, transformations

s1 = pcset.make_pcset24(0, 1, 9, 10, 17, 20)  # this is T1I of the prime form
sc1 = pcset.SetClass24(s1)
sp = list(sc1.get_subset_classes())
sp.sort()

for s in sp:
    print("{0: <25}{1}".format(s.name_prime, s.ic_vector_string))

pcset.make_subset_graph(sc1)
"""
Hexachord: [00, 01, 05, 08, 15, 16]

Selection of SCs w/o ic11, ic12 (tritone, qflat tritone)

Only 2 pentachords
[00, 01, 05, 08, 15] 
[00, 01, 08, 15, 16]


tl = [52.5, 60, 70, 84, 105]
t = tempo.plot_tempo_table(tl)

"""