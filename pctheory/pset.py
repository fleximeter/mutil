"""
File: pset.py
Author: Jeff Martin
Date: 11/1/2021

Copyright © 2021 by Jeffrey Martin. All rights reserved.
Email: jmartin@jeffreymartincomposer.com
Website: https://jeffreymartincomposer.com

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

from pctheory import pitch, transformations
import music21
import numpy


def fb_class(pset: set, p0: int):
    """
    Gets the FB-class of a pset
    :param pset: The pset
    :param p0: The lowest pitch
    :return: The FB-class as a list of integers
    """
    intlist = []
    for p in pset:
        intlist.append((p.p - p0) % 12)
    intlist.sort()
    if len(intlist) > 0:
        del intlist[0]
    return intlist


def invert(pset: set):
    """
    Inverts a pset
    :param pset: The pset
    :return: The inverted pset
    """
    pset2 = set()
    for p in pset:
        pset2.add(pitch.Pitch12(p.p * -1))
    return pset2


def m21_make_pset(item):
    """
    Makes a pset from a music21 object
    :param item: A music21 object
    :return: A pset
    """
    pset2 = set()
    if type(item) == music21.note.Note:
        pset2.add(pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.pitch.Pitch:
        pset2.add(pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.chord.Chord:
        for p in item.pitches:
            pset2.add(pitch.Pitch12(p.midi - 60))
    else:
        raise TypeError("Unsupported music21 type")
    return pset2


def p_ic_matrix(pset: set):
    """
    Gets the pitch ic-matrix
    :param pset: The pset
    :return: The ic-matrix as a list of lists
    """
    mx = numpy.empty((len(pset), len(pset)))
    pseg = list(pset)
    pseg.sort()
    for i in range(mx.shape[0]):
        for j in range(mx.shape[1]):
            mx[i][j] = abs(pseg[i].p - pseg[j].p)
    return mx


def p_ic_roster(pset: set):
    """
    Gets the pitch ic-roster
    :param pset: The pset
    :return: The ic-roster as a dictionary
    """
    pseg = list(pset)
    roster = {}
    pseg.sort()
    for i in range(len(pseg) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            interval = abs(pseg[i].p - pseg[j].p)
            if interval not in roster:
                roster[interval] = 1
            else:
                roster[interval] += 1
    return roster


def p_set_class(pset: set):
    """
    Gets the set-class of a pset
    :param pset: The pset
    :return: The set-class as a list of integers
    """
    pseg = list(pset)
    pseg.sort()
    intlist = []
    for i in range(1, len(pseg)):
        intlist.append(pseg[i].p - pseg[i - 1].p)
    return intlist


def pcint_class(pset: set):
    """
    Gets the PCINT-class of a pset
    :param pset: The pset
    :return: The PCINT-class as a list of integers
    """
    pseg = list(pset)
    pseg.sort()
    intlist = []
    for i in range(1, len(pseg)):
        intlist.append((pseg[i].p - pseg[i - 1].p) % 12)
    return intlist


def pm_similarity(pset1: set, pset2: set, ic_roster1=None, ic_roster2=None):
    """
    Gets the pitch-measure (PM) similarity between pset1 and pset2
    :param pset1: A pset
    :param pset2: A pset
    :param ic_roster1: The ic_roster for pset 1. If None, will be calculated.
    :param ic_roster2: The ic_roster for pset 2. If None, will be calculated.
    :return: The PM similarity as a tuple of integers
    """
    cint = len(pset1.intersection(pset2))
    ic_shared = 0
    if ic_roster1 is None:
        ic_roster1 = p_ic_roster(pset1)
    if ic_roster2 is None:
        ic_roster2 = p_ic_roster(pset2)
    for ic in ic_roster1:
        if ic in ic_roster2:
            if ic_roster1[ic] < ic_roster2[ic]:
                ic_shared += ic_roster1[ic]
            else:
                ic_shared += ic_roster2[ic]
    return (cint, ic_shared)


def subsets(pset: set):
    """
    Gets all subsets of a pset, using the bit masking solution from
    https://afteracademy.com/blog/print-all-subsets-of-a-given-set
    :param pset: A pset
    :return: A list containing all subsets of the pset
    """
    total = 2 ** len(pset)
    sub = []
    pseg = list(pset)
    pseg.sort()
    for index in range(total):
        sub.append([])
        for i in range(len(pset)):
            if index & (1 << i):
                sub[index].append(pitch.Pitch12(pseg[i].p))
    sub.sort()
    return sub


def transform(pset: set, transformation: transformations.UTO):
    """
    Transforms a pset
    :param pset: A pset
    :param transformation: A transformation
    :return: The transformed set
    """
    pset2 = set()
    for p in pset:
        pset2.add(pitch.Pitch12(p.p * transformation[1] + transformation[0]))
    return pset2


def transpose(pset: set, n: int):
    """
    Transposes a pset
    :param pset: The pset
    :param n: The index of transposition
    :return: The transposed pset
    """
    pset2 = set()
    for p in pset:
        pset2.add(pitch.Pitch12(p.p + n))
    return pset2
