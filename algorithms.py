"""
File: algorithms.py

This file defines some standard compositional algorithms
"""

import pctheory.pitch as pitch
import pctheory.pcset as pcset
import pctheory.pcseg as pcseg
import pctheory.transformations as transformations
import random

_rng = random.Random()


def wander(start_note=60, num_notes=200, intervals=[], weights=[], note_range=(0, 36)):
    """
    A wandering algorithm
    :param start_note: The first note
    :param num_notes: The number of notes to generate
    :param intervals: A list of intervals (negative versions will be added automatically)
    :param weights: A list of weight tuples. The first number in the tuple is the weight 
    for the ascending interval, and the second number is the weight for the descending 
    interval.
    :param note_range: A tuple consisting of the lowest allowed note and the highest 
    allowed note
    :return: A list of MIDI notes
    """
    intervals += [-i for i in intervals]
    weights = [w[0] for w in weights] + [w[1] for w in weights]
    start_note -= 60
    notes = [pitch.Pitch(start_note)]
    for i in range(num_notes - 1):
        new_int = _rng.choices(intervals, weights, k=1)[0]
        new_note = pitch.Pitch(notes[-1].p + new_int)
        while note_range[0] > new_note.p: 
            new_note.p += 12
        while note_range[1] < new_note.p: 
            new_note.p -= 12
        notes.append(new_note)
    
    return [p.midi for p in notes]
