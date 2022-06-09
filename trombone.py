"""
File: trombone.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for making a trombone piece.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from pctheory import pcset, tempo, transformations

# Old hexachord prime form: [00, 01, 05, 08, 15, 16]
# New hexachord prime form: [00, 01, 06, 10, 14, 17]
s1 = pcset.make_pcset24(0, 4, 9, 10, 17, 20)  # this is T1I of the prime form
sc1 = pcset.SetClass24(s1)
tto = transformations.get_ttos24()


def list_possible_subsets():
    """
    Lists subsets that you might want to use (not including tritones or microtonal flat tritone)
    :return: None
    """
    sp = list(sc1.get_subset_classes())
    sp.sort()
    for s in sp:
        # don't want tritones
        if not (s.ic_vector[11] or s.ic_vector[12]):
            print("{0: <25}{1}".format(s.name_prime, s.ic_vector_string))
    print("{0: <25}{1}".format(sc1.name_prime, sc1.ic_vector_string))


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


if __name__ == "__main__":
    # list_possible_subsets()
    display_subset_graph()
    # display_tempo_table()
