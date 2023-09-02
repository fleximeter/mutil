import pctheory.pseg as pseg
import pctheory.pset as pset
from mgen import xml_gen

base_pset = pseg.make_pseg24(-10, -2, 11, 18, 19, 24, 12, 15, 16, 20, 4, 3, -3, -10)
base_pset = set(base_pset)
pset_list = [base_pset, pset.transpose(pset.invert(base_pset), 14)]

score = xml_gen.create_score_piano(num_measures=20)
split_chords = [xml_gen.split_pset_for_grand_staff(x) for x in pset_list]
xml_gen.add_sequence(score[1], xml_gen.make_music21_list([x[0] for x in split_chords], [4 for x in split_chords]))
xml_gen.add_sequence(score[2], xml_gen.make_music21_list([x[1] for x in split_chords], [4 for x in split_chords]))
score.show()
