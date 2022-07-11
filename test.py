from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources
import simpleaudio as sa
import numpy as np


def play_chord(chord: set):
    freqs = [440 * 2 ** ((p.midi - 69) / 12) for p in chord]
    sample_rate = 44100  # 44.1 kHz
    time = 2.0  # seconds
    num_samples = int(time * sample_rate)
    print(num_samples)
    time_arr = np.linspace(0, time, num_samples, False)  # an array of time points from 0 to t
    notes = [np.sin(freqs[i] * time_arr * 2 * np.pi) for i in range(len(freqs))]  # create buffer for each note
    output = np.zeros((num_samples, 2))
    for i in range(len(notes)):
        output[0:num_samples, 0] += notes[i]
        output[0:num_samples, 1] += notes[i]
    output *= 32767 / np.max(np.abs(output))
    output = output.astype(np.int16)
    play_obj = sa.play_buffer(output, 1, 2, sample_rate)
    play_obj.wait_done()


ps = pset.make_pset12(0)
for p in ps:
    print(440 * 2 ** ((p.midi-69)/12))
play_chord(ps)
