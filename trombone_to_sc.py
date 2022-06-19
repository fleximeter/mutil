"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from mgen import xml_parse_sc

FOLDER = "H:\\My Drive\\Composition\\Compositions\\Trombone Piece"
FILE = "Trombone Piece 0.2.1 - Full score - 01 Flow 1.xml"


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

                    if note.duration > 1:
                        note.env = f"[[0, 1, 0.9, 0.65, 0.65, 0, 0, 0, 0, 0], [0.04, 0.1, 0.08, " \
                                   f"{note.duration - 0.04 - 0.1 - 0.08 - 0.15}, 0.15, 0, 0, 0, 0], " \
                                   f"[4, -2, -4, 0, -4, 0, 0, 0, 0]]"
                        note.synth_index = 2
                    elif note.duration >= 0.2:
                        note.env = f"[[0, 1, 0.65, 0, 0, 0, 0, 0, 0, 0], [0.03, {note.duration - 0.03 - 0.05}, " \
                                   f"0.05, 0, 0, 0, 0, 0, 0], [4, -4, -4, 0, 0, 0, 0, 0, 0]]"
                    else:
                        note.env = f"[[0, 1, 0.9, 0.65, 0, 0, 0, 0, 0, 0], [0.02, 0.08, " \
                                   f"{note.duration - 0.02 - 0.08 - 0.03}, 0.03, 0, 0, 0, 0, 0], " \
                                        f"[4, -2, -5, -4, 0, 0, 0, 0, 0]]"

                    note.mul = 1


if __name__ == "__main__":
    parsed_parts = xml_parse_sc.analyze_xml(f"{FOLDER}\\{FILE}", 1)
    m_last = xml_parse_sc.get_highest_measure_no(parsed_parts)
    add_sc_data(parsed_parts)
    # xml_parse_sc.dump_parts(parsed_parts)
    xml_parse_sc.dump_sc_to_file(f"{FOLDER}\\SuperCollider\\score.scd", parsed_parts,
                                 xml_parse_sc.get_highest_measure_no(parsed_parts))
