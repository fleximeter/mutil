import mido
import algorithms

QTR = 480
TEMPO_MULTIPLIER = 1000000
TEMPO = 60
DUR = QTR // 4

notes = algorithms.wander_nth_int(48, 2000, 
                          [2, 4, 5, 7, 9, 11, 14, 16, 17], 
                          [(9, 9), (7, 4), (7, 3), (4, 3), (3, 2), (4, 2), (3, 1), (3, 1), (3, 1)],
                          (-48, -12),
                          5,
                          4)

meta_track = mido.MidiTrack()
meta_track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
meta_track.append(mido.MetaMessage('set_tempo', tempo=TEMPO * TEMPO_MULTIPLIER // 60, time=0))
meta_track.append(mido.MetaMessage('key_signature', key='C', time=0))
meta_track.append(mido.MetaMessage('end_of_track', time=0))
track1 = mido.MidiTrack()
track1.append(mido.MetaMessage('track_name', name="Track1", time=0))

for note in notes:
    track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
    track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=DUR))

track1.append(mido.MetaMessage('end_of_track', time=0))

mid = mido.MidiFile()
mid.tracks.append(meta_track)
mid.tracks.append(track1)
mid.save("data/song.mid")
