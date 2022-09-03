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
FILE = "Trombone Piece 0.2.4 - Full score - 01 erudition I.xml"
NUM_BUFFERS = 8
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
                note.mul = 5
                note.bus_out = NUM_BUSES - CHANGE_BUS_CONSTANT + i
            i += 1


def add_buf(note):
    """
    Adds a buffer to a Note
    :param note: A Note
    :return:
    """
    # Choose a sensible buffer for long notes
    if note.duration >= 1:
        if -200 <= note.pitch.p < -51:
            note.buffer = 0
        elif -51 <= note.pitch.p < -39:
            note.buffer = 4
        elif -39 <= note.pitch.p < -27:
            note.buffer = 1
        elif -27 <= note.pitch.p < -15:
            note.buffer = 5
        elif -15 <= note.pitch.p < -3:
            note.buffer = 2
        elif -3 <= note.pitch.p < 9:
            note.buffer = 6
        elif 9 <= note.pitch.p < 21:
            note.buffer = 3
        elif 21 <= note.pitch.p:
            note.buffer = 7
    # For short notes, choose a random buffer
    else:
        note.buffer = random.randrange(0, NUM_BUFFERS, 1)


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


def batch_synth_update(new_parts, updates):
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


def build_score():
    """
    Builds the SuperCollider score
    :return:
    """
    parsed_parts = xml_parse_sc.analyze_xml(f"{FOLDER}\\{FILE}", 1)

    # Data structures that hold score updates
    # Dynamics to insert into the score
    dynamics = [
        Dynamic(synth=0, levels=[1, 0.1, 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0], start_note=(0, 0, 0),
                end_note=(0, 0, 0)),
        Dynamic(synth=0, levels=[1, 0.1, 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0], start_note=(0, 5, 0),
                end_note=(0, 5, 0))
    ]
    # A data structure that holds conversion information for FM synths. Index 1 holds the synth index in the score,
    # Index 2 is the new synth index, Index 3 is the dynamic values for the envelope, Index 4 is the time points
    # (excluding start) where dynamic peaks and valleys are, and Index 5 is the list of envelope curves.
    # The envelope times will be calculated automatically from Index 4. The values in Index 4 must sum to 1.
    synth_updates = [
        [[0, 0, 0], 10, [0.2, 1], [1], [0]], # time is 1 because it takes the entire duration of the synth to get from beginning to end of the timbre envelope
        [[0, 0, 1], 10, [0.2, 1], [1], [0]],
        [[0, 0, 2], 10, [0.2, 1], [1], [0]],
        [[0, 0, 3], 10, [0.2, 1], [1], [0]],
        [[0, 0, 4], 10, [0.2, 1], [1], [0]],
        [[0, 5, 0], 10, [0.2, 1], [1], [0]],
        [[0, 5, 1], 10, [0.2, 1], [1], [0]],
        [[0, 5, 2], 10, [0.2, 1], [1], [0]],
        [[0, 5, 3], 10, [0.2, 1], [1], [0]],
        [[0, 5, 4], 10, [0.2, 1], [1], [0]]
    ]

    # Output the score for manual edit planning
    xml_parse_sc.dump_parts(parsed_parts)

    # Add data
    add_sc_data(parsed_parts)
    batch_synth_update(parsed_parts, synth_updates)
    add_effects(parsed_parts, dynamics)
    collapse_voices(parsed_parts)

    # Create the SuperCollider score
    xml_parse_sc.dump_sc_to_file(f"{FOLDER}\\SuperCollider\\score.scd", parsed_parts)


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
