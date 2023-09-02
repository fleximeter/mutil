import pctheory.pseg as pseg
import pctheory.pset as pset
from mgen import xml_gen
import os
import numpy as np
import functools

PATH = "G:\My Drive\Transfer\Composition\Compositions\String Quartet"
base_pseg = pseg.make_pseg24(-10, -2, 11, 18, 19, 24, 12, 15, 16, 20, 4, 3, -3, -10)
base_pset = set(base_pseg)
pset_list = [base_pset, pset.transpose(pset.invert(base_pset), 4)]
pseg_list = [base_pseg, [-np.inf, -np.inf], pseg.transpose(pseg.invert(base_pseg), 4)]

# Chord score
score1 = xml_gen.create_score_piano(num_measures=20)
split_chords = [xml_gen.split_pset_for_grand_staff(x) for x in pset_list]
xml_gen.add_sequence(score1[1], xml_gen.make_music21_list([x[0] for x in split_chords], [4 for x in split_chords]))
xml_gen.add_sequence(score1[2], xml_gen.make_music21_list([x[1] for x in split_chords], [4 for x in split_chords]))
# score1.show()
xml_gen.export_to_xml(score1, os.path.join(PATH, "chords.xml"))

# Pseg score
score2 = xml_gen.create_score_piano(num_measures=20)
pseg_list = functools.reduce(lambda z, y :z + y, pseg_list)
xml_gen.add_sequence(score2[1], xml_gen.make_music21_list(pseg_list, [1 for x in pseg_list]))
# score2.show()
xml_gen.export_to_xml(score2, os.path.join(PATH, "psegs.xml"))
