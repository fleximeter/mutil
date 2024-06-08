"""
File: algorithms.py

This file defines some standard compositional algorithms
"""

import mido
import numpy as np
import pctheory.pitch as pitch
import random

MIDI_TEMPO_MULTIPLIER = 1000000
MIDI_TEMPO = 60
_rng = random.Random()


class NoteEnvelope:
    """
    Represents a simple linear note envelope with different points specified.
    It will compute the points in between automatically.
    """
    def __init__(self, ranges, indices) -> None:
        """
        Initializes the NoteEnvelope. The ranges should be in the format
        [(0, 12), (0, 24), (-12, 12), ...] and the indices should be list 
        indices [0, 5, 7, ...]
        :param ranges: A list of range tuples. The first item in each tuple
        is the lowest note in the range, and the second item is the highest
        note in the range.
        :param indices: A list of corresponding indices for the note tuples,
        indicating where that range should be reached
        """
        self.ranges = ranges
        self.indices = indices

    def __call__(self, index):
        """
        Calculates the range for a given index
        :param index: The index
        :return: The range
        """
        # If it's outside the range of indices
        if index < self.indices[0]:
            return self.ranges[0]
        if index > self.indices[-1]:
            return self.ranges[-1]
        
        found_idx = None
        upper_search_idx = len(self.indices) - 1
        lower_search_idx = 0
        
        # Search for the range indices that correspond to the index provided
        while found_idx is None:
            # log(n) searching
            middle_idx = (upper_search_idx - lower_search_idx) // 2 + lower_search_idx
            if self.indices[lower_search_idx] <= index <= self.indices[middle_idx]:
                upper_search_idx = middle_idx
            else:
                lower_search_idx = middle_idx

            # have we found a corresponding index? 
            if self.indices[lower_search_idx] == index:
                found_idx = lower_search_idx
                return self.ranges[found_idx]
            elif self.indices[upper_search_idx] == index:
                found_idx = upper_search_idx
                return self.ranges[found_idx]
            elif lower_search_idx + 1 == upper_search_idx:
                found_idx = lower_search_idx

        # calculate y = mx + b for the upper and lower boundaries
        run = self.indices[found_idx+1] - self.indices[found_idx]
        m1 = (self.ranges[found_idx+1][0] - self.ranges[found_idx][0]) / run
        b1 = self.ranges[found_idx][0] - m1 * self.indices[found_idx]
        m2 = (self.ranges[found_idx+1][1] - self.ranges[found_idx][1]) / run
        b2 = self.ranges[found_idx][1] - m2 * self.indices[found_idx]

        # return the calculated range
        return (round(m1 * index + b1), round(m2 * index + b2))


def make_midi_file(file_name: str, notes, durations, time_signature):
    """
    Makes a MIDI files
    :param file_name: The name of the file
    :param notes: A list of MIDI note numbers. If a note is -1, it will be a rest.
    :param durations: A list of MIDI durations
    :param time_signature: The time signature
    """
    time_signature = [int(i) for i in time_signature.split('/')]
    meta_track = mido.MidiTrack()
    meta_track.append(mido.MetaMessage('time_signature', numerator=time_signature[0], denominator=time_signature[1], clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    meta_track.append(mido.MetaMessage('set_tempo', tempo=MIDI_TEMPO * MIDI_TEMPO_MULTIPLIER // 60, time=0))
    meta_track.append(mido.MetaMessage('key_signature', key='C', time=0))
    meta_track.append(mido.MetaMessage('end_of_track', time=0))
    track1 = mido.MidiTrack()
    track1.append(mido.MetaMessage('track_name', name="Track1", time=0))

    i = 0
    while i < len(notes):
        start_dur = 0
        if notes[i] == -1:
            start_dur = durations[i]
            i += 1
        track1.append(mido.Message('note_on', channel=0, note=notes[i], velocity=64, time=start_dur))
        track1.append(mido.Message('note_off', channel=0, note=notes[i], velocity=0, time=durations[i]))
        i += 1

    track1.append(mido.MetaMessage('end_of_track', time=0))

    mid = mido.MidiFile()
    mid.tracks.append(meta_track)
    mid.tracks.append(track1)
    mid.save(file_name)
    

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
        while current_range[0] > new_note.p + 60: 
            new_note.p += 12
        while current_range[1] < new_note.p + 60: 
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
        while current_range[0] > new_note.p + 60:
            new_note.p += 12
        while current_range[1] < new_note.p + 60:
            new_note.p -= 12
        notes.append(new_note)
    
    return [p.midi for p in notes]
