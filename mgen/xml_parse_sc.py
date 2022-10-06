"""
File: xml_parse_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for parsing MusicXML data into lists of Notes for a SuperCollider piece.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from fractions import Fraction
import music21
from pctheory import pitch

MAP12 = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAP24 = {"C": 0, "D": 4, "E": 8, "F": 10, "G": 14, "A": 18, "B": 22}
PC12 = 12
PC24 = 24


class Dynamic:
    """
    Represents a dynamic object (crescendo, decrescendo, etc.
    """
    def __init__(self, **kwargs):
        self.bus_in = kwargs["bus_in"] if "bus_in" in kwargs else 0                      # input bus index
        self.bus_out = kwargs["bus_out"] if "bus_out" in kwargs else 0                   # output bus index
        self.curves = kwargs["curves"] if "curves" in kwargs else 0                      # curves for the envelope
        self.duration = kwargs["duration"] if "duration" in kwargs else 0                # dynamic duration
        self.end_note = kwargs["end_note"] if "end_note" in kwargs else 0                # end note
        self.end_time = kwargs["end_time"] if "end_time" in kwargs else 0                # end time
        self.levels = kwargs["levels"] if "levels" in kwargs else 0                      # levels for the envelope
        self.measure = kwargs["measure"] if "measure" in kwargs else 0                   # measure number
        self.start_note = kwargs["start_note"] if "start_note" in kwargs else 0          # start note
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else -1         # start time
        self.synth = kwargs["synth"] if "synth" in kwargs else 0                         # the synth to use
        self.times = kwargs["times"] if "times" in kwargs else 0                         # times for the envelope
        self.voice_index = kwargs["voice_index"] if "voice_index" in kwargs else (0, 0)  # index of the affected voice


class Effect:
    """
    Represents an effect object
    """
    def __init__(self, **kwargs):
        self.bus_in = kwargs["bus_in"] if "bus_in" in kwargs else 0                 # input bus index
        self.bus_out = kwargs["bus_out"] if "bus_out" in kwargs else 0              # output bus index
        self.end_note = kwargs["end_note"] if "end_note" in kwargs else 0           # end note
        self.end_time = kwargs["end_time"] if "end_time" in kwargs else 0           # end time
        self.measure = kwargs["measure"] if "measure" in kwargs else 0              # measure number
        self.synth = kwargs["synth"] if "synth" in kwargs else 0                    # the synth to use
        self.duration = kwargs["duration"] if "duration" in kwargs else 0           # effect duration
        self.start_index = kwargs["start_index"] if "start_index" in kwargs else 0  # start index
        self.start_note = kwargs["start_note"] if "start_note" in kwargs else 0     # start note
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else -1    # start time


class Note:
    """
    Represents a note with pitch, duration, and start time
    """
    def __init__(self, **kwargs):
        self.bus_out = kwargs["bus_out"] if "bus_out" in kwargs else 0              # output bus index
        self.buffer = kwargs["buffer"] if "buffer" in kwargs else 0                 # buffer index for granulation
        self.duration = kwargs["duration"] if "duration" in kwargs else 0           # duration
        self.end_time = kwargs["end_time"] if "end_time" in kwargs else 0           # end time
        self.env = kwargs["env"] if "env" in kwargs else "[[][][]]"                 # envelope specification
        self.envlen = kwargs["envlen"] if "envlen" in kwargs else "[[][][]]"        # number of points in envelope
        self.measure = kwargs["measure"] if "measure" in kwargs else 0              # measure number
        self.mul = kwargs["mul"] if "mul" in kwargs else 1                          # mul value
        self.pitch = kwargs["pitch"] if "pitch" in kwargs else None                 # pitch integer
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else 0     # start time
        self.synth = kwargs["synth"] if "synth" in kwargs else 0                    # the synth to use
        self.wait = kwargs["wait"] if "wait" in kwargs else 0                       # the time to wait until next note


class Pan:
    """
    Represents a panning object
    """
    def __init__(self, **kwargs):
        self.bus_in = kwargs["bus_in"] if "bus_in" in kwargs else 0                 # input bus index
        self.measure = kwargs["measure"] if "measure" in kwargs else 0              # measure number
        self.pan2 = kwargs["pan2"] if "pan2" in kwargs else 0                       # pan stereo
        self.panx = kwargs["panx"] if "panx" in kwargs else 0                       # pan multichannel
        self.start_note = kwargs["start_note"] if "start_note" in kwargs else 0     # start note
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else -1    # start time


class Sound:
    """
    Represents a sound
    """
    def __init__(self, **kwargs):
        self.bus_out = kwargs["bus_out"] if "bus_out" in kwargs else 0              # output bus index
        self.buffer = kwargs["buffer"] if "buffer" in kwargs else "\"k\""           # buffer index for granulation
        self.duration = kwargs["duration"] if "duration" in kwargs else 0           # duration
        self.end_time = kwargs["end_time"] if "end_time" in kwargs else 0           # end time
        self.env = kwargs["env"] if "env" in kwargs else "[[][][]]"                 # envelope specification
        self.envlen = kwargs["envlen"] if "envlen" in kwargs else "[[][][]]"        # number of points in envelope
        self.measure = kwargs["measure"] if "measure" in kwargs else 0              # measure number
        self.mul = kwargs["mul"] if "mul" in kwargs else 1                          # mul value
        self.pitch = kwargs["pitch"] if "pitch" in kwargs else None                 # pitch integer
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else 0     # start time
        self.synth = kwargs["synth"] if "synth" in kwargs else "\\play_buf"         # the synth to use
        self.wait = kwargs["wait"] if "wait" in kwargs else 0                       # the time to wait until next note


def analyze_xml(xml_name, part_indices=None):
    """
    Analyzes a MusicXML file and converts it into data useful for SuperCollider
    :param xml_name: The file name
    :param part_indices: The indices of parts to use. If None, extracts all parts.
    :return: An n-dimensional list of Notes
    """
    file_parts = read_file(xml_name)
    return parse_parts(file_parts, part_indices)


def convert_pitch24(pitch21):
    """
    Converts a music21 pitch to a Pitch24 object
    :param pitch21: A music21 pitch
    :return: A Pitch24 object
    """
    note = MAP24[pitch21.step]
    octave = pitch21.octave - 4
    if pitch21.accidental is not None:
        note += int(2 * pitch21.accidental.alter)
    note += PC24 * octave
    return pitch.Pitch24(note)


def dump_parts(new_parts):
    """
    Dumps the new part data for visual inspection
    :param new_parts: New (parsed) parts
    :return:
    """
    current_voice_index = 0
    for part in new_parts:
        for voice in part:
            print(f"Voice {current_voice_index + 1}")
            print("{0: <3}{1: >4}{2: >6}{3: >5}{4: >9}{5: >10}{6: >10}{7: >12}".format("m", "i", "p", "mul", "dur",
                                                                                       "start", "end", "index"))
            for i in range(len(voice)):
                if type(voice[i]) == Note:
                    print("{0: <3}{1: >4}{2: >6}{3: >5}{4: >9}{5: >10}{6: >10}{7: >12}".format(voice[i].measure,
                          i, voice[i].pitch.p, voice[i].mul, round(voice[i].duration, 4),
                          round(voice[i].start_time, 4), round(voice[i].end_time, 4),
                          f"[{current_voice_index}][{i}]"))
                if type(voice[i]) == Sound:
                    print("{0: <3}{1: >4}{2: >6}{3: >5}{4: >9}{5: >10}{6: >10}{7: >12}".format(voice[i].measure,
                          i, "sound", voice[i].mul, round(voice[i].duration, 4),
                          round(voice[i].start_time, 4), round(voice[i].end_time, 4),
                          f"[{current_voice_index}][{i}]"))
            print()
            current_voice_index += 1


def dump_sc(new_parts, score_name):
    """
    Dumps the new part data in SuperCollider format
    :param new_parts: New (parsed) parts
    :param score_name: The name of the score loading function in the SC file
    :return: A list of SuperCollider score files
    """
    score_list = []
    data = f"(\n"
    num_measures_read = 0
    num_measures = get_highest_measure_no(new_parts)

    # Get the number of voices
    num_voices = 0
    for part in new_parts:
        num_voices += len(part)

    data += "~{0} = Array.fill({1}, {2});\n".format(score_name, num_voices, "{List.new}")

    # A list of current starting indices. We add each measure of each voice, then move on to the
    # next measure and add the contents of each voice in that measure
    idx = [0 for i in range(num_voices)]

    # Iterate through all of the measures in the piece
    for measure_no in range(num_measures + 1):
        if num_measures_read > 50:
            data += ")\n"
            score_list.append(data)
            data = f"(\n"
            num_measures_read = 0

        current_voice_index = 0  # The current voice index
        for part in new_parts:
            for voice in part:
                data += f"// Measure {measure_no}, Voice {current_voice_index}\n"
                # For each item in the current measure for the current voice
                for i in range(idx[current_voice_index], len(voice)):
                    # If the flag is false, we have to stop adding things and record the current index
                    # as the starting point for the next measure's iteration
                    flag = False
                    if voice[i].measure == measure_no:
                        flag = True
                    # Provided that we can still add the current item, we continue and add it.
                    if flag:
                        if type(voice[i]) == Note and voice[i].synth == 0:
                            data += f"~dict = Dictionary.new;\n" + \
                                    f"~dict.put(\\i0, {current_voice_index});\n" + \
                                    f"~dict.put(\\i1, {i});\n" + \
                                    f"~dict.put(\\buf0, {voice[i].buffer});\n" + \
                                    f"~dict.put(\\buf1, 1);\n" + \
                                    f"~dict.put(\\duration, {voice[i].duration});\n" + \
                                    f"~dict.put(\\env, {voice[i].env});\n" + \
                                    f"~dict.put(\\envlen, {voice[i].envlen});\n" + \
                                    f"~dict.put(\\measure, {voice[i].measure});\n" + \
                                    f"~dict.put(\\mul, {voice[i].mul});\n" + \
                                    f"~dict.put(\\out, {voice[i].bus_out});\n" + \
                                    f"~dict.put(\\pitch, {voice[i].pitch.p});\n" + \
                                    f"~dict.put(\\start, {voice[i].start_time});\n" + \
                                    f"~dict.put(\\synth, \\synth{voice[i].synth}_{voice[i].envlen});\n" + \
                                    f"~dict.put(\\type, \\Granular);\n" + \
                                    f"~dict.put(\\wait, {voice[i].wait});\n" + \
                                    f"~{score_name}[{current_voice_index}].add(~dict);\n"
                        elif type(voice[i]) == Note and voice[i].synth >= 10:
                            data += f"~dict = Dictionary.new;\n" + \
                                    f"~dict.put(\\i0, {current_voice_index});\n" + \
                                    f"~dict.put(\\i1, {i});\n" + \
                                    f"~dict.put(\\buf, {voice[i].buffer});\n" + \
                                    f"~dict.put(\\mod_curves, {voice[i].mod_curves});\n" + \
                                    f"~dict.put(\\duration, {voice[i].duration});\n" + \
                                    f"~dict.put(\\env, {voice[i].env});\n" + \
                                    f"~dict.put(\\envlen, {voice[i].envlen});\n" + \
                                    f"~dict.put(\\mod_levels, {voice[i].mod_levels});\n" + \
                                    f"~dict.put(\\measure, {voice[i].measure});\n" + \
                                    f"~dict.put(\\mul, {voice[i].mul});\n" + \
                                    f"~dict.put(\\out, {voice[i].bus_out});\n" + \
                                    f"~dict.put(\\pitch, {voice[i].pitch.p});\n" + \
                                    f"~dict.put(\\start, {voice[i].start_time});\n" + \
                                    f"~dict.put(\\synth, \\synth{voice[i].synth}_{voice[i].envlen});\n" + \
                                    f"~dict.put(\\mod_times, {voice[i].mod_times});\n" + \
                                    f"~dict.put(\\type, \\FM);\n" + \
                                    f"~dict.put(\\wait, {voice[i].wait});\n" + \
                                    f"~{score_name}[{current_voice_index}].add(~dict);\n"
                        elif type(voice[i]) == Sound:
                            data += f"~dict = Dictionary.new;\n" + \
                                    f"~dict.put(\\i0, {current_voice_index});\n" + \
                                    f"~dict.put(\\i1, {i});\n" + \
                                    f"~dict.put(\\buf, {voice[i].buffer});\n" + \
                                    f"~dict.put(\\duration, {voice[i].duration});\n" + \
                                    f"~dict.put(\\env, {voice[i].env});\n" + \
                                    f"~dict.put(\\envlen, {voice[i].envlen});\n" + \
                                    f"~dict.put(\\measure, {voice[i].measure});\n" + \
                                    f"~dict.put(\\mul, {voice[i].mul});\n" + \
                                    f"~dict.put(\\out, {voice[i].bus_out});\n" + \
                                    f"~dict.put(\\pitch, {voice[i].pitch.p});\n" + \
                                    f"~dict.put(\\rate, 1);\n" + \
                                    f"~dict.put(\\start, {voice[i].start_time});\n" + \
                                    f"~dict.put(\\synth, {voice[i].synth});\n" + \
                                    f"~dict.put(\\type, \\Sound);\n" + \
                                    f"~dict.put(\\wait, {voice[i].wait});\n" + \
                                    f"~{score_name}[{current_voice_index}].add(~dict);\n"
                        elif type(voice[i]) == Dynamic:
                            data += f"~dict = Dictionary.new;\n" + \
                                    f"~dict.put(\\curves, {voice[i].curves});\n" + \
                                    f"~dict.put(\\duration, {voice[i].duration});\n" + \
                                    f"~dict.put(\\in, {voice[i].bus_in});\n" + \
                                    f"~dict.put(\\levels, {voice[i].levels});\n" + \
                                    f"~dict.put(\\out, {voice[i].bus_out});\n" + \
                                    f"~dict.put(\\start, {voice[i].start_time});\n" + \
                                    f"~dict.put(\\synth, \\dynamic{voice[i].synth});\n" + \
                                    f"~dict.put(\\times, {voice[i].times});\n" + \
                                    f"~dict.put(\\type, \\Dynamic);\n" + \
                                    f"~{score_name}[{current_voice_index}].add(~dict);\n"
                        elif type(voice[i]) == Effect:
                            data += f"~dict = Dictionary.new;\n" + \
                                    f"~dict.put(\\duration, {voice[i].duration});\n" + \
                                    f"~dict.put(\\in, {voice[i].bus_in});\n" + \
                                    f"~dict.put(\\out, {voice[i].bus_out});\n" + \
                                    f"~dict.put(\\start, {voice[i].start_time});\n" + \
                                    f"~dict.put(\\synth, \\effect{voice[i].synth});\n" + \
                                    f"~dict.put(\\type, \\Effect);\n" + \
                                    f"~{score_name}[{current_voice_index}].add(~dict);\n"
                        elif type(voice[i]) == Pan:
                            data += f"~dict = Dictionary.new;\n" + \
                                    f"~dict.put(\\duration, {voice[i].duration});\n" + \
                                    f"~dict.put(\\in, {voice[i].bus_in});\n" + \
                                    f"~dict.put(\\pan2, {voice[i].pan2});\n" + \
                                    f"~dict.put(\\panx, {voice[i].panx});\n" + \
                                    f"~dict.put(\\start, {voice[i].start_time});\n" + \
                                    f"~dict.put(\\type, \\Pan);\n" + \
                                    f"~{score_name}[{current_voice_index}].add(~dict);\n"

                    # If the flag test failed, we will stop adding notes, etc.
                    else:
                        idx[current_voice_index] = i
                        break
                current_voice_index += 1
        num_measures_read += 1

    data += ")\n"
    score_list.append(data)
    return score_list


def dump_sc_to_file(file, new_parts, score_name):
    """
    Writes dumped SC data to a file
    :param file: The file name
    :param new_parts: New (parsed) parts
    :param score_name: The highest numbered measure
    :return:
    """
    scores = dump_sc(new_parts, score_name)
    if len(scores) > 1:
        for i in range(len(scores)):
            with open(f"{file}_{i}.scd", "w") as f:
                f.write(scores[i])
    else:
        with open(f"{file}.scd", "w") as f:
            f.write(scores[0])


def equal_loudness(note):
    """
    Applies an equal loudness effect to a Note
    :param note: A Note
    :return: A mul value
    """
    # 20, 65
    # 50, 35
    # 100, 30 8x
    # 500, 10 2x
    # 1000, 5 1.5x
    # 2000, 0
    # 5000, 5
    # 10000, 15
    note_level = 1
    note_frequency = 440.0 * 2 ** ((note.pitch.p - 18) / 24)

    # apply the equal loudness contour
    if note_frequency < 2000:
        note_level *= (8 * 10 ** -15) * ((-note_frequency + 2000) ** 4.5) + 1
    else:
        note_level *= (1.5 * 10 ** -8) * ((note_frequency - 2000) ** 2) + 1

    # if this is a FM note, decrease the volume
    if note.synth >= 10:
        note_level *= 0.05
    else:
        note_level *= 1

    return note_level


def get_highest_measure_no(parsed_parts):
    """
    Gets the highest measure number in a list of parts
    :param parsed_parts: A list of parsed parts
    :return: The highest measure number
    """
    num_measures = 0
    for part in parsed_parts:
        for voice in part:
            for note in voice:
                if type(note) == Note:
                    if note.measure > num_measures:
                        num_measures = note.measure
    return num_measures


def parse_parts(parts, part_indices=None):
    """
    Parses parts
    :param parts: A list of parts
    :param part_indices: The indices of parts to use. If None, extracts all parts.
    :return:
    """
    new_parts = []  # The new list of parts
    indices = [i for i in range(len(parts))]  # The list of part indices to parse

    # Before we parse any individual parts, we need to scan ALL parts for metronome marks, because they do not
    # necessarily attach to each part separately.
    metronome_marks = {}
    for part in parts:
        next_tempo = 0
        for item in part:
            # The initial tempo might not be in the first measure, so this hack picks it up.
            if type(item) == music21.tempo.MetronomeMark:
                next_tempo = item.number
            elif type(item) == music21.stream.Measure:
                # Record any tempo change that happened in between the end of the previous measure and the beginning of
                # this measure
                if next_tempo and item.number not in metronome_marks:
                    metronome_marks[item.number] = next_tempo
                    next_tempo = 0
                # Iterate through the measure and look for tempo changes that have not been recorded yet
                for item2 in item:
                    if type(item2) == music21.tempo.MetronomeMark and item.number not in metronome_marks:
                        metronome_marks[item.number] = item2.number

    # Get the list of part indices that are being extracted
    if part_indices is not None:
        if type(part_indices) == int:
            indices.clear()
            indices.append(part_indices)
        else:
            indices.clear()
            for i in part_indices:
                indices.append(i)

    # Extract each part separately
    for i in range(len(indices)):
        # new_parts is a 3D list of lists. Hierarchy of new_parts:
        # Level 1: Part
        # Level 2: Voice (for voices in a part)
        # Level 3: Subvoice (for notes in chords). There is one subvoice for each note in a chord.
        new_parts.append([])
        # Tracks the offset position in the part
        part_time_offset = 0
        current_meter = 0
        current_tempo = 0
        current_quarter_duration = 0
        unresolved_ties = []

        for measure in parts[indices[i]]:
            if type(measure) == music21.stream.Measure:
                # If there is a tempo change in this measure, we need to update the tempo
                if measure.number in metronome_marks:
                    current_tempo = Fraction(metronome_marks[measure.number])
                    current_quarter_duration = Fraction(60, current_tempo)
                for item in measure:
                    # If there is a meter change, we need to update the meter
                    if type(item) == music21.meter.TimeSignature:
                        current_meter = Fraction(item.beatCount * item.beatDuration.quarterLength)

                    # If the measure contains voices, not just individual notes or chords, we need to iterate
                    # over each voice
                    if type(item) == music21.stream.Voice:
                        # Add new voices to new_parts if we don't have enough
                        while len(new_parts[i]) < int(item.id):
                            new_parts[i].append([[]])
                        for item2 in item:
                            if type(item2) == music21.chord.Chord:
                                # If this chord has more notes than we've encountered before,
                                # we need to add subvoices.
                                if len(new_parts[i][int(item.id) - 1]) < len(item2.pitches):
                                    for j in range(len(item2.pitches) - len(new_parts[i][int(item.id) - 1])):
                                        new_parts[i][int(item.id) - 1].append([])

                                # Parse each pitch in the chord
                                for p in range(len(item2.pitches)):
                                    n = Note(pitch=convert_pitch24(item2.pitches[p]),
                                             duration=Fraction(item2.duration.quarterLength) * current_quarter_duration,
                                             measure=measure.number,
                                             quarter_duration=Fraction(item2.duration.quarterLength),
                                             start_time=Fraction(part_time_offset + item2.offset * current_quarter_duration))

                                    # If the note is tied, we need to keep track of it
                                    if item2.tie is not None:
                                        if item2.tie.type == "start":
                                            new_parts[i][int(item.id) - 1][p].append(n)
                                            unresolved_ties.append((i, int(item.id) - 1, p,
                                                                    len(new_parts[i][int(item.id) - 1][p]) - 1))
                                        elif item2.tie.type == "continue":
                                            for t in unresolved_ties:
                                                if new_parts[t[0]][t[1]][t[2]][t[3]].pitch == n.pitch:
                                                    new_parts[t[0]][t[1]][t[2]][t[3]].duration += n.duration
                                                    break
                                        else:
                                            delete = -1
                                            for t in range(len(unresolved_ties)):
                                                prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                                if prev.pitch == n.pitch:
                                                    prev.duration += n.duration
                                                    prev.end_time = prev.start_time + prev.duration
                                                    delete = t
                                                    break
                                            if delete > -1:
                                                del unresolved_ties[delete]
                                    else:
                                        n.end_time = n.start_time + n.duration
                                        new_parts[i][int(item.id) - 1][p].append(n)

                            elif type(item2) == music21.note.Note:
                                n = None
                                # Catch special notes that represent nonstandard sounds
                                if item2.notehead == "x":
                                    n = Sound(pitch=convert_pitch24(item2.pitch),
                                              duration=Fraction(item2.duration.quarterLength) *
                                                       current_quarter_duration,
                                              measure=measure.number,
                                              quarter_duration=Fraction(item2.duration.quarterLength),
                                              start_time=Fraction(part_time_offset + item2.offset *
                                                                  current_quarter_duration))
                                else:
                                    n = Note(pitch=convert_pitch24(item2.pitch),
                                             duration=Fraction(item2.duration.quarterLength) * current_quarter_duration,
                                             measure=measure.number,
                                             quarter_duration=Fraction(item2.duration.quarterLength),
                                             start_time=Fraction(part_time_offset + item2.offset *
                                                                 current_quarter_duration))

                                # If the note is tied, we need to keep track of it
                                if item2.tie is not None:
                                    if item2.tie.type == "start":
                                        new_parts[i][int(item.id) - 1][0].append(n)
                                        unresolved_ties.append((i, int(item.id) - 1, 0,
                                                                len(new_parts[i][int(item.id) - 1][0]) - 1))
                                    elif item2.tie.type == "continue":
                                        for t in unresolved_ties:
                                            if new_parts[t[0]][t[1]][t[2]][t[3]].pitch == n.pitch:
                                                new_parts[t[0]][t[1]][t[2]][t[3]].duration += n.duration
                                                break
                                    else:
                                        delete = 0
                                        for t in range(len(unresolved_ties)):
                                            prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                            if prev.pitch == n.pitch:
                                                prev.duration += n.duration
                                                prev.end_time = prev.start_time + prev.duration
                                                delete = t
                                                break
                                        del unresolved_ties[delete]
                                else:
                                    n.end_time = n.start_time + n.duration
                                    new_parts[i][int(item.id) - 1][0].append(n)

                    elif type(item) == music21.chord.Chord:
                        # If this chord has more notes than we've encountered before,
                        # we need to add subvoices.
                        if len(new_parts[i][0]) < len(item.pitches):
                            for j in range(len(item.pitches) - len(new_parts[i][0])):
                                new_parts[i][0].append([])

                        # Parse each pitch in the chord
                        for p in range(len(item.pitches)):
                            n = Note(pitch=convert_pitch24(item.pitches[p]),
                                     duration=Fraction(item.duration.quarterLength) * current_quarter_duration,
                                     measure=measure.number,
                                     quarter_duration=Fraction(item.duration.quarterLength),
                                     start_time=Fraction(part_time_offset + item.offset * current_quarter_duration))

                            # If the note is tied, we need to keep track of it
                            if item.tie is not None:
                                if item.tie.type == "start":
                                    new_parts[i][0][p].append(n)
                                    unresolved_ties.append((i, 0, p, len(new_parts[i][0][p]) - 1))
                                elif item.tie.type == "continue":
                                    for t in unresolved_ties:
                                        if new_parts[t[0]][t[1]][t[2]][t[3]].pitch == n.pitch:
                                            new_parts[t[0]][t[1]][t[2]][t[3]].duration += n.duration
                                            break
                                else:
                                    delete = 0
                                    for t in range(len(unresolved_ties)):
                                        prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                        if prev.pitch == n.pitch:
                                            prev.duration += n.duration
                                            prev.end_time = prev.start_time + prev.duration
                                            delete = t
                                            break
                                    del unresolved_ties[delete]
                            else:
                                n.end_time = n.start_time + n.duration
                                new_parts[i][0][p].append(n)

                    elif type(item) == music21.note.Note:
                        n = None
                        # Catch special notes that represent nonstandard sounds
                        if item.notehead == "x":
                            n = Sound(pitch=convert_pitch24(item.pitch),
                                      duration=Fraction(item.duration.quarterLength) * current_quarter_duration,
                                      measure=measure.number,
                                      quarter_duration=Fraction(item.duration.quarterLength),
                                      start_time=Fraction(part_time_offset + item.offset * current_quarter_duration))
                        else:
                            n = Note(pitch=convert_pitch24(item.pitch),
                                     duration=Fraction(item.duration.quarterLength) * current_quarter_duration,
                                     measure=measure.number,
                                     quarter_duration=Fraction(item.duration.quarterLength),
                                     start_time=Fraction(part_time_offset + item.offset * current_quarter_duration))

                        # If the note is tied, we need to keep track of it
                        if item.tie is not None:
                            if item.tie.type == "start":
                                new_parts[i][0][0].append(n)
                                unresolved_ties.append((i, 0, 0, len(new_parts[i][0][0]) - 1))
                            elif item.tie.type == "continue":
                                for t in unresolved_ties:
                                    if new_parts[t[0]][t[1]][t[2]][t[3]].pitch == n.pitch:
                                        new_parts[t[0]][t[1]][t[2]][t[3]].duration += n.duration
                                        break
                            else:
                                delete = 0
                                for t in range(len(unresolved_ties)):
                                    prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                    if prev.pitch == n.pitch:
                                        prev.duration += n.duration
                                        prev.end_time = prev.start_time + prev.duration
                                        delete = t
                                        break
                                del unresolved_ties[delete]
                        else:
                            n.end_time = n.start_time + n.duration
                            new_parts[i][0][0].append(n)

                # Update how far we've moved
                part_time_offset += current_meter * current_quarter_duration

    # We need to collapse subvoices into voices to make things clearer
    new_parts2 = []
    for part in new_parts:
        part2 = []
        for voice in part:
            for subvoice in voice:
                part2.append(subvoice)
        new_parts2.append(part2)
    return new_parts2


def read_file(input_xml):
    """
    Opens a file and imports music21 data
    :param input_xml:
    :return: The parts in the file
    """
    stream = music21.converter.parse(input_xml)
    parts = []
    for item in stream:
        if type(item) == music21.stream.Part or type(item) == music21.stream.PartStaff:
            parts.append(item)
    return parts


def write_to_file(data, file):
    """
    Writes dumped data to a file
    :param data: The data
    :param file: The file name
    :return:
    """
    with open(file, "w") as f:
        f.write(data)
