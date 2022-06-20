"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from mgen import xml_parse_sc, sc_data_gen
import random
import time

FOLDER = "H:\\My Drive\\Composition\\Compositions\\Trombone Piece"
FILE = "Trombone Piece 0.2.1 - Full score - 01 Flow 1.xml"
NUM_BUFFERS = 8
random.seed(time.time())


def add_sc_data(new_parts):
    """
    Adds buffer indices to a list of new parts for SuperCollider
    :param new_parts: A list of new parts
    :return:
    """
    for p in new_parts:
        for v in p:
            for v2 in v:
                for note in v2:
                    add_buf(note)
                    add_env(note)
                    note.mul = 5


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
    m_last = xml_parse_sc.get_highest_measure_no(parsed_parts)
    add_sc_data(parsed_parts)
    # xml_parse_sc.dump_parts(parsed_parts)
    xml_parse_sc.dump_sc_to_file(f"{FOLDER}\\SuperCollider\\score.scd", parsed_parts)
    xml_parse_sc.dump_parts(parsed_parts)
