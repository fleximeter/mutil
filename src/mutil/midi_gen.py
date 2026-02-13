"""
File: midi_gen.py
"""

import mgen.algorithms as algorithms

QTR = 480

# A virtuosic deep bass line
# dur = QTR // 4
# num_notes = 2000
# path = "data/song1.mid"
# z = algorithms.NoteEnvelope([(-36, -12), (-36, 0), (-24, 0), (-24, -12), (-36, -12), (-36, 0), (-24, 0), (-24, -12)], 
#                             [0, int(num_notes*0.2), int(num_notes*0.4), int(num_notes*0.5), int(num_notes*0.6), int(num_notes*0.8), int(num_notes*0.99)])
# notes = algorithms.wander_nth_int(43, num_notes, 
#                         [2, 4, 5, 7, 11, 14, 16, 17], 
#                         [(9, 9), (7, 4), (7, 3), (5, 3), (3, 2), (3, 1), (3, 1), (3, 1)],
#                         z,
#                         5,
#                         4)
# algorithms.stochastic_add_rests(notes, 15, 10)
# durations = algorithms.rubato(notes, dur, dur * 0.02)
# algorithms.make_midi_file(path, notes, durations, "4/4")


# A virtuosic high line
dur = QTR // 4
num_notes = 2000
path = "data\\song5.mid"
z = algorithms.NoteEnvelope([(36, 48), (36, 55), (48, 60), (57, 60), (43, 55), (36, 55), (36, 48)], 
                            [0, int(num_notes*0.2), int(num_notes*0.35), int(num_notes*0.45), int(num_notes*0.6), int(num_notes*0.75), int(num_notes)])
notes = algorithms.wander_nth_int(65, num_notes, 
                        [0, 2, 4, 6, 11, 17], 
                        [(7, 7), (7, 5), (3, 2), (2, 2), (7, 5), (5, 4)],
                        z,
                        5,
                        6)
algorithms.stochastic_add_rests(notes, 15, 10)
durations = algorithms.rubato(notes, dur, dur * 0.02)
algorithms.make_midi_file(path, notes, durations, "4/4")
