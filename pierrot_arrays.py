"""
File: pierrot_arrays.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 2/4/22

This file contains functionality for working with arrays.
"""

from pctheory import array, pcset, pitch

m = [
    [pitch.PitchClass(11), pcset.make_pcset(0, 2, 10, 6), pitch.PitchClass(5), pcset.make_pcset(0, 8, 10, 4),
     pitch.PitchClass(1), pcset.make_pcset(0, 4, 7, 9), pitch.PitchClass(11), pcset.make_pcset(3, 6, 7, 8),
     pitch.PitchClass(1)],
    [pitch.PitchClass(8), pcset.make_pcset(1, 4, 5, 6), pitch.PitchClass(10), pcset.make_pcset(0, 2, 5, 6),
     pitch.PitchClass(9), pcset.make_pcset(1, 3, 4, 10), pitch.PitchClass(5), pcset.make_pcset(0, 1, 2, 7),
     pitch.PitchClass(9)],
    [pitch.PitchClass(5), pcset.make_pcset(8, 9, 2, 7), pitch.PitchClass(1), pcset.make_pcset(8, 11, 6, 7),
     pitch.PitchClass(3), pcset.make_pcset(5, 7, 8, 9), pitch.PitchClass(0), pcset.make_pcset(1, 4, 5, 8),
     pitch.PitchClass(10)],
    [pitch.PitchClass(0), pcset.make_pcset(11, 10, 3, 6), pitch.PitchClass(8), pcset.make_pcset(1, 3, 5, 9),
     pitch.PitchClass(10), pcset.make_pcset(3, 4, 9, 11), pitch.PitchClass(7), pcset.make_pcset(0, 3, 8, 11),
     pitch.PitchClass(5)],
    [pitch.PitchClass(10), pcset.make_pcset(1, 3, 5, 9), pitch.PitchClass(4), pcset.make_pcset(8, 1, 3, 7),
     pitch.PitchClass(11), pcset.make_pcset(0, 3, 6, 8), pitch.PitchClass(10), pcset.make_pcset(2, 6, 9, 11),
     pitch.PitchClass(4)],
    [pitch.PitchClass(4), pcset.make_pcset(11, 2, 10, 7), pitch.PitchClass(0), pcset.make_pcset(9, 2, 10, 5),
     pitch.PitchClass(6), pcset.make_pcset(0, 4, 5, 8), pitch.PitchClass(11), pcset.make_pcset(0, 5, 7, 10),
     pitch.PitchClass(3)],
    [pitch.PitchClass(0), pcset.make_pcset(11, 4, 5, 6), pitch.PitchClass(8), pcset.make_pcset(11, 3, 6, 7),
     pitch.PitchClass(1), pcset.make_pcset(2, 5, 7, 10), pitch.PitchClass(3), pcset.make_pcset(0, 1, 8, 9),
     pitch.PitchClass(5)]
]

m = array.make_array_chain(m, 3, False)
for i in range(len(m)):
    print(m[i])
