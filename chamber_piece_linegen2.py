# line generator for chamber orchestra piece

from mgen import xml_gen
from pctheory import pitch
from mgen.comptools import multiply, rotate
import music21

score = xml_gen.create_score("Line Generator", "Jeff Martin")
xml_gen.add_instrument(score, "Cello", "Vc.")
xml_gen.add_measures(score, 50, 1, None, "4/4")
xml_gen.add_item(score[1], music21.clef.BassClef(), 1)

# the 4 forms of the basic sequence of pitch intervals
seq = {
    'p': [-2, 1, -4, 1, 5, -1, 2, -5]
}
seq['r'] = seq['p'].copy()
seq['r'].reverse()
seq['i'] = multiply(seq['p'], -1)
seq['ri'] = seq['i'].copy()
seq['ri'].reverse()

int_seq = seq['p'] + seq['p'] + seq['i'] + rotate(seq['p'], 2) + seq['p'] + seq['r']

# build the sequence with a starting pitch
seq_builder = [pitch.Pitch(45)]

# the sequence length
LENGTH = 100

# add the notes in
for i in range(LENGTH):
    seq_builder.append(pitch.Pitch(seq_builder[-1].p + int_seq[i%len(int_seq)]))
rhythm = [1 for i in range(len(seq_builder))]
mseq = xml_gen.make_music21_list(seq_builder, rhythm)
xml_gen.add_sequence(score[1], mseq)
xml_gen.remove_empty_measures(score)
xml_gen.export_to_xml(score, "data/score2.musicxml")
score.show()
