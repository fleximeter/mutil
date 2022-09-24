"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from mgen import xml_parse_sc, sc_data_gen
from mgen.xml_parse_sc import Dynamic, Effect, Note, Sound
import random
import time

FOLDER = "H:\\My Drive\\Composition\\Compositions\\Trombone Piece"
OUTPUT = "D:\\SuperCollider\\erudition_i"
FILE1 = "Trombone Piece 0.2.4.1a - Full score - 01 erudition I.xml"
FILE2 = "Trombone Piece 0.2.4.1b - Full score - 01 erudition I.xml"

NUM_BUFFERS = 24
NUM_BUSES = 80
CHANGE_BUS_CONSTANT = 20
random.seed(time.time())


def add_sc_data(new_parts):
    """
    Adds buffer indices to a list of new parts for SuperCollider
    :param new_parts: A list of new parts
    :return:
    """
    # A variable to give an absolute number to the current voice
    i = 0
    for part in new_parts:
        for voice in part:
            for note in voice:
                add_buf(note)
                add_env(note)
                note.mul = 1
                note.bus_out = NUM_BUSES - CHANGE_BUS_CONSTANT + i
            i += 1


def add_buf(note):
    """
    Adds a buffer to a Note
    :param note: A Note
    :return:
    """
    buf_map = [-48, -44, -40, -38, -34, -30, -26, -24, -20, -16, -14, -10, -6, -2, 0, 4, 8, 10, 14, 18, 22, 24, 28, 32]

    # Choose a sensible buffer for long notes
    if note.duration > 0.5:
        if note.pitch.p < buf_map[0]:
            note.buffer = 0
        elif note.pitch.p > buf_map[len(buf_map) - 1]:
            note.buffer = len(buf_map) - 1
        else:
            for i in range(len(buf_map)):
                if abs(note.pitch.p - buf_map[i]) <= 2:
                    note.buffer = i

    # For short notes, choose a random buffer
    else:
        note.buffer = random.randrange(0, NUM_BUFFERS - 1, 1)


def add_effects(new_parts, effect_parts):
    """
    Adds dynamics to a list of parsed parts. Updates buses.
    :param new_parts: A list of parsed parts
    :param effect_parts: A list of dynamic parts
    :return:
    """
    # Iterate through each effect entry for the current voice
    for effect in effect_parts:
        # Identify the starting and ending notes
        start_note = new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]
        end_note = new_parts[effect.end_note[0]][effect.end_note[1]][effect.end_note[2]]
        if type(start_note) == list:
            for item in start_note:
                if type(item) == Note or type(item) == Sound:
                    start_note = item
                    break
        if type(end_note) == list:
            for item in end_note:
                if type(item) == Note or type(item) == Sound:
                    end_note = item
                    break

        # Set times and duration
        effect.start_time = start_note.start_time
        effect.end_time = end_note.start_time + end_note.duration
        effect.measure = start_note.measure
        effect.duration = effect.end_time - effect.start_time

        # Update bus of effect, as well as buses of affected notes
        effect.bus_out = start_note.bus_out
        effect.bus_in = effect.bus_out - CHANGE_BUS_CONSTANT
        for i in range(effect.start_note[2], effect.end_note[2] + 1):
            if type(new_parts[effect.start_note[0]][effect.start_note[1]][i]) == list:
                for item in new_parts[effect.start_note[0]][effect.start_note[1]][i]:
                    if type(item) == Note or type(item) == Sound:
                        item.bus_out = effect.bus_in
            else:
                new_parts[effect.start_note[0]][effect.start_note[1]][i].bus_out = effect.bus_in

        # When adding effects, we use separate chaining. That is, we create a list containing the effect
        # and starting note, and put that list into the voice where the starting note used to be.
        # We will go through the voice and flatten it out later, after all dynamics and effects are added.
        # This allows us to easily add dynamics and effects by index.
        if type(new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]) != list:
            item_list = [effect, new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]]
            new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]] = item_list
        else:
            new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]].insert(0, effect)


def add_env(note):
    """
    Adds an envelope to a Note
    :param note: A Note
    :return:
    """
    if note.duration > 1:
        note.env = sc_data_gen.env6_strong_atk(note.duration)
        note.envlen = 6
    elif note.duration >= 0.25:
        note.env = sc_data_gen.env5_strong_atk(note.duration)
        note.envlen = 5
    else:
        note.env = sc_data_gen.env4_strong_atk(note.duration)
        note.envlen = 4


def batch_fm_synth_update(new_parts, updates):
    """
    Performs a batch update of synth indices
    :param new_parts: A list of parts
    :param updates: A tuple (or list). Index 1 is a tuple/list containing the index of the node to update.
    Index 2 is the new synth index.
    :return:
    """
    for item in updates:
        dur = new_parts[item[0][0]][item[0][1]][item[0][2]].duration
        new_parts[item[0][0]][item[0][1]][item[0][2]].synth = item[1] + len(item[2])
        new_parts[item[0][0]][item[0][1]][item[0][2]].mod_levels = item[2]
        new_parts[item[0][0]][item[0][1]][item[0][2]].mod_curves = item[4]
        new_parts[item[0][0]][item[0][1]][item[0][2]].mod_times = [float(dur * n) for n in item[3]]


def batch_dynamic_synth_update(new_parts):
    """
    Performs a batch update of dynamic synths
    :param new_parts: A list of parts
    :return:
    """
    for part in new_parts:
        for voice in part:
            for item in voice:
                if type(item) == list:
                    for item2 in item:
                        if type(item2) == Dynamic:
                            item2.times = [float(n * item2.duration) for n in item2.times]


