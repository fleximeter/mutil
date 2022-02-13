"""
File: v_analyze.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functions for analyzing vertical slices.
Copyright (c) 2022 by Jeff Martin.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import fractions
import json
import music21
from vslice2 import VSlice
from results import Results
from fractions import Fraction
from pctheory import pitch, pcset
from decimal import Decimal


def analyze(input_xml, first=-1, last=-1, use_local=False):
    """
    Performs a vertical analysis on the given stream and writes a report to CSV
    :param input_xml: The musicxml file to analyze
    :param first: The first measure to analyze
    :param last: The last measure to analyze
    :param use_local: Whether or not to use local bounds for register analysis
    :return: A Results object containing the results of the analysis
    """
    stream = music21.converter.parse(input_xml)
    parts = []
    for item in stream:
        if type(item) == music21.stream.Part:
            parts.append(item)
    results = slice_parts(parts, get_slice_num(parts), [], [use_local], first, last)
    return results[0]


def analyze_corpus(name, first=-1, last=-1, use_local=False):
    """
    Performs a vertical analysis on the given stream and writes a report to CSV
    :param name: The musicxml file in the music21 corpus to analyze
    :param first: The first measure to analyze
    :param last: The last measure to analyze
    :param use_local: Whether or not to use local bounds for register analysis
    :return: A Results object containing the results of the analysis
    """
    stream = music21.corpus.parse(name)
    parts = []
    for item in stream:
        if type(item) == music21.stream.Part:
            parts.append(item)
    results = slice_parts(parts, get_slice_num(parts), [], [use_local], first, last)
    return results[0]


def analyze_with_sections(input_xml, section_divisions, use_local):
    """
    Performs a vertical analysis on the given stream and writes a report to CSV
    :param input_xml: The musicxml file to analyze
    :param section_divisions: A list of section divisions
    :param use_local: Whether or not to use local bounds for register analysis
    :return: A list of Results objects containing the results of the analysis.
    Index 0 is a complete analysis, and the remaining indices are section analyses
    in the order in which they were provided.
    """
    stream = music21.converter.parse(input_xml)
    parts = []
    for item in stream:
        if type(item) == music21.stream.Part:
            parts.append(item)
    return slice_parts(parts, get_slice_num(parts), section_divisions, use_local, -1, -1)


#done
def clean_slices(slices, match_tempo=False):
    """
    Cleans up a list of v_slices
    :param slices: A list of v_slices
    :param match_tempo: Whether or not to force tempo match
    """
    # Remove duplicate slices, and update durations
    if len(slices) > 0:
        i = 1
        while i < len(slices):
            if slice_compare(slices[i - 1], slices[i], match_tempo):
                slices[i - 1].duration += slices[i].duration
                slices[i - 1].quarter_duration += slices[i].quarter_duration
                del slices[i]
            else:
                i += 1


#done
def factor(n):
    """
    Factors a positive integer
    :param n: An integer
    :returns: A list of factors, in sorted order, including duplicates
    """
    factors = []
    d = 1
    while d <= int(n ** 0.5):
        if n % d == 0:
            factors.append(d)
            n //= d
        else:
            d += 1
        if d == 1:
            d += 1
        # if d > int(n ** 0.5):
        #     factors.append(n)
    factors.append(n)
    # factors.sort()
    return factors


#done
def get_bounds(slices):
    """
    Gets the upper and lower bounds of a list of v_slices
    :param slices: A list of v_slices
    :return: The lower and upper bounds as a tuple. The lower bound is index 0,
    and the upper bound is index 1. If the slices contain no pitches, each of
    the bounds will be None.
    """

    lower_bound = None
    upper_bound = None

    for i in range(0, len(slices)):
        if (lower_bound is None or upper_bound is None) and len(slices[i].pseg) > 0:
            lower_bound = slices[i].pseg[0].p
            upper_bound = slices[i].pseg[len(slices[i].pseg) - 1].p
        if len(slices[i].pseg) > 0 and lower_bound is not None and upper_bound is not None:
            if slices[i].pseg[0].p < lower_bound:
                lower_bound = slices[i].pseg[0].p
            if slices[i].pseg[len(slices[i].pseg) - 1].p > upper_bound:
                upper_bound = slices[i].pseg[len(slices[i].pseg) - 1].p

    return lower_bound, upper_bound


#done
def get_piece_bounds(parts):
    """
    Determines the lower and upper bounds of a piece
    :param parts: A list of parts
    :return: The lower and upper bounds as a tuple.
    """
    lower = None
    upper = None
    for part in parts:
        for item in part:
            if type(item) == music21.stream.Measure:
                for item2 in item:
                    if type(item2) == music21.stream.Voice:
                        for item3 in item2:
                            if type(item3) == music21.note.Note or type(item3) == music21.chord.Chord:
                                for pitch in item3.pitches:
                                    if lower is None:
                                        lower = pitch.midi - 60
                                    if upper is None:
                                        upper = pitch.midi - 60
                                    if lower > pitch.midi - 60:
                                        lower = pitch.midi - 60
                                    if upper < pitch.midi - 60:
                                        upper = pitch.midi - 60
                    elif type(item2) == music21.note.Note or type(item2) == music21.chord.Chord:
                        for pitch in item2.pitches:
                            if lower is None:
                                lower = pitch.midi - 60
                            if upper is None:
                                upper = pitch.midi - 60
                            if lower > pitch.midi - 60:
                                lower = pitch.midi - 60
                            if upper < pitch.midi - 60:
                                upper = pitch.midi - 60

    return lower, upper


#done
def get_slice_num(parts):
    """
    Determines the number of slices per quarter note based on subdivisions of the note.
    :param parts: A stream of parts
    :returns: The number of slices per quarter note
    """
    # A collection of all the unique denominators we find
    denominators = {}
    denominators_list = []

    # Find all the unique denominators
    for part in parts:
        for stream in part:
            if type(stream) == music21.stream.Measure:
                for item in stream:
                    if type(item) == music21.note.Note or type(item) == music21.note.Rest or type(item) == \
                            music21.chord.Chord:
                        ql = item.duration.quarterLength
                        if type(item.duration.quarterLength) != Fraction:
                            ql = Fraction(item.duration.quarterLength)
                        if ql.denominator not in denominators:
                            denominators[ql.denominator] = True

    # Get the LCM and return it. This is the number of slices per quarter note that we need.
    for item in denominators:
        denominators_list.append(item)
    return lcm(denominators_list)


#done
def lcm(integers):
    """
    Computes the LCM of a list of positive integers
    :param integers: A list of positive integers
    :return: The LCM
    """
    factors = {}  # A dictionary of individual factors and their multiplicities
    multiple = 1  # The LCM

    for num in integers:
        cur_factors = factor(num)  # The factors of the current number
        current = 1  # The current factor we are considering
        count = 0  # The number of occurrences of that factor
        for i in range(len(cur_factors)):
            # If we found another occurrence of that factor, increase the count
            if cur_factors[i] == current:
                count += 1
            # Otherwise record the count and move on
            else:
                if current not in factors:
                    factors[current] = count
                elif factors[current] < count:
                    factors[current] = count
                current = cur_factors[i]
                count = 1
            # If we are done, record the count of the last factor
            if i + 1 == len(cur_factors):
                if current not in factors:
                    factors[current] = count
                elif factors[current] < count:
                    factors[current] = count

    # Compute the LCM
    for item in factors:
        multiple *= item ** factors[item]
    # print(multiple)
    return multiple


#done
def set_slice_bounds(slices, bounds):
    """
    Sets the bounds of a list of v_slices
    :param slices: A list of v_slices
    :param bounds: A tuple with the lower and upper bounds
    """

    for i in range(len(slices)):
        slices[i].lower_bound = bounds[0]
        slices[i].upper_bound = bounds[1]


#done
def slice_parts(parts, n, section_divisions, use_local, first=-1, last=-1):
    """
    Takes n vertical slices of each beat from each of the parts. Note that beats are always quarter notes
    in music21. The parts do not need to have the same time signature for each measure: each slice is taken
    independently of the time signature. The parts do not even need to have the same number of total beats.
    However, it is assumed that a quarter note in any given part is equal in duration to a quarter note in
    any other part (this means that all parts must share the same tempo for a quarter note).
    :param parts: A list of parts
    :param n: The number of slices per quarter note
    :param section_divisions: A list of section divisions
    :param use_local: Whether or not to use local bounds for register analysis
    :param first: The first measure to analyze (-1 means start at the beginning)
    :param last: The last measure to analyze (-1 means analyze to the end)
    :return: A list of v_slices
    """

    sc = pcset.SetClass()  # A set-class for calculating names, etc.
    final_slices = []      # Holds the finalized slices to return
    first_measure = -1     # We assume that the first measure is -1
    last_measure = -1      # We assume that the last measure is -1
    next_indices = [0 for i in range(len(parts))]  # The index of the next measure, for each part
    next_measure = -1      # The number of the next measure
    tempo = Decimal(60)    # We assume a tempo of 60 to begin
    tempo_multiplier = 10  # This is in place to avoid floats
    time_signature = None  # The current time signature
    transpose = [0 for i in range(len(parts))]  # The amount by which to transpose, for each part

    if len(parts) == 0:
        print("No parts were provided")

    else:
        # Determine the index of the first measure in each part. a is the part index,
        # and b is the index of the item inside the current part (which may or may not be a measure)
        for a in range(len(parts)):
            found_first = False
            for b in range(len(parts[a])):
                if type(parts[a][b]) == music21.stream.Measure:
                    if parts[a][b].number >= first:
                        next_measure = parts[a][b].number
                        first_measure = next_measure
                        next_indices[a] = b
                        found_first = True
                # No need to continue after the first measure was found
                if found_first:
                    break

        # We consider each measure separately. When we have finished the last measure,
        # the next_measure will reset to -1 and we will stop.
        while next_measure != -1:
            last_measure = next_measure
            # The slices taken for this measure
            measure_slices = []

            # Consider each part separately for this measure
            for a in range(len(parts)):
                # Tracks the number of slices taken for the current part in the current measure
                num_slices_taken = 0
                for item in parts[a][next_indices[a]]:
                    last_item_was_voice = False
                    furthest_voice_slice = 0

                    # MusicXML doesn't handle transposition properly for 8va and 8vb clefs, so we need manual
                    # transposition. Record for the future.
                    if type(item) == music21.clef.Bass8vaClef or type(item) == music21.clef.Treble8vaClef:
                        transpose[a] = 12
                    elif type(item) == music21.clef.Bass8vbClef or type(item) == music21.clef.Treble8vbClef:
                        transpose[a] = -12
                    elif isinstance(item, music21.clef.Clef):
                        transpose[a] = 0

                    # Record the current time signature
                    if type(item) == music21.meter.TimeSignature:
                        time_signature = item

                    # Update the tempo if we find a new one
                    if type(item) == music21.tempo.MetronomeMark:
                        tempo = Decimal(item.number)

                        # Specific adjustments for Carter 5
                        if parts[a][next_indices[a]].number == 46:
                            tempo = Decimal(512) / Decimal(7)
                        elif parts[a][next_indices[a]].number == 66:
                            tempo = Decimal(384) / Decimal(7)
                        elif parts[a][next_indices[a]].number == 128:
                            tempo = Decimal(1152) / Decimal(10)
                        # print(f"Tempo: {tempo}, Measure {parts[a][next_indices[a]].number}")
                        # deprecated:
                        # tempo_multiplier = 10 ** str(tempo)[::-1].find(".")

                    # If we have found multiple voices in the same part in the same measure
                    if type(item) == music21.stream.Voice:
                        last_item_was_voice = True

                        # Track the start point for the voice
                        slice_start = num_slices_taken

                        for item2 in item:
                            # We can only take slices of notes, rests, or chords
                            if type(item2) == music21.note.Note or type(item2) == music21.note.Rest or type(
                                    item2) == music21.chord.Chord:
                                ql = item2.duration.quarterLength
                                if type(item2.duration.quarterLength) != Fraction:
                                    ql = Fraction(item2.duration.quarterLength)

                                num_slices = int(ql * n)
                                # the pitches are considered as integers in p-space. The p_names hold pitch names
                                # which is often more convenient for humans.
                                pitches_in_item = []
                                p_names_in_item = []

                                # We use Morris's p-space. Obviously rests do not have pitches.
                                if type(item2) != music21.note.Rest:
                                    for p in item2.pitches:
                                        name = p.name
                                        octave = p.octave + (transpose[a] // 12)
                                        pitches_in_item.append(p.midi - 60 + transpose[a])
                                        p_names_in_item.append(name + str(octave))

                                # Perform slicing. num_slices is the number of slices we take for the current object.
                                for j in range(num_slices):
                                    if num_slices_taken >= len(measure_slices):
                                        measure_slices.append(
                                            VSlice(tempo,
                                                   Fraction(1, n.numerator), parts[a][next_indices[a]].number))
                                    measure_slices[num_slices_taken].add_pitches(pitches_in_item, p_names_in_item, a)
                                    measure_slices[num_slices_taken].time_signature = time_signature
                                    measure_slices[num_slices_taken].start_position = Fraction(num_slices_taken,
                                                                                               n.numerator)
                                    num_slices_taken += 1

                        # Record the furthest slice reached in this voice if necessary
                        if furthest_voice_slice < num_slices_taken:
                            furthest_voice_slice = num_slices_taken

                        # Reset the slice counter to start on the next voice
                        num_slices_taken = slice_start

                    # If we just evaluated a voice and are done, we need to reset the slice counter
                    elif last_item_was_voice and num_slices_taken < furthest_voice_slice:
                        num_slices_taken = furthest_voice_slice

                    # We can only take slices of notes, rests, or chords
                    if type(item) == music21.note.Note or type(item) == music21.note.Rest or type(
                            item) == music21.chord.Chord:
                        ql = item.duration.quarterLength
                        if type(item.duration.quarterLength) != Fraction:
                            ql = Fraction(item.duration.quarterLength)

                        num_slices = int(ql * n)

                        # the pitches are considered as integers in p-space. The p_objects hold pitch names which
                        # is often more convenient for humans.
                        pitches_in_item = []
                        p_names_in_item = []

                        # We use Morris's p-space. Obviously rests do not have pitches.
                        if type(item) != music21.note.Rest:
                            for p in item.pitches:
                                name = p.name
                                octave = p.octave + (transpose[a] // 12)
                                pitches_in_item.append(p.midi - 60 + transpose[a])
                                p_names_in_item.append(name + str(octave))

                        # Perform slicing. num_slices is the number of slices we take for the current object.
                        for j in range(num_slices):
                            if num_slices_taken >= len(measure_slices):
                                measure_slices.append(
                                    VSlice(tempo,
                                           Fraction(1, n.numerator), parts[a][next_indices[a]].number))
                            measure_slices[num_slices_taken].add_pitches(pitches_in_item, p_names_in_item, a)
                            measure_slices[num_slices_taken].time_signature = time_signature
                            measure_slices[num_slices_taken].start_position = Fraction(num_slices_taken,
                                                                                       n.numerator)
                            num_slices_taken += 1

            # Clean up the slices from this measure
            clean_slices(measure_slices, True)
            for item in measure_slices:
                final_slices.append(item)

            # Find the next measure for each part
            for a in range(len(parts)):  # a is the part index
                found_next = False
                next_measure = -1
                # We start at the item after the current measure
                for b in range(next_indices[a] + 1, len(parts[a])):
                    if type(parts[a][b]) == music21.stream.Measure:
                        next_measure = parts[a][b].number
                        next_indices[a] = b
                        found_next = True
                    # No need to continue after the first measure was found
                    if found_next:
                        break

            # If we've analyzed the last measure, it's time to stop analyzing
            if next_measure > last > -1:
                next_measure = -1

    results = []
    global_bounds = get_piece_bounds(parts)

    # Make pctheory objects
    for sl in final_slices:
        sl.make_sets()

    # Create sectional results
    for i in range(len(section_divisions)):
        section_slices = []
        for sl in final_slices:
            if section_divisions[i][0] <= sl.measure <= section_divisions[i][1]:
                section_slices.append(sl)
        clean_slices(section_slices, True)
        bounds = global_bounds
        if use_local[i]:
            bounds = get_bounds(section_slices)
        set_slice_bounds(section_slices, bounds)
        for s in section_slices:
            s.run_calculations(sc)
        clean_slices(section_slices)
        results.append(Results(section_slices, section_divisions[i][0], section_divisions[i][1], len(parts)))

    # Create overall results
    clean_slices(final_slices, True)
    bounds = global_bounds
    if len(use_local) == 1:
        if use_local[0]:
            bounds = get_bounds(final_slices)
    set_slice_bounds(final_slices, bounds)
    for f_slice in final_slices:
        f_slice.run_calculations(sc)
    clean_slices(final_slices)
    results.insert(0, Results(final_slices, first_measure, last_measure, len(parts)))
    return results


#done
def slice_compare(slice1, slice2, match_tempo=False):
    """
    Compares two v_slices for equality
    :param slice1: A v_slice
    :param slice2: A v_slice
    :param match_tempo: Whether or not to match tempo
    :return: True if equal, False if not equal
    """
    equal = True
    if slice1.p_count != slice2.p_count:
        equal = False
    elif match_tempo and slice1._tempo != slice2._tempo:
        equal = False
    else:
        for p in slice1.pitchseg:
            if p not in slice2.pitchseg:
                equal = False
                break
    return equal


def read_analysis_from_file(path):
    """
    Reads analysis data from a file
    :param path: The file path
    :return: A list of Results objects
    """
    data = None
    results = []
    with open(path, "r") as file_in:
        data = json.load(file_in)
    for item in data:
        slices = []
        for dslice in item["slices"]:
            cslice = VSlice()
            cslice._core = bool(dslice["core"])
            cslice._derived_core = bool(dslice["derived_core"])
            cslice._derived_core_associations = dslice["derived_core_associations"]
            cslice._duration = Decimal(dslice["duration"])
            cslice._ipseg = dslice["ipseg"]
            cslice._measure = dslice["measure"]
            cslice._p_cardinality = dslice["p_cardinality"]
            cslice._p_count = dslice["p_count"]
            cslice._pc_cardinality = dslice["pc_cardinality"]
            cslice._pcseg = [pitch.PitchClass(pc) for pc in dslice["pcseg"]]
            cslice._pcset = set(cslice.pcseg)
            cslice._pcsegs = [[pitch.PitchClass(pc) for pc in dslice["pcsegs"][v]]
                              for v in range(len(dslice["pcsegs"]))]
            cslice._pcset = set(cslice.pcseg)
            cslice._pcsets = [set(cslice.pcsegs[v]) for v in range(len(cslice.pcsegs))]
            cslice._pitchseg = dslice["pitchseg"]
            cslice._pitchsegs = dslice["pitchsegs"]
            cslice._pnameseg = dslice["pnameseg"]
            cslice._pnamesegs = dslice["pnamesegs"]
            cslice._pseg = [pitch.Pitch(p) for p in dslice["pseg"]]
            cslice._psegs = [[pitch.Pitch(p) for p in dslice["psegs"][v]] for v in range(len(dslice["psegs"]))]
            cslice._pset = set(cslice.pseg)
            cslice._psets = [set(cslice.psegs[v]) for v in range(len(cslice.psegs))]
            cslice._quarter_duration = Fraction(dslice["quarter_duration"][0], dslice["quarter_duration"][1])
            cslice._sc_name = dslice["sc_name"]
            cslice._sc_name_carter = dslice["sc_name_carter"]
            cslice._ins = dslice["ins"]
            cslice._lns = dslice["lns"]
            cslice._lower_bound = dslice["lower_bound"]
            cslice._mediant = dslice["mediant"]
            cslice._ns = dslice["ns"]
            cslice._ps = dslice["ps"]
            cslice._start_position = Fraction(dslice["start_position"][0], dslice["start_position"][1])
            cslice._time_signature = music21.meter.TimeSignature(dslice["time_signature"])
            cslice._uns = dslice["uns"]
            cslice._upper_bound = dslice["upper_bound"]
            slices.append(cslice)
        result = Results(slices, item["measure_num_first"], item["measure_num_last"], len(item["pitch_highest_voices"]))
        result._max_p_count = item["max_p_count"]
        result._duration = Decimal(item["duration"])
        result._ins_avg = item["ins_avg"]
        result._ins_max = item["ins_max"]
        result._ins_min = item["ins_min"]
        result._lns_avg = item["lns_avg"]
        result._lns_max = item["lns_max"]
        result._lns_min = item["lns_min"]
        result._lower_bound = item["lower_bound"]
        result._lps_card = item["lps_card"]
        result._mediant_avg = item["mediant_avg"]
        result._mediant_max = item["mediant_max"]
        result._mediant_min = item["mediant_min"]
        result._num_measures = item["num_measures"]
        result._num_voices = len(item["pitch_highest_voices"])
        result._pitch_highest = item["pitch_highest"]
        result._pitch_highest_voices = item["pitch_highest_voices"]
        result._pitch_lowest = item["pitch_lowest"]
        result._pitch_lowest_voices = item["pitch_lowest_voices"]
        result._ps_avg = item["ps_avg"]
        result._ps_max = item["ps_max"]
        result._ps_min = item["ps_min"]
        result._quarter_duration = Fraction(item["quarter_duration"][0], item["quarter_duration"][1])
        result._uns_avg = item["uns_avg"]
        result._uns_max = item["uns_max"]
        result._uns_min = item["uns_min"]
        result._upper_bound = item["upper_bound"]
        result._pc_duration = {}
        result._pc_frequency = {}
        result._pitch_duration = {}
        result._pitch_frequency = {}
        for key, val in item["pc_duration"].items():
            result.pc_duration[int(key)] = Decimal(val[0])
        for v in range(len(item["pc_duration_voices"])):
            result.pc_duration_voices.append({})
            for key, val in item["pc_duration_voices"][v].items():
                result.pc_duration_voices[v][int(key)] = Decimal(val)
        for key, val in item["pitch_duration"].items():
            result.pitch_duration[int(key)] = Decimal(val)
        for v in range(len(item["pitch_duration_voices"])):
            result.pitch_duration_voices.append({})
            for key, val in item["pitch_duration_voices"][v].items():
                result.pitch_duration_voices[v][int(key)] = Decimal(val)
        for key, val in item["pc_frequency"].items():
            result.pc_frequency[int(key)] = val
        for v in range(len(item["pc_frequency_voices"])):
            result.pc_frequency_voices.append({})
            for key, val in item["pc_frequency_voices"][v].items():
                result.pc_frequency_voices[v][int(key)] = val
        for key, val in item["pitch_frequency"].items():
            result.pitch_frequency[int(key)] = val
        for v in range(len(item["pitch_frequency_voices"])):
            result.pitch_frequency_voices.append({})
            for key, val in item["pitch_frequency_voices"][v].items():
                result.pitch_frequency_voices[v][int(key)] = val

        results.append(result)
    return results


def write_analysis_to_file(results, path):
    """
    Writes an analysis to file
    :param results: A Results object
    :param path: A path
    :return:
    """
    data = []
    for i in range(len(results)):
        data.append({})
        data[i]["max_p_count"] = results[i].max_p_count
        data[i]["duration"] = str(results[i].duration)
        data[i]["ins_avg"] = results[i].ins_avg
        data[i]["ins_max"] = results[i].ins_max
        data[i]["ins_min"] = results[i].ins_min
        data[i]["lns_avg"] = results[i].lns_avg
        data[i]["lns_max"] = results[i].lns_max
        data[i]["lns_min"] = results[i].lns_min
        data[i]["lower_bound"] = results[i].lower_bound
        data[i]["lps_card"] = results[i].lps_card
        data[i]["measure_num_first"] = results[i].measure_num_first
        data[i]["measure_num_last"] = results[i].measure_num_last
        data[i]["mediant_avg"] = results[i].mediant_avg
        data[i]["mediant_max"] = results[i].mediant_max
        data[i]["mediant_min"] = results[i].mediant_min
        data[i]["num_measures"] = results[i].num_measures
        data[i]["pitch_highest"] = results[i].pitch_highest
        data[i]["pitch_highest_voices"] = results[i].pitch_highest_voices
        data[i]["pitch_lowest"] = results[i].pitch_lowest
        data[i]["pitch_lowest_voices"] = results[i].pitch_lowest_voices
        data[i]["ps_avg"] = results[i].ps_avg
        data[i]["ps_max"] = results[i].ps_max
        data[i]["ps_min"] = results[i].ps_min
        data[i]["quarter_duration"] = [results[i].quarter_duration.numerator, results[i].quarter_duration.denominator]
        data[i]["uns_avg"] = results[i].uns_avg
        data[i]["uns_max"] = results[i].uns_max
        data[i]["uns_min"] = results[i].uns_min
        data[i]["upper_bound"] = results[i].upper_bound
        data[i]["pc_duration"] = {}
        data[i]["pc_duration_voices"] = []
        data[i]["pc_frequency"] = results[i].pc_frequency
        data[i]["pc_frequency_voices"] = results[i].pc_frequency_voices
        data[i]["pitch_duration"] = {}
        data[i]["pitch_duration_voices"] = []
        data[i]["pitch_frequency"] = results[i].pitch_frequency
        data[i]["pitch_frequency_voices"] = results[i].pitch_frequency_voices
        data[i]["slices"] = []
        for key, val in results[i].pc_duration.items():
            data[i]["pc_duration"][key] = str(val)
        for v in range(len(results[i].pc_duration_voices)):
            data[i]["pc_duration_voices"].append({})
            for key, val in results[i].pc_duration_voices[v].items():
                data[i]["pc_duration_voices"][len(data[i]["pc_duration_voices"]) - 1][key] = str(val)
        for key, val in results[i].pitch_duration.items():
            data[i]["pitch_duration"][key] = str(val)
        for v in range(len(results[i].pitch_duration_voices)):
            data[i]["pitch_duration_voices"].append({})
            for key, val in results[i].pitch_duration_voices[v].items():
                data[i]["pitch_duration_voices"][len(data[i]["pitch_duration_voices"]) - 1][key] = str(val)
        for rslice in results[i].slices:
            cslice = {}
            cslice["core"] = int(rslice.core)
            cslice["derived_core"] = int(rslice.derived_core)
            cslice["derived_core_associations"] = rslice.derived_core_associations
            cslice["duration"] = str(rslice.duration)
            cslice["ipseg"] = rslice.ipseg
            cslice["measure"] = rslice.measure
            cslice["p_cardinality"] = rslice.p_cardinality
            cslice["p_count"] = rslice.p_count
            cslice["pc_cardinality"] = rslice.pc_cardinality
            cslice["pcseg"] = [pc.pc for pc in rslice.pcseg]
            cslice["pcsegs"] = [[pc.pc for pc in rslice.pcsegs[v]] for v in range(len(rslice.pcsegs))]
            cslice["pitchseg"] = [p for p in rslice.pitchseg]
            cslice["pitchsegs"] = [[p for p in rslice.pitchsegs[v]] for v in range(len(rslice.pitchsegs))]
            cslice["pnameseg"] = [pname for pname in rslice.pnameseg]
            cslice["pnamesegs"] = [[pname for pname in rslice.pnamesegs[v]] for v in range(len(rslice.pnamesegs))]
            cslice["pseg"] = [p.p for p in rslice.pseg]
            cslice["psegs"] = [[p.p for p in rslice.psegs[v]] for v in range(len(rslice.psegs))]
            cslice["quarter_duration"] = [rslice.quarter_duration.numerator, rslice.quarter_duration.denominator]
            cslice["sc_name"] = rslice.sc_name
            cslice["sc_name_carter"] = rslice.sc_name_carter
            cslice["ins"] = rslice.ins
            cslice["lns"] = rslice.lns
            cslice["lower_bound"] = rslice.lower_bound
            cslice["mediant"] = rslice.mediant
            cslice["ns"] = rslice.ns
            cslice["ps"] = rslice.ps
            cslice["start_position"] = [rslice.start_position.numerator, rslice.start_position.denominator]
            cslice["time_signature"] = rslice.time_signature.ratioString
            cslice["uns"] = rslice.uns
            cslice["upper_bound"] = rslice.upper_bound
            data[i]["slices"].append(cslice)

    with open(path, "w") as out:
        out.write(json.dumps(data))


def write_general_report(section_name, file, file_command, results, lowest_pitch, highest_pitch):
    """
    Writes a general report to CSV
    :param section_name: The name of the section being reported
    :param file: The file path
    :param file_command: The command ("w" or "a")
    :param results: A Results object
    :param lowest_pitch: The lowest pitch analyzed
    :param highest_pitch: The highest pitch analyzed
    :return: None
    """
    with open(file, file_command) as general:
        if file_command == "w":
            # Write column headings
            general.write("Section,LPS,P_U,P_L,PS avg,PS min,PS max,UNS avg,UNS min,UNS max," + \
                          "LNS avg,LNS min,LNS max,INS avg,INS min,INS max,MT avg,MT min,MT max")
            for i in range(0, 12):
                general.write(",pc" + str(i) + " dur")
            for i in range(0, 12):
                general.write(",pc" + str(i) + " freq")
            for i in range(lowest_pitch, highest_pitch + 1):
                general.write(",p" + str(i) + " dur")
            for i in range(lowest_pitch, highest_pitch + 1):
                general.write(",p" + str(i) + " freq")
            general.write("\n")
        general.write(section_name + ",")
        general.write(str(results.lps_card) + "," + str(results.pitch_highest) + "," + str(results.pitch_lowest) +
                      "," + str(results.ps_avg) + "," + str(results.ps_min) + "," + str(results.ps_max) +
                      "," + str(results.uns_avg) + "," + str(results.uns_min) + "," + str(results.uns_max) +
                      "," + str(results.lns_avg) + "," + str(results.lns_min) + "," + str(results.lns_max) +
                      "," + str(results.ins_avg) + "," + str(results.ins_min) + "," + str(results.ins_max) +
                      "," + str(results.mediant_avg) + "," + str(results.mediant_min) + "," +
                      str(results.mediant_max))
        for i in range(0, 12):
            if i in results.pc_duration.keys():
                general.write("," + str(float(results.pc_duration[i])))
            else:
                general.write(",0")
        for i in range(0, 12):
            if i in results.pc_frequency.keys():
                general.write("," + str(float(results.pc_frequency[i])))
            else:
                general.write(",0")
        for i in range(lowest_pitch, highest_pitch + 1):
            if i in results.pitch_duration.keys():
                general.write("," + str(float(results.pitch_duration[i])))
            else:
                general.write(",0")
        for i in range(lowest_pitch, highest_pitch + 1):
            if i in results.pitch_frequency.keys():
                general.write("," + str(float(results.pitch_frequency[i])))
            else:
                general.write(",0")
        general.write("\n")
        for v in range(results.num_voices):
            general.write(f"{section_name} (Voice {v}),")
            general.write(f"{results.pitch_highest_voices[v] - results.pitch_lowest_voices[v] + 1},")
            general.write(f"{results.pitch_highest_voices[v]},")
            general.write(f"{results.pitch_lowest_voices[v]},")
            general.write(",,,,,,,,,,,,,,")
            for i in range(0, 12):
                if i in results.pc_duration_voices[v].keys():
                    general.write("," + str(float(results.pc_duration_voices[v][i])))
                else:
                    general.write(",0")
            for i in range(0, 12):
                if i in results.pc_frequency_voices[v].keys():
                    general.write("," + str(float(results.pc_frequency_voices[v][i])))
                else:
                    general.write(",0")
            for i in range(lowest_pitch, highest_pitch + 1):
                if i in results.pitch_duration_voices[v].keys():
                    general.write("," + str(float(results.pitch_duration_voices[v][i])))
                else:
                    general.write(",0")
            for i in range(lowest_pitch, highest_pitch + 1):
                if i in results.pitch_frequency_voices[v].keys():
                    general.write("," + str(float(results.pitch_frequency_voices[v][i])))
                else:
                    general.write(",0")
            general.write("\n")


def write_report(file, results):
    """
    Writes a report to CSV
    :param file: A file name (and path if necessary)
    :param results: A Results object
    """
    with open(file, "w") as output:
        if len(results.slices) > 0:
            # Track the onset position in seconds
            position = 0

            # Output column headings
            line = "Measure #,Start Time (seconds),Duration (seconds),Quarter duration,Chord cardinality," + \
                   "PS,Match,NS,UNS,INS,LNS,MT,Morris name,Carter name,Core,Derived core,DC associations,pcset,pset,psc"
            for i in range(results.max_p_count):
                line += ",Pitch " + str(i + 1)
            for i in range(results.ps_max):
                line += ",Pn_" + str(i + 1)
            line += "\n"
            output.write(line)

            # Output each slice
            for item in results.slices:
                line = str(item.measure)
                line += "," + str(float(position))
                line += "," + str(float(item.duration))
                line += ",\'" + str(item.quarter_duration)
                line += "," + str(item.p_count)
                line += "," + str(item.ps)
                if item.p_cardinality == item.ps:
                    line += ",TRUE"
                else:
                    line += ",FALSE"
                if item.ns is not None:
                    line += "," + str(item.ns)
                else:
                    line += ",N/A"
                if item.uns is not None:
                    line += "," + str(item.uns)
                else:
                    line += ",N/A"
                line += "," + str(item.ins)
                if item.lns is not None:
                    line += "," + str(item.lns)
                else:
                    line += ",N/A"
                if item.mediant is not None:
                    line += "," + str(item.mediant)
                else:
                    line += ",N/A"
                if item.sc_name is not None:
                    line += "," + str(item.sc_name)
                else:
                    line += ",N/A"
                if item.sc_name_carter is not None:
                    line += ",\"" + str(item.sc_name_carter) + "\""
                else:
                    line += ",N/A"
                line += "," + str(item.core) + "," + str(item.derived_core)
                if item.derived_core:
                    line += ",\"" + str(item.derived_core_associations) + "\""
                else:
                    line += ",N/A"
                if item.pcset is not None:
                    line += ",\"" + item.get_pcset_str() + "\""
                else:
                    line += ",N/A"
                if item.pset is not None:
                    line += f",\"{item.get_pset_str()}\""
                else:
                    line += ",N/A"
                line += "," + item.get_ipseg_string()
                for i in range(results.max_p_count):
                    if i < len(item.pitchseg):
                        line += "," + str(item.pnameseg[i])
                    else:
                        line += ","
                for i in range(results.ps_max):
                    if i < len(item.pseg):
                        line += "," + str(item.pseg[i])
                    else:
                        line += ","
                line += "\n"
                output.write(line)
                position += item.duration

        # If we have no slices to write, just write a newline
        else:
            output.write("\n")
