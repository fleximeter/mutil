"""
File: pseg.py
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


def intervals(pseg: list):
    """
    Gets the ordered interval content of a pseg
    :param pseg: The pseg
    :return: The ordered interval content as a list
    """
    intlist = []
    for i in range(1, len(pseg)):
        intlist.append(pseg[i].p - pseg[i - 1].p)
    return intlist
    

def invert(pseg: list):
    """
    Inverts a pseg
    :param pseg: The pseg
    :return: The inverted pseg
    """
    pseg2 = []
    for p in pseg:
        pseg2.append(pitch.Pitch12(p.p * -1))
    return pseg2


def m21_make_pseg(item):
    """
    Makes a pseg from a music21 object
    :param item: A music21 object
    :return: A pseg
    """
    pseg2 = []
    if type(item) == music21.note.Note:
        pseg2.append(pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.pitch.Pitch:
        pseg2.append(pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.chord.Chord:
        for p in item.pitches:
            pseg2.append(pitch.Pitch12(p.midi - 60))
    else:
        raise TypeError("Unsupported music21 type")
    return pseg2


def multiply_order(pseg: list, n: int):
    """
    Multiplies a pseg's order
    :param pseg: The pseg
    :param n: The multiplier
    :return: The order-multiplied pseg
    """
    pseg2 = []
    for i in range(len(pseg)):
        pseg2.append(pitch.Pitch12(pseg[(i * n) % len(pseg)].p))
    return pseg2


def retrograde(pseg: list):
    """
    Retrogrades a pseg
    :param pseg: The pseg
    :return: The retrograded pseg
    """
    pseg2 = []
    for i in range(len(pseg) - 1, -1, -1):
        pseg2.append(pitch.Pitch12(pseg[i].pc))
    return pseg2


def rotate(pseg: list, n: int):
    """
    Rotates a pseg
    :param pseg: The pseg
    :param n: The index of rotation
    :return: The rotated pseg
    """
    pseg2 = []
    for i in range(len(pseg)):
        pseg2.append(pitch.Pitch12(pseg[(i - n) % len(pseg)].p))
    return pseg2


def transpose(pseg: list, n: int):
    """
    Transposes a pseg
    :param pseg: The pseg
    :param n: The index of transposition
    :return: The transposed pseg
    """
    pseg2 = []
    for p in pseg:
        pseg2.append(pitch.Pitch12(p.p + n))
    return pseg2