def build_score():
    """
    Builds the SuperCollider score
    :return:
    """
    parsed_parts1 = xml_parse_sc.analyze_xml(f"{FOLDER}\\{FILE1}")
    parsed_parts2 = xml_parse_sc.analyze_xml(f"{FOLDER}\\{FILE2}")

    # Data structures that hold score updates
    # Dynamics to insert into the score
    dynamics1 = [
        Dynamic(synth=3, levels=[2, 5, 1, 0, 0], times=[1/3, 2/3, 0, 0, 0], curves=[0, 0, 0, 0], start_note=(0, 0, 0),
                end_note=(0, 0, 0)),
        Dynamic(synth=3, levels=[2, 5, 1, 0, 0], times=[1/3, 2/3, 0, 0, 0], curves=[0, 0, 0, 0], start_note=(0, 5, 0),
                end_note=(0, 5, 0))
    ]
    # A data structure that holds conversion information for FM synths. Index 1 holds the synth index in the score,
    # Index 2 is the new synth index, Index 3 is the dynamic values for the envelope, Index 4 is the time points
    # (excluding start) where dynamic peaks and valleys are, and Index 5 is the list of envelope curves.
    # The envelope times will be calculated automatically from Index 4. The values in Index 4 must sum to 1.
    synth_updates1 = [
        [[0, 0, 0], 10, [0.2, 0.5], [1], [0]], # time is 1 because it takes the entire duration of the synth to get from beginning to end of the timbre envelope
        [[0, 0, 1], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 2], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 3], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 4], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 0], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 1], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 2], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 3], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 4], 10, [0.2, 0.5], [1], [0]],

        # m13
        [[0, 0, 19], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 5], 10, [0.2, 0.5], [1], [0]],

        # m15
        [[0, 0, 20], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 6], 10, [0.2, 0.5], [1], [0]],

        # m16
        [[0, 5, 7], 10, [0.2, 0.5], [1], [0]],

        # m21
        [[0, 0, 21], 10, [0.2, 0.5], [1], [0]],
        [[0, 3, 0], 10, [0.2, 0.5], [1], [0]],
        [[0, 4, 0], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 12], 10, [0.2, 0.5], [1], [0]],

        # m23
        [[0, 0, 22], 10, [0.2, 0.5], [1], [0]],
        [[0, 3, 1], 10, [0.2, 0.5], [1], [0]],
        [[0, 4, 1], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 13], 10, [0.2, 0.5], [1], [0]],

        # m29
        [[0, 0, 36], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 16], 10, [0.2, 0.5], [1], [0]],

        # m30
        [[0, 0, 39], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 18], 10, [0.2, 0.5], [1], [0]],

        # m33
        [[0, 0, 49], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 51], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 19], 10, [0.2, 0.5], [1], [0]],

        # m41-48
        [[0, 0, 90], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 91], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 92], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 93], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 96], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 97], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 98], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 23], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 24], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 25], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 26], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 28], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 30], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 31], 10, [0.2, 0.5], [1], [0]],
        [[0, 7, 0], 10, [0.2, 0.5], [1], [0]],

        # m48-55
        [[0, 0, 112], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 114], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 115], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 116], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 117], 10, [0.2, 0.5], [1], [0]],
        [[0, 3, 7], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 90], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 32], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 33], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 35], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 38], 10, [0.2, 0.5], [1], [0]],
        [[0, 7, 1], 10, [0.2, 0.5], [1], [0]],

        # m58
        [[0, 0, 135], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 49], 10, [0.2, 0.5], [1], [0]],

        # m68-75
        [[0, 0, 147], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 150], 10, [0.2, 0.5], [1], [0]],
        [[0, 0, 151], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 75], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 76], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 82], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 85], 10, [0.2, 0.5], [1], [0]],

        # m76-78
        [[0, 5, 86], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 90], 10, [0.2, 0.5], [1], [0]],
        [[0, 7, 4], 10, [0.2, 0.5], [1], [0]],

        # m79-81
        [[0, 5, 93], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 94], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 95], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 96], 10, [0.2, 0.5], [1], [0]],

        # m87-89
        [[0, 0, 207], 10, [0.2, 0.5], [1], [0]],
        [[0, 1, 16], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 97], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 98], 10, [0.2, 0.5], [1], [0]],
        [[0, 6, 2], 10, [0.2, 0.5], [1], [0]],
        [[0, 6, 3], 10, [0.2, 0.5], [1], [0]],

    ]

    # Output the score for manual edit planning
    xml_parse_sc.dump_parts(parsed_parts1)

    # Add data
    add_sc_data(parsed_parts1)
    add_sc_data(parsed_parts2)
    batch_fm_synth_update(parsed_parts1, synth_updates1)
    add_effects(parsed_parts1, dynamics1)
    batch_dynamic_synth_update(parsed_parts1)
    collapse_voices(parsed_parts1)

    # Create the SuperCollider score
    xml_parse_sc.dump_sc_to_file(f"{OUTPUT}\\score1.scd", parsed_parts1, "score_1_maker")
    xml_parse_sc.dump_sc_to_file(f"{OUTPUT}\\score2.scd", parsed_parts2, "score_2_maker")


def collapse_voices(new_parts):
    """
    Collapses separately chained notes in a list of parts
    :param new_parts: A list of parts
    :return: None
    """
    for part in new_parts:
        for voice in part:
            i = 0
            while i < len(voice):
                if type(voice[i]) == list:
                    if len(voice[i]) > 0:
                        current = voice[i]
                        for j in range(len(current) - 1, -1, -1):
                            voice.insert(i, current[j])
                        current.clear()
                    else:
                        del voice[i]
                else:
                    i += 1


if __name__ == "__main__":
    build_score()
