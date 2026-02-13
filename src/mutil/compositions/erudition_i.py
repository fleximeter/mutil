"""
File: trombone.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for making a trombone piece.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from pctheory import pcset, pitch, tempo, transformations
from mgen import xml_gen
import music21

# Old hexachord prime form: [00, 01, 05, 08, 15, 16]
# New hexachord prime form: [00, 01, 06, 10, 14, 17]
s1 = pcset.make_pcset24(0, 4, 9, 10, 17, 20)  # this is T1I of the prime form
sc1 = pcset.SetClass24(s1)
tto = transformations.get_ttos24()
google_drive = "H:\\My Drive"


def list_possible_subsets():
    """
    Lists subsets that you might want to use (not including tritones or microtonal flat tritone)
    :return: None
    """
    sp = list(sc1.get_abstract_subset_classes())
    sp.sort()
    # separate the ones with tritones
    for s in sp:
        if not (s.ic_vector[11] or s.ic_vector[12]):
            print("{0: <25}{1}".format(s.name_prime, s.ic_vector_string))
    for s in sp:
        if s.ic_vector[11] or s.ic_vector[12]:
            print("{0: <25}{1}".format(s.name_prime, s.ic_vector_string))


def display_subset_graph():
    """
    Renders a subset graph
    :return:
    """
    pcset.make_subset_graph(sc1, 3, True)


def display_tempo_table():
    """
    Makes a tempo table
    :return:
    """
    tl = [52.5, 60, 70, 84, 105]
    tempo.plot_tempo_table(tl)


def make_score():
    """
    Makes a score with all of the subset-classes except the null set
    :return:
    """
    score = xml_gen.create_score("Trombone", "Jeffrey Martin")
    xml_gen.add_instrument(score, "Trombone", "Tbn.")

    # Get the subset-classes
    sp = list(sc1.get_abstract_subset_classes())
    sp.sort()

    # Make chords and lyrics
    s_list = []
    lyrics = [[s.name_prime] for s in sp]
    del lyrics[0]  # remove the null set name
    for s in sp:
        # don't add the null set
        if len(s) > 0:
            chord = []
            for n in s.pcset:
                chord.append(pitch.Pitch24(n.pc))
            s_list.append(chord)
    chords = xml_gen.make_music21_list(s_list, [4.0 for item in s_list])
    for c in chords:
        xml_gen.make_semi_closed(c)
        xml_gen.cleanup_semi_closed(c)

    # Make the score
    xml_gen.add_measures(score, len(s_list), meter="4/4")
    xml_gen.add_item(score[1], music21.clef.BassClef(), 1)
    xml_gen.add_sequence(score[1], chords, lyrics)
    xml_gen.export_to_xml(score, google_drive + "\\Composition\\Compositions\\Trombone Piece\\trombone.xml")


if __name__ == "__main__":
    list_possible_subsets()
    # display_subset_graph()
    # display_tempo_table()
    # make_score()
