# line generator for chamber orchestra piece

from mgen import xml_gen
from pctheory import pitch, pcset, pcseg, pset, pseg

score = xml_gen.create_score("Line Generator", "Jeff Martin")
xml_gen.add_instrument(score, "Violin", "Vln.")
xml_gen.add_measures(score, 20, 1, None, "4/4")

# the sequence of pitch intervals
int_seq = [-2, 1, 2, -3, -2, 1, 3, -4, 3]

# the original note sequence
# orig_seq = pseg.make_pseg12(88, 86, 87, 89, 86, 84, 85, 88, 84, 87)

# build the sequence with a starting pitch
seq_builder = [pitch.Pitch(88)]

# the sequence length
LENGTH = 30

# add the notes in
for i in range(LENGTH):
    seq_builder.append(pitch.Pitch(seq_builder[-1].p + int_seq[i%len(int_seq)]))
rhythm = [1 for i in range(len(seq_builder))]
mseq = xml_gen.make_music21_list(seq_builder, rhythm)
xml_gen.add_sequence(score[1], mseq)

score.show()
