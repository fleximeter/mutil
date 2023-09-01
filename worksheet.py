import music21
import mgen.xml_gen as xml_gen
import random

chords = set()
base_pitches = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
accidentals = ['--', '-', '', '#', '##']
registers = [4, 5]

for reg in registers:
    for pitch in base_pitches:
        for acc in accidentals:
            base_pitch = f"{pitch}{acc}{reg}"
            for reg1 in registers:
                for pitch1 in base_pitches:
                    for acc1 in accidentals:
                        other_pitch = f"{pitch1}{acc1}{reg1}"
                        chords.add(music21.chord.Chord([music21.pitch.Pitch(base_pitch), music21.pitch.Pitch(other_pitch)], quarterLength=4))

chords = list(chords)
NUM_CHORDS = 100
selected = 0

def weighted_coin_toss(prob_heads):
    choices = [1, 0]
    weights = [prob_heads, 1 - prob_heads]
    
    result = random.choices(choices, weights=weights, k=1)
    return result[0]

def contains_weird_accidental(chord):
    for note in chord.pitches:
        if note.name in {'C-', 'F-', 'E#', 'B#', 'c-', 'f-', 'e#', 'b#'}:
            return True
        elif note.accidental:
            if abs(note.accidental.alter) > 1:
                return True
    return False

chosen_chords = []

while selected < NUM_CHORDS:
    i = random.randrange(0, len(chords))
    if not contains_weird_accidental(chords[i]) or weighted_coin_toss(0.001):
        chosen_chords.append(chords[i])
        del chords[i]
        selected += 1

lyrics = []
for chord in chosen_chords:
    interval = music21.interval.Interval(pitchStart=chord.pitches[0], pitchEnd=chord.pitches[1])
    lyrics.append(interval.name)

s = xml_gen.create_score("Worksheet")
xml_gen.add_instrument(s, "Violin", "Vln.")
xml_gen.add_measures(s, NUM_CHORDS, 1, None, '4/4')
xml_gen.add_sequence(s[1], chosen_chords, lyrics)
xml_gen.export_to_xml(s, "D:\\sample_worksheet.xml")
