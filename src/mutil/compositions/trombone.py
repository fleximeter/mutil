"""
File: trombone.py
Date: 3/1/24

This file contains functionality for CAC in a trombone piece
"""

from pctheory.pcseg import make_pcseg12, transform, transform_hstack
from pctheory.pitch import Pitch
from mgen import xml_gen
from music21.clef import BassClef
import numpy as np

pcseg1 = make_pcseg12(0, 3, 5, 1, 5, 0, 3)
pcseg2 = make_pcseg12(0, 1, 5, 3, 0, 3, 5)

transf = [
    "T5Ir5",
    "T7Ir5",
]

seg = transform_hstack(pcseg1, transf)

for t in transf:
    print(t, transform(pcseg1, t))
for t in transf:
    print(t, transform(pcseg2, t))
print(seg)

seg_p = [Pitch(pc.pc - 12) for pc in seg]

score = xml_gen.create_score("Trombone Draft")
xml_gen.add_instrument(score, "Bass Trombone", "B. Tbn.")
xml_gen.add_measures(score, 4, meter="4/4")
xml_gen.add_item(score[1], BassClef(), 1)
xml_gen.add_sequence(score[1], xml_gen.make_music21_list(seg_p, [1/2 for i in range(len(seg_p))]))
score.show()
