"""
Name: m21.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 7/9/22

This file contains functions for working with music21 and pctheory.
"""

import music21
import pctheory.pitch

def m21_make_pseg(item):
    """
    Makes a pseg from a music21 object
    :param item: A music21 object
    :return: A pseg
    """
    pseg2 = []
    if type(item) == music21.note.Note:
        pseg2.append(pctheory.pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.pitch.Pitch:
        pseg2.append(pctheory.pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.chord.Chord:
        for p in item.pitches:
            pseg2.append(pctheory.pitch.Pitch12(p.midi - 60))
    else:
        raise TypeError("Unsupported music21 type")
    return pseg2
