"""
Name: pset_realizer.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 7/24/23

This file contains functionality for realizing psets in scores.
"""

from pctheory import pcset, pset
from mgen import xml_gen

# We'll generate several different realizations of this pcset within a specified registral range
base_set = pcset.make_pcset12(0, 1, 2, 4, 7, 8)
LOWEST_NOTE = -24
HIGHEST_NOTE = 24
NUM_DUPLICATE_PITCHES = 4
NUM_CHORDS = 10

# only include psets that don't have large intervals
def filter_func(x):
    pseg = list(x)
    pseg.sort()
    for i in range(1, len(pseg)):
        if pseg[i].p - pseg[i-1].p > 11:
            return False
    return True

realizations = pset.generate_random_pset_realizations(base_set, LOWEST_NOTE, HIGHEST_NOTE, NUM_CHORDS, NUM_DUPLICATE_PITCHES, filter_func)

# Split the chord for rendering on a grand staff
for i, chord in enumerate(realizations):
    realizations[i] = xml_gen.split_pset_for_grand_staff(chord)
top_staff = [chord[0] for chord in realizations]
bottom_staff = [chord[1] for chord in realizations]

# Generate music21 objects for positioning the chords on the staves
durations = [4 for i in range(NUM_CHORDS)]
m21_list_top = xml_gen.make_music21_list(top_staff, durations)
m21_list_bottom = xml_gen.make_music21_list(bottom_staff, durations)

# Create the score and add the chords
score = xml_gen.create_score_piano(num_measures=NUM_CHORDS)
xml_gen.add_sequence(score[1], m21_list_top)
xml_gen.add_sequence(score[2], m21_list_bottom)

score.show()
