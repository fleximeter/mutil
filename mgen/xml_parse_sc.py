"""
File: xml_parse_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for parsing MusicXML data into lists of Notes for a SuperCollider piece.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from fractions import Fraction
import music21
from pctheory import pitch, pcseg, pcset

LEVELS = {-5: 0.2, -4: 0.28, -3: 0.36, -2: 0.44, -1: 0.52, 0: 0.6, 1: 0.68, 2: 0.76, 3: 0.84, 4: 0.92, 5: 1.0}
MAP12 = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAP24 = {"C": 0, "D": 4, "E": 8, "F": 10, "G": 14, "A": 18, "B": 22}
PC12 = 12
PC24 = 24


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
        self.synth = kwargs["synth"] if "synth" in kwargs else 0  # the synth to use


class Dynamic:
    """
    Represents a dynamic object (crescendo, decrescendo, etc.
    """
    def __init__(self, **kwargs):
        self.bus_in = kwargs["bus_in"] if "bus_in" in kwargs else 0                 # input bus index
        self.bus_out = kwargs["bus_out"] if "bus_out" in kwargs else 0              # output bus index
        self.synth = kwargs["synth"] if "synth" in kwargs else 0     # the synth to use
        self.duration = kwargs["duration"] if "duration" in kwargs else 0           # dynamic duration
        self.end_level = kwargs["end_level"] if "end_level" in kwargs else 0        # end volume index
        self.start_level = kwargs["start_level"] if "start_level" in kwargs else 0  # start volume index
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else -1    # start time


class Effect:
    """
    Represents an effect object
    """
    def __init__(self, **kwargs):
        self.bus_in = kwargs["bus_in"] if "bus_in" in kwargs else 0                 # input bus index
        self.bus_out = kwargs["bus_out"] if "bus_out" in kwargs else 0              # output bus index
        self.synth = kwargs["synth"] if "synth" in kwargs else 0                    # the synth to use
        self.duration = kwargs["duration"] if "duration" in kwargs else 0           # effect duration
        self.start_index = kwargs["start_index"] if "start_index" in kwargs else 0  # start index
        self.start_time = kwargs["start_time"] if "start_time" in kwargs else -1    # start time


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
    Dumps the new part data
    :param new_parts: New (parsed) parts
    :return:
    """
    for p in new_parts:
        for v in range(len(p)):
            for v2 in range(len(p[v])):
                print(f"Voice {v + 1}.{v2 + 1}")
                print("{0: <3}{1: >4}{2: >5}{3: >5}{4: >9}{5: >10}{6: >10}".format("m", "i", "p", "mul", "dur",
                                                                                   "start", "end"))
                for i in range(len(p[v][v2])):
                    if type(p[v][v2][i]) == Note:
                        print("{0: <3}{1: >4}{2: >5}{3: >5}{4: >9}{5: >10}{6: >10}".format(p[v][v2][i].measure, i,
                              p[v][v2][i].pitch.p, p[v][v2][i].mul, round(float(p[v][v2][i].duration), 4),
                              round(float(p[v][v2][i].start_time), 4), round(float(p[v][v2][i].end_time), 4)))
                print()


def dump_sc(new_parts):
    """
    Dumps the new part data in SuperCollider format
    :param new_parts: New (parsed) parts
    :return:
    """
    data = "(\n"
    num_measures = get_highest_measure_no(new_parts)

    # Get the number of voices
    num_voices = 0
    for p in new_parts:
        for v in p:
            num_voices += len(v)

    data += "~score = Array.fill({0}, {1});\n".format(num_voices, "{List.new}")

    idx = [0 for i in range(num_voices)]
    for i in range(num_measures + 1):
        cidx = 0
        for p in new_parts:
            for v in p:
                for v2 in v:
                    data += f"// Measure {i}, Voice {cidx}\n"
                    for j in range(idx[cidx], len(v2)):
                        flag = False
                        if type(v2[j]) == Dynamic:
                            if v2[j + 1].measure == i:
                                flag = True
                        elif v2[j].measure == i:
                            flag = True
                        if flag:
                            if type(v2[j]) == Note:
                                data += f"d = Dictionary.new;\n" + \
                                        f"d.put(\\buf, {v2[j].buffer});\n" + \
                                        f"d.put(\\duration, {float(v2[j].duration)});\n" + \
                                        f"d.put(\\env, {v2[j].env});\n" + \
                                        f"d.put(\\envlen, {v2[j].envlen});\n" + \
                                        f"d.put(\\measure, {v2[j].measure});\n" + \
                                        f"d.put(\\mul, {equal_loudness(v2[j])});\n" + \
                                        f"d.put(\\out, {v2[j].bus_out});\n" + \
                                        f"d.put(\\pitch, {v2[j].pitch.p});\n" + \
                                        f"d.put(\\start, {float(v2[j].start_time)});\n" + \
                                        f"d.put(\\synth, \\synth{v2[j].synth}_{v2[j].envlen});\n" + \
                                        f"d.put(\\type, \\Note);\n" + \
                                        f"~score[{cidx}].add(d);\n"
                            elif type(v2[j]) == Dynamic:
                                data += f"d = Dictionary.new;\n" + \
                                        f"d.put(\\duration, {v2[j].duration});\n" + \
                                        f"d.put(\\end_level, {v2[j].end_level});\n" + \
                                        f"d.put(\\in, {v2[j].bus_in});\n" + \
                                        f"d.put(\\out, {v2[j].bus_out});\n" + \
                                        f"d.put(\\start, {float(v2[j].start_time)});\n" + \
                                        f"d.put(\\start_level, {v2[j].start_level});\n" + \
                                        f"d.put(\\synth, \\dynamic{v2[j].synth});\n" + \
                                        f"d.put(\\type, \\Dynamic);\n" + \
                                        f"~score[{cidx}].add(d);\n"
                            elif type(v2[j]) == Effect:
                                data += f"d = Dictionary.new;\n" + \
                                        f"d.put(\\duration, {v2[j].duration});\n" + \
                                        f"d.put(\\in, {v2[j].bus_in});\n" + \
                                        f"d.put(\\out, {v2[j].bus_out});\n" + \
                                        f"d.put(\\start, {float(v2[j].start_time)});\n" + \
                                        f"d.put(\\synth, \\effect{v2[j].synth});\n" + \
                                        f"d.put(\\type, \\Effect);\n" + \
                                        f"~score[{cidx}].add(d);\n"
                        else:
                            idx[cidx] = j
                            break
                    cidx += 1

    data += ")\n"
    return data


def dump_sc_to_file(file, new_parts):
    """
    Writes dumped SC data to a file
    :param file: The file name
    :param new_parts: New (parsed) parts
    :param num_measures: The highest numbered measure
    :return:
    :return:
    """
    with open(file, "w") as f:
        f.write(dump_sc(new_parts))


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
    level = LEVELS[note.mul]
    frequency = 440.0 * 2 ** ((note.pitch.p - 18) / 24)
    if frequency < 2000:
        level *= (8 * 10 ** -15) * ((-frequency + 2000) ** 4.5) + 1
    else:
        level *= (1.5 * 10 ** -8) * ((frequency - 2000) ** 2) + 1
    return level


def get_highest_measure_no(parsed_parts):
    """
    Gets the highest measure number in a list of parts
    :param parsed_parts: A list of parsed parts
    :return: The highest measure number
    """
    num_measures = 0
    for p in parsed_parts:
        for v in p:
            for v1 in v:
                for n in v1:
                    if type(n) == Note:
                        if n.measure > num_measures:
                            num_measures = n.measure
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
        """
        new_parts is a 3D list of lists. Hierarchy of new_parts:
        Level 1: Part
        Level 2: Voice (for voices in a part)
        Level 3: Subvoice (for notes in chords). There is one subvoice for each note in a chord.
        """
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
                                        new_parts[i][int(item.id) - 1][p].append(n)

                            elif type(item2) == music21.note.Note:
                                n = Note(pitch=convert_pitch24(item2.pitch),
                                         duration=Fraction(item2.duration.quarterLength) * current_quarter_duration,
                                         measure=measure.number,
                                         quarter_duration=Fraction(item2.duration.quarterLength),
                                         start_time=Fraction(part_time_offset + item2.offset * current_quarter_duration))

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

    return new_parts


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
