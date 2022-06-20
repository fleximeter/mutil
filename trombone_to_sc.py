"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from mgen import xml_parse_sc, sc_data_gen
from mgen.xml_parse_sc import Dynamic
import random
import time

FOLDER = "H:\\My Drive\\Composition\\Compositions\\Trombone Piece"
FILE = "Trombone Piece 0.2.1 - Full score - 01 Flow 1.xml"
NUM_BUFFERS = 8
NUM_BUSES = 40
random.seed(time.time())


def add_sc_data(new_parts):
    """
    Adds buffer indices to a list of new parts for SuperCollider
    :param new_parts: A list of new parts
    :return:
    """
    i = 0
    for p in new_parts:
        for v in p:
            for v2 in v:
                for note in v2:
                    add_buf(note)
                    add_env(note)
                    note.mul = 5
                    note.bus_out = NUM_BUSES - 10 + i
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
    # Iterate through each part, voice, and subvoice to add corresponding dynamics
    for i in range(len(new_parts)):  # part
        n = 0
        for j in range(len(dynamic_parts[i])):  # voice
            for k in range(len(dynamic_parts[i][j])):  # subvoice
                for m in range(len(dynamic_parts[i][j][k])):  # note
                    if m < len(new_parts[i][j][k]):
                        # Insert the dynamic if it is here
                        if type(dynamic_parts[i][j][k][m]) == Dynamic:
                            if dynamic_parts[i][j][k][m].start_time < 0:
                                # Update the start time of the dynamic if it is not manually specified
                                # to match the start time of the next note in the sequence
                                dynamic_parts[i][j][k][m].start_time = new_parts[i][j][k][n].start_time

                            # Set the input and output bus indices for the Dynamic synth
                            dynamic_parts[i][j][k][m].bus_in = new_parts[i][j][k][n].bus_out - 10
                            dynamic_parts[i][j][k][m].bus_out = new_parts[i][j][k][n].bus_out

                            # Update the output buses of the affected notes to go to the Dynamic synth
                            for o in range(m, len(new_parts[i][j][k])):
                                if new_parts[i][j][k][o].end_time <= dynamic_parts[i][j][k][m].start_time + \
                                        dynamic_parts[i][j][k][m].duration:
                                    new_parts[i][j][k][o].bus_out -= 10
                                else:
                                    break

                            new_parts[i][j][k].insert(n, dynamic_parts[i][j][k][m])
                        else:
                            new_parts[i][j][k][n].mul = dynamic_parts[i][j][k][m]
                        n += 1


def add_effects(new_parts, effects):
    """
    Adds effects to a list of parsed parts. Updates buses.
    :param new_parts: A list of parsed parts
    :param effects: A list of effects
    :return:
    """
    # Iterate through each part, voice, and subvoice to add corresponding effects
    for i in range(len(new_parts)):  # part
        n = 0
        for j in range(len(new_parts[i])):  # voice
            for k in range(len(new_parts[i][j])):  # subvoice
                for m in range(len(effects[i][j][k])):  # note
                    # Set the input and output bus indices for the Effect synth
                    effects[i][j][k][m].bus_in = new_parts[i][j][k][effects[i][j][k][m].start_index].bus_out - 10
                    effects[i][j][k][m].bus_out = new_parts[i][j][k][effects[i][j][k][m].start_index].bus_out
                    effects[i][j][k][m].start_time = new_parts[i][j][k][effects[i][j][k][m].start_index].start_time

                    # Update the output buses of the affected notes to go to the Effect synth
                    for o in range(effects[i][j][k][m].start_index, len(new_parts[i][j][k])):
                        if new_parts[i][j][k][o].end_time <= new_parts[i][j][k][effects[i][j][k][m].start_index]. \
                                start_time + effects[i][j][k][m].duration:
                            new_parts[i][j][k][o].bus_out -= 10
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
    dynamics = [[
        [[Dynamic(curvesynth=1, start_level=-4, end_level=-1, duration=4)]],
        [[], []],
        [[Dynamic(curvesynth=1, start_level=-4, end_level=-1, duration=4, start_time=2.5)]]
    ]]
    parsed_parts = xml_parse_sc.analyze_xml(f"{FOLDER}\\{FILE}", 1)
    m_last = xml_parse_sc.get_highest_measure_no(parsed_parts)
    add_sc_data(parsed_parts)
    add_dynamics(parsed_parts, dynamics)
    xml_parse_sc.dump_sc_to_file(f"{FOLDER}\\SuperCollider\\score.scd", parsed_parts)
    xml_parse_sc.dump_parts(parsed_parts)
