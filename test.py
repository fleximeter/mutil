from pctheory import pcseg, pcset, pseg, pset, pitch, transformations
from mgen import xml_gen
import music21

base_sc = pcset.get_all_combinatorial_hexachord("C")
print(base_sc)

# generate 10 different spacings of the chord
realizations = pset.generate_random_pset_realizations(base_sc.pcset, -12, 12, 10)

score = xml_gen.create_score_piano(num_measures=10)
score.show()
