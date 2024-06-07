"""
File: midi_gen.py
"""

import mido
import algorithms

QTR = 480
TEMPO_MULTIPLIER = 1000000
TEMPO = 60
DUR = QTR // 4

z = algorithms.NoteEnvelope([(0, 12), (0, 24), (12, 36)], [0, 400, 1400])

notes = algorithms.wander_nth_int(65, 2000, 
                          [2, 4, 5, 7, 11, 14, 16, 17], 
                          [(9, 9), (7, 4), (7, 3), (5, 3), (3, 2), (3, 1), (3, 1), (3, 1)],
                          z,
                          5,
                          4)
algorithms.stochastic_add_rests(notes, 15, 10)
durations = algorithms.rubato(notes, DUR, DUR * 0.02)

meta_track = mido.MidiTrack()
meta_track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
meta_track.append(mido.MetaMessage('set_tempo', tempo=TEMPO * TEMPO_MULTIPLIER // 60, time=0))
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
mid.save("data/song.mid")
