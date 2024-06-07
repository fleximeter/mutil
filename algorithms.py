"""
File: algorithms.py

This file defines some standard compositional algorithms
"""

import numpy as np
import pctheory.pitch as pitch
import pctheory.pcset as pcset
import pctheory.pcseg as pcseg
import pctheory.transformations as transformations
import random

_rng = random.Random()


class NoteEnvelope:
    """
    Represents a simple linear note envelope with different points specified.
    It will compute the points in between automatically.
    """
    def __init__(self, ranges, indices) -> None:
        self.ranges = ranges
        self.indices = indices

    def __call__(self, index):
        if index < self.indices[0]:
            return self.ranges[0]
        if index > self.indices[-1]:
            return self.ranges[-1]
        found_idx = None
        upper_search_idx = len(self.indices) - 1
        lower_search_idx = 0
        while found_idx is None:
            middle_idx = (upper_search_idx - lower_search_idx) // 2 + lower_search_idx
            if self.indices[lower_search_idx] <= index <= self.indices[middle_idx]:
                upper_search_idx = middle_idx
            else:
                lower_search_idx = middle_idx 
            if self.indices[lower_search_idx] == index:
                found_idx = lower_search_idx
                return self.ranges[found_idx]
            elif self.indices[upper_search_idx] == index:
                found_idx = upper_search_idx
                return self.ranges[found_idx]
            elif lower_search_idx + 1 == upper_search_idx:
                found_idx = lower_search_idx
        run = self.indices[found_idx+1] - self.indices[found_idx]
        m1 = (self.ranges[found_idx+1][0] - self.ranges[found_idx][0]) / run
        b1 = self.ranges[found_idx][0] - m1 * self.indices[found_idx]
        m2 = (self.ranges[found_idx+1][1] - self.ranges[found_idx][1]) / run
        b2 = self.ranges[found_idx][1] - m1 * self.indices[found_idx]
        return (round(m1 * index + b1), round(m2 * index + b2))


def rubato(note_list: list, mean_dur=480, stdev=1):
    """
    Stochastically adds rests to a MIDI track, approximately every N notes, using a normal
    distribution
    :param note_list: The track to add rests to
    :param mean: The mean rest interval
    :param stdev: The standard deviation
    :return: A list of durations
    """
    return [int(x) for x in np.random.normal(mean_dur, stdev, len(note_list)).tolist()]
    

def stochastic_add_rests(note_list: list, mean=15, stdev=5):
    """
    Stochastically adds rests to a MIDI track, approximately every N notes, using a normal
    distribution
    :param note_list: The track to add rests to
    :param mean: The mean rest interval
    :param stdev: The standard deviation
    """
    next_rest = int(np.random.normal(mean, stdev, 1)[0])
    next_rest = max(next_rest, 1)
    while next_rest < len(note_list):
        note_list.insert(next_rest, -1)
        next_interval = int(np.random.normal(mean, stdev, 1)[0])
        next_interval = max(next_interval, 1)
        next_rest += 1 + next_interval


def wander(start_note: int, num_notes: int, intervals: list, weights: list, note_range):
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
        current_range = note_range(i)
        while current_range[0] > new_note.p: 
            new_note.p += 12
        while current_range[1] < new_note.p: 
            new_note.p -= 12
        notes.append(new_note)
    
    return [p.midi for p in notes]


def wander_nth_int(start_note: int, num_notes: int, intervals: list, weights: list, note_range, nth_interval=5, n=5):
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
        current_range = note_range(i)
        while current_range[0] > new_note.p: 
            new_note.p += 12
        while current_range[1] < new_note.p: 
            new_note.p -= 12
        notes.append(new_note)
    
    return [p.midi for p in notes]
