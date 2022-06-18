"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

import music21
from pctheory import pitch, pcseg, pcset
from fractions import Fraction
from decimal import Decimal

FOLDER = "H:\\My Drive\\Composition\\Compositions\\Trombone Piece"
FILE = "Trombone Piece 0.2.1 - Full score - 01 Flow 1.xml"
MAP24 = {"C": 0, "D": 4, "E": 8, "F": 10, "G": 14, "A": 18, "B": 22}
PC12 = 12
PC24 = 24


class Note:
    """
    Represents a note with pitch, duration, and start time
    """

    def __init__(self, **kwargs):
        self._duration = kwargs["duration"] if "duration" in kwargs else 0
        self._measure = kwargs["measure"] if "measure" in kwargs else 0
        self._pitch = kwargs["pitch"] if "pitch" in kwargs else None
        self._quarter_duration = kwargs["quarter_duration"] if "quarter_duration" in kwargs else 0
        self._start_quarter_note = kwargs["start_quarter_note"] if "start_quarter_note" in kwargs else 0
        self._start_time = kwargs["start_time"] if "start_time" in kwargs else 0

    @property
    def duration(self):
        """
        The duration in seconds
        :return: The duration in seconds
        """
        return self._duration

    @duration.setter
    def duration(self, value):
        """
        The duration in seconds
        :param value: The new value
        :return:
        """
        self._duration = value

    @property
    def measure(self):
        """
        The measure number
        :return: The measure number
        """
        return self._measure

    @measure.setter
    def measure(self, value):
        """
        The measure number
        :param value: The new value
        :return:
        """
        self._measure = value

    @property
    def pitch(self):
        """
        The pitch
        :return: The pitch
        """
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        """
        The pitch
        :param value: The new pitch
        :return:
        """
        self._pitch = value

    @property
    def quarter_duration(self):
        """
        The duration in quarter notes
        :return: The duration in quarter notes
        """
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        """
        The duration in quarter notes
        :param value: The new value
        :return:
        """
        self._quarter_duration = value

    @property
    def start_quarter_note(self):
        """
        The start quarter note
        :return: The start quarter note
        """
        return self._start_quarter_note

    @start_quarter_note.setter
    def start_quarter_note(self, value):
        """
        The start quarter note
        :param value: The new value
        :return:
        """
        self._start_quarter_note = value

    @property
    def start_time(self):
        """
        The start time
        :return: The start time
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """
        The start time
        :param value: The new value
        :return:
        """
        self._start_time = value


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
                for item in p[v][v2]:
                    print(f"m{item.measure}, {item.pitch.p}, {item.duration}, {item.start_time}")


def dump_sc(new_parts):
    """
    Dumps the new part data in SuperCollider format
    :param new_parts: New (parsed) parts
    :return:
    """
    data = "(\n"

    # Get the number of voices
    num_voices = 0
    current_voice = 0
    for p in new_parts:
        for v in p:
            num_voices += len(v)

    data += "~score = Array.fill({0}, {1});\n".format(num_voices, "{List.new}")
    for p in new_parts:
        for v in range(len(p)):
            for v2 in range(len(p[v])):
                for item in p[v][v2]:
                    data += f"d = Dictionary.new;\n" + \
                        f"d.put(\\measure, {item.measure});\n" + \
                        f"d.put(\\pitch, {item.pitch.p});\n" + \
                        f"d.put(\\duration, {float(item.duration)});\n" + \
                        f"d.put(\\start, {float(item.start_time)});\n" + \
                        f"~score[{current_voice}].add(d);\n"

    data += ")\n"
    return data


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
                                                if new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].pitch == n.pitch:
                                                    new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].duration += n.duration
                                                    delete = t
                                                    break
                                            del unresolved_ties[delete]
                                    else:
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
                                            if new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].pitch == n.pitch:
                                                new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].duration += n.duration
                                                delete = t
                                                break
                                        del unresolved_ties[delete]
                                else:
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
                                        if new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].pitch == n.pitch:
                                            new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].duration += n.duration
                                            delete = t
                                            break
                                    del unresolved_ties[delete]
                            else:
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
                                    if new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].pitch == n.pitch:
                                        new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]].duration += n.duration
                                        delete = t
                                        break
                                del unresolved_ties[delete]
                        else:
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


if __name__ == "__main__":
    file_parts = read_file(f"{FOLDER}\\{FILE}")
    parsed_parts = parse_parts(file_parts, 1)
    write_to_file(dump_sc(parsed_parts), f"{FOLDER}\\SuperCollider\\score.scd")
