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
    A wandering algorithm. You specify the starting pitch, a list of possible intervals,
    and a list of possible weight tuples. Each weight tuple corresponds to an interval:
    the first item in the tuple is the weighted probability that we can use this interval
    ascending; the second item is the weighted probability that we can use this interval
    descending. All weights are global - in relation to the weights for all other intervals.
    The algorithm will use randomness to wander around, choosing the next interval with a
    weighted random process.
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


def wander_nth_int(start_note=60, num_notes=200, intervals=[], weights=[], note_range=(0, 36), nth_interval=5, n=5):
    """
    A wandering algorithm, where the nth interval is always a specified interval. 
    It will go up or down randomly for this interval.
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
        if i % n == 0:
            new_int = _rng.choice([nth_interval, -nth_interval])
        else:
            new_int = _rng.choices(intervals, weights, k=1)[0]
        new_note = pitch.Pitch(notes[-1].p + new_int)
        while note_range[0] > new_note.p: 
            new_note.p += 12
        while note_range[1] < new_note.p: 
            new_note.p -= 12
        notes.append(new_note)
    
    return [p.midi for p in notes]
