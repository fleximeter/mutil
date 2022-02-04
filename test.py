from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, transformations, util

m = [
    [pitch.PitchClass(11), pcset.make_pcset(9, 10, 4, 5), pitch.PitchClass(1), pcset.make_pcset(11, 10, 3, 6),
     pitch.PitchClass(7), pcset.make_pcset(4, 10, 11, 0), pitch.PitchClass(2), pcset.make_pcset(1, 5, 7, 9),
     pitch.PitchClass(0)],
    [pitch.PitchClass(7), pcset.make_pcset(10, 1, 2, 3), pitch.PitchClass(5), pcset.make_pcset(9, 2, 6, 0),
     pitch.PitchClass(10), pcset.make_pcset(1, 3, 4, 9), pitch.PitchClass(5), pcset.make_pcset(1, 2, 7, 0),
     pitch.PitchClass(9)],
    [pitch.PitchClass(6), pcset.make_pcset(1, 11, 7, 0), pitch.PitchClass(3), pcset.make_pcset(9, 2, 4, 7),
     pitch.PitchClass(11), pcset.make_pcset(3, 6, 9, 10), pitch.PitchClass(1), pcset.make_pcset(4, 8, 9, 11),
     pitch.PitchClass(5)],
    [pitch.PitchClass(3), pcset.make_pcset(9, 4, 5, 7), pitch.PitchClass(0), pcset.make_pcset(10, 5, 6, 7),
     pitch.PitchClass(2), pcset.make_pcset(1, 4, 7, 8), pitch.PitchClass(0), pcset.make_pcset(2, 3, 6, 10),
     pitch.PitchClass(7)],
    [pitch.PitchClass(0), pcset.make_pcset(8, 2, 3, 4), pitch.PitchClass(9), pcset.make_pcset(8, 1, 11, 4),
     pitch.PitchClass(5), pcset.make_pcset(2, 6, 9, 11), pitch.PitchClass(7), pcset.make_pcset(3, 6, 8, 11),
     pitch.PitchClass(1)],
    [pitch.PitchClass(5), pcset.make_pcset(1, 3, 11, 0), pitch.PitchClass(8), pcset.make_pcset(1, 4, 6, 0),
     pitch.PitchClass(9), pcset.make_pcset(1, 3, 5, 10), pitch.PitchClass(4), pcset.make_pcset(2, 9, 10, 11),
     pitch.PitchClass(6)],
    [pitch.PitchClass(11), pcset.make_pcset(1, 5, 6, 9), pitch.PitchClass(0), pcset.make_pcset(11, 10, 3, 5),
     pitch.PitchClass(7), pcset.make_pcset(2, 5, 6, 11), pitch.PitchClass(9), pcset.make_pcset(1, 4, 5, 7),
     pitch.PitchClass(0)]
]

m = array.make_array_chain(m, 2, True)
for i in range(len(m)):
    print(m[i])
