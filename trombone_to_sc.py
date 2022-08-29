"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from mgen import xml_parse_sc, sc_data_gen
from mgen.xml_parse_sc import Dynamic, Effect, Note
import random
import time

FOLDER = "H:\\My Drive\\Composition\\Compositions\\Trombone Piece"
FILE = "Trombone Piece 0.2.4 - Full score - 01 Flow 1.xml"
NUM_BUFFERS = 8
NUM_BUSES = 80
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
                note.bus_out = NUM_BUSES - 20 + i
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


def add_dynamics(new_parts, dynamic_parts):
    """
    Adds dynamics to a list of parsed parts. Updates buses.
    :param new_parts: A list of parsed parts
    :param dynamic_parts: A list of dynamic parts
    :return:
    """

    # Iterate through each dynamic entry for the current voice
    for dynamic in dynamic_parts:
        # Identify the starting and ending notes
        start_note = new_parts[dynamic.start_note[0]][dynamic.start_note[1]][dynamic.start_note[2]]
        end_note = new_parts[dynamic.start_note[0]][dynamic.start_note[1]][dynamic.start_note[2]]
        if type(start_note) == list:
            for item in start_note:
                if type(item) == Note:
                    start_note = item
                    break
        if type(end_note) == list:
            for item in end_note:
                if type(item) == Note:
                    end_note = item
                    break

        # Set times and duration
        dynamic.start_time = start_note.start_time
        dynamic.end_time = end_note.end_time
        dynamic.duration = dynamic.end_time - dynamic.start_time

        # When adding dynamics, we use separate chaining. That is, we create a list containing the dynamic
        # and starting note, and put that list into the voice where the starting note used to be.
        # We will go through the voice and flatten it out later, after all dynamics and effects are added.
        # This allows us to easily add dynamics and effects by index.
        if type(new_parts[dynamic.index_insert[0]][dynamic.index_insert[1]][dynamic.index_insert[2]]) != list:
            item_list = [dynamic, new_parts[dynamic.index_insert[0]][dynamic.index_insert[1]][dynamic.index_insert[2]]]
            new_parts[dynamic.index_insert[0]][dynamic.index_insert[1]][dynamic.index_insert[2]] = item_list
        else:
            new_parts[dynamic.index_insert[0]][dynamic.index_insert[1]][dynamic.index_insert[2]].insert(0, dynamic)

        for i in range(dynamic.start_note[2], dynamic.end_note[2] + 1):
            pass

def add_effects(new_parts, effects):
    """
    Adds effects to a list of parsed parts. Updates buses.
    :param new_parts: A list of parsed parts
    :param effects: A list of effects
    :return:
    """
    # Iterate through each effect entry for the current voice
    for effect in effects:
        effect.start_time = effect.start_note.start_time
        effect.end_time = effect.end_note.end_time
        effect.duration = effect.end_time - effect.start_time

        # When adding effects, we use separate chaining. That is, we create a list containing the effect
        # and starting note, and put that list into the voice where the starting note used to be.
        # We will go through the voice and flatten it out later, after all dynamics and effects are added.
        # This allows us to easily add dynamics and effects by index.
        if type(new_parts[effect.index_insert[0]][effect.index_insert[1]][effect.index_insert[2]]) != list:
            item_list = [effect, new_parts[effect.index_insert[0]][effect.index_insert[1]][effect.index_insert[2]]]
            new_parts[effect.index_insert[0]][effect.index_insert[1]][effect.index_insert[2]] = item_list
        else:
            new_parts[effect.index_insert[0]][effect.index_insert[1]][effect.index_insert[2]].insert(0, effect)

    # Iterate through each part, voice, and subvoice to add corresponding effects
    for i in range(len(new_parts)):  # part
        n = 0
        for j in range(len(new_parts[i])):  # voice
            for k in range(len(new_parts[i][j])):  # subvoice
                for m in range(len(effects[i][j][k])):  # note
                    # Set the input and output bus indices for the Effect synth
                    effects[i][j][k][m].bus_in = new_parts[i][j][k][effects[i][j][k][m].start_index].bus_out - 20
                    effects[i][j][k][m].bus_out = new_parts[i][j][k][effects[i][j][k][m].start_index].bus_out
                    effects[i][j][k][m].start_time = new_parts[i][j][k][effects[i][j][k][m].start_index].start_time

                    # Update the output buses of the affected notes to go to the Effect synth
                    for o in range(effects[i][j][k][m].start_index, len(new_parts[i][j][k])):
                        if new_parts[i][j][k][o].end_time <= new_parts[i][j][k][effects[i][j][k][m].start_index]. \
                                start_time + effects[i][j][k][m].duration:
                            new_parts[i][j][k][o].bus_out -= 20
                        else:
                            break

                    new_parts[i][j][k].insert(effects[i][j][k][m].start_index, effects[i][j][k][m])


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


if __name__ == "__main__":
    parsed_parts = xml_parse_sc.analyze_xml(f"{FOLDER}\\{FILE}", 1)
    dynamics = [
        Dynamic(synth=0, start_level=-4, end_level=-1, start_note=(0, 0, 1), end_note=(0, 0, 1)),
        Dynamic(synth=0, start_level=-4, end_level=-1, start_note=(0, 0, 1), end_note=(0, 0, 1))
    ]
    m_last = xml_parse_sc.get_highest_measure_no(parsed_parts)
    add_sc_data(parsed_parts)
    # add_dynamics(parsed_parts, dynamics)
    xml_parse_sc.dump_sc_to_file(f"{FOLDER}\\SuperCollider\\score.scd", parsed_parts)
    xml_parse_sc.dump_parts(parsed_parts)
