"""
File: xml_parse_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for parsing MusicXML data into Pbinds for a SuperCollider piece.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from fractions import Fraction
import music21
from pctheory import pitch


MAP12 = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
PC12 = 12


class PbindNote:
    """
    Represents a note for a Pbind
    """
    def __init__(self, **kwargs):
        """
        Creates a PbindNote
        """
        self.midi = kwargs["midi"] if "midi" in kwargs else 60
        self.quarterLength = kwargs["quarterLength"] if "quarterLength" in kwargs else 1


class PbindRest:
    """
    Represents a rest for a Pbind
    """
    def __init__(self, **kwargs):
        """
        Creates a PbindRest
        """
        self.quarterLength = kwargs["quarterLength"] if "quarterLength" in kwargs else 1


def dump_sc(new_parts):
    """
    Dumps the new part data in SuperCollider format
    :param new_parts: New (parsed) parts
    :return:
    """
    data = "~score = [\n"
    for p in new_parts:
        for v in p:
            for v2 in v:
                if len(v2) > 0:
                    data += "    Pbind(\n        \\instrument, Pseq([\\wt], inf),\n        \\dur, Pseq([\n            "
                    for i in range(len(v2) - 1):
                        if type(v2[i]) == PbindNote:
                            data += f"{v2[i].quarterLength.numerator}/{v2[i].quarterLength.denominator}, "
                        else:
                            data += f"Rest({v2[i].quarterLength.numerator}/{v2[i].quarterLength.denominator}), "
                    if type(v2[len(v2) - 1]) == PbindNote:
                        data += f"{v2[len(v2) - 1].quarterLength.numerator}/{v2[len(v2) - 1].quarterLength.denominator}"
                    else:
                        data += f"Rest({v2[len(v2) - 1].quarterLength.numerator}/{v2[len(v2) - 1].quarterLength.denominator})"
                    data += "\n        ], 1),\n"
                    data += "\n        \\amp, Pseq([0.3], inf),\n        \\midinote, Pseq([\n            "
                    for i in range(len(v2) - 1):
                        if type(v2[i]) == PbindNote:
                            data += f"{v2[i].midi}, "
                        else:
                            data += "0, "
                    if type(v2[len(v2) - 1]) == PbindNote:
                        data += f"{v2[len(v2) - 1].midi}"
                    else:
                        data += "0"
                    data += "\n        ], 1),\n        \\legato, 1.05\n    ),\n"
    data += "];\n"
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
        new_parts.append([[[]]])
        # Tracks the offset position in the part
        part_time_offset = 0
        current_meter = 0
        current_tempo = 0
        current_quarter_duration = 0
        unresolved_ties = []
        transpose = 0

        for measure in parts[indices[i]]:
            if type(measure) == music21.stream.Measure:
                # If there is a tempo change in this measure, we need to update the tempo
                if measure.number in metronome_marks:
                    current_tempo = Fraction(metronome_marks[measure.number])
                    current_quarter_duration = Fraction(60, current_tempo)
                for item in measure:
                    #if type(item) == music21.clef.Treble8vbClef:
                    #    transpose = -12
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
                                    n = PbindNote(midi=item2.pitches[p].midi + transpose, quarterLength=item2.duration.quarterLength)
                                    # If the note is tied, we need to keep track of it
                                    if item2.tie is not None:
                                        if item2.tie.type == "start":
                                            new_parts[i][int(item.id) - 1][p].append(n)
                                            unresolved_ties.append((i, int(item.id) - 1, p,
                                                                    len(new_parts[i][int(item.id) - 1][p]) - 1))
                                        elif item2.tie.type == "continue":
                                            for t in unresolved_ties:
                                                if new_parts[t[0]][t[1]][t[2]][t[3]].midi == n.midi:
                                                    new_parts[t[0]][t[1]][t[2]][t[3]].quarterLength += n.quarterLength
                                                    break
                                        else:
                                            delete = 0
                                            for t in range(len(unresolved_ties)):
                                                prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                                if prev.midi == n.midi:
                                                    prev.quarterLength += n.quarterLength
                                                    delete = t
                                                    break
                                            del unresolved_ties[delete]
                                    else:
                                        new_parts[i][int(item.id) - 1][p].append(n)

                            elif type(item2) == music21.note.Note:
                                # Catch special notes that represent nonstandard sounds
                                n = PbindNote(midi=item2.pitch.midi + transpose, quarterLength=Fraction(item2.duration.quarterLength))

                                # If the note is tied, we need to keep track of it
                                if item2.tie is not None:
                                    if item2.tie.type == "start":
                                        new_parts[i][int(item.id) - 1][0].append(n)
                                        unresolved_ties.append((i, int(item.id) - 1, 0,
                                                                len(new_parts[i][int(item.id) - 1][0]) - 1))
                                    elif item2.tie.type == "continue":
                                        for t in unresolved_ties:
                                            if new_parts[t[0]][t[1]][t[2]][t[3]].midi == n.midi:
                                                new_parts[t[0]][t[1]][t[2]][t[3]].quarterLength += n.quarterLength
                                                break
                                    else:
                                        delete = 0
                                        for t in range(len(unresolved_ties)):
                                            prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                            if prev.midi == n.midi:
                                                prev.quarterLength += n.quarterLength
                                                delete = t
                                                break
                                        del unresolved_ties[delete]
                                else:
                                    new_parts[i][int(item.id) - 1][0].append(n)

                            elif type(item) == music21.note.Rest:
                                n = PbindRest(quarterLength=Fraction(item.duration.quarterLength))
                                new_parts[i][int(item.id) - 1][0].append(n)

                    elif type(item) == music21.chord.Chord:
                        # If this chord has more notes than we've encountered before,
                        # we need to add subvoices.
                        if len(new_parts[i][0]) < len(item.pitches):
                            for j in range(len(item.pitches) - len(new_parts[i][0])):
                                new_parts[i][0].append([])

                        # Parse each pitch in the chord
                        for p in range(len(item.pitches)):
                            n = PbindNote(midi=item.pitches[p].midi + transpose, quarterLength=Fraction(item.duration.quarterLength))

                            # If the note is tied, we need to keep track of it
                            if item.tie is not None:
                                if item.tie.type == "start":
                                    new_parts[i][0][p].append(n)
                                    unresolved_ties.append((i, 0, p, len(new_parts[i][0][p]) - 1))
                                elif item.tie.type == "continue":
                                    for t in unresolved_ties:
                                        if new_parts[t[0]][t[1]][t[2]][t[3]].midi == n.midi:
                                            new_parts[t[0]][t[1]][t[2]][t[3]].quarterLength += n.quarterLength
                                            break
                                else:
                                    delete = 0
                                    for t in range(len(unresolved_ties)):
                                        prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                        if prev.midi == n.midi:
                                            prev.quarterLength += n.quarterLength
                                            delete = t
                                            break
                                    del unresolved_ties[delete]
                            else:
                                new_parts[i][0][p].append(n)

                    elif type(item) == music21.note.Note:
                        if len(new_parts[i]) == 0:
                            new_parts[i].append([[]])
                        n = PbindNote(midi=item.pitch.midi + transpose, quarterLength=Fraction(item.duration.quarterLength))

                        # If the note is tied, we need to keep track of it
                        if item.tie is not None:
                            if item.tie.type == "start":
                                new_parts[i][0][0].append(n)
                                unresolved_ties.append((i, 0, 0, len(new_parts[i][0][0]) - 1))
                            elif item.tie.type == "continue":
                                for t in unresolved_ties:
                                    if new_parts[t[0]][t[1]][t[2]][t[3]].midi == n.midi:
                                        new_parts[t[0]][t[1]][t[2]][t[3]].quarterLength += n.quarterLength
                                        break
                            else:
                                delete = 0
                                for t in range(len(unresolved_ties)):
                                    prev = new_parts[unresolved_ties[t][0]][unresolved_ties[t][1]][unresolved_ties[t][2]][unresolved_ties[t][3]]
                                    if prev.midi == n.midi:
                                        prev.quarterLength += n.quarterLength
                                        delete = t
                                        break
                                del unresolved_ties[delete]
                        else:
                            new_parts[i][0][0].append(n)
                    elif type(item) == music21.note.Rest:
                        n = PbindRest(quarterLength=Fraction(item.duration.quarterLength))
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
