"""
Name: pierrot_chords.py
Author: Jeff Martin
Description:
This file generates all chords that could be used in the Pierrot piece.
Here is a test from the desktop
"""

from pctheory import pcset, tables, transformations

# The data table
data_table = tables.create_tables()
current = pcset.make_pcset12(1, 2)


def make_pcsets():
    """
    Makes the prime form pcsets that are used in the piece
    :return: The pcsets
    """
    pcsets = [
        pcset.make_pcset12(0, 1, 4),
        pcset.make_pcset12(0, 1, 5),
        pcset.make_pcset12(0, 2, 6),
        pcset.make_pcset12(0, 3, 7),
        pcset.make_pcset12(0, 1, 4, 8),
        pcset.make_pcset12(0, 1, 4, 6),
        pcset.make_pcset12(0, 1, 3, 7),
        pcset.make_pcset12(0, 1, 4, 6, 8),
        pcset.make_pcset12(0, 3, 4, 5, 8),
        pcset.make_pcset12(0, 1, 4, 5, 7, 9)
    ]
    return pcsets


def make_corpus(pcsets):
    """
    Makes the pcset corpus for the piece
    :param pcsets: The pcsets in prime form
    :return: The corpus
    """
    piece_corpus = set()
    for s in pcsets:
        c = pcset.get_corpus(s)
        piece_corpus = piece_corpus.union(c)
    return piece_corpus


def search_corpus(piece_corpus, search_set):
    """
    Searches a corpus for a provided set
    :param piece_corpus: The piece corpus
    :param search_set: A set
    :return: The set(s) that contain the provided set
    """
    contains = set()
    for p in piece_corpus:
        if search_set.issubset(p) or search_set == p:
            contains.add(p)
    return contains


if __name__ == "__main__":
    sets = make_pcsets()
    pierrot_corpus = make_corpus(sets)
    search = search_corpus(pierrot_corpus, current)
    for item in search:
        print(item)
