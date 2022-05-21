"""
File: transformations.py
Author: Jeff Martin
Date: 10/30/2021

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

from enum import Enum
from pctheory import pitch


class OperatorType(Enum):
    """
    Represents operator types
    """
    RTn = 1
    RTnI = 2
    RTnM5 = 3
    RTnM7 = 4
    Tn = 5
    TnI = 6
    TnM5 = 7
    TnM7 = 8


class RO:
    """
    Represents a row operator (RO). Objects of this class are subscriptable.
    [0] is the index of transposition. [1] is whether or not to retrograde (0-no or 1-yes).
    [2] is the multiplier. Multiplication is performed first, then retrograding,
    then transposition. These operators can be used with pcsegs.
    """
    def __init__(self, T=0, R=0, M=0, I=0):
        """
        Creates a RO
        :param T: The index of transposition
        :param R: Whether or not to retrograde
        :param M: Whether or not to multiply
        :param I: Whether or not to invert
        """
        self._ro = [T, R, M, I]

    def __eq__(self, other):
        return self._ro[0] == other.ro[0] and self._ro[1] == other.ro[1] and self._ro[2] == other.ro[2] and \
               self._ro[3] == other.ro[3]

    def __getitem__(self, item):
        return self._ro[item]

    def __hash__(self):
        return self._ro[0] * 10000 + self._ro[1] * 1000 + self._ro[2] * 100 + self._ro[3]

    def __ne__(self, other):
        return self._ro[0] != other.ro[0] or self._ro[1] != other.ro[1] or self._ro[2] != other.ro[2] or \
               self._ro[3] != other.ro[3]

    @property
    def ro(self):
        """
        Gets the RO as a list. Index 0 is the index of transposition, index 1 is whether or not to retrograde, and
        index 2 is the multiplier.
        :return: The RO
        """
        return self._ro

    @ro.setter
    def ro(self, value):
        """
        Sets the RO using a list
        :param value: A list
        :return:
        """
        self._ro = value

    def transform(self, pcseg: list):
        """
        Transforms a pcseg
        :param pcseg: A pcseg
        :return: The transformed pcseg
        """
        pcseg2 = list()
        n = 12
        if len(pcseg) > 0:
            if type(pcseg[0]) == pitch.PitchClass24:
                n = 24
        for i in range(len(pcseg)):
            pc = pcseg[i].pc
            if n == 12:
                if self._ro[3]:
                    pc *= 11
                if self._ro[2]:
                    pc *= 5
            else:
                if self._ro[3]:
                    pc *= 23
                if self._ro[2]:
                    pc *= 17
            pcseg2.append(pitch.PitchClass12(pc + self._ro[0]))
        if self._ro[1]:
            pcseg2.reverse()
        return pcseg2


class TTO:
    """
    Represents a twelve-tone operator (TTO). Objects of this class are subscriptable.
    [0] is the index of transposition. [1] is the multiplier. Multiplication is performed first,
    then transposition.
    """
    def __init__(self, T=0, M=0, I=0):
        """
        Creates a TTO
        :param T: The index of transposition
        :param M: Whether or not to multiply
        :param I: Whether or not to invert
        """
        self._tto = [T, M, I]

    def __eq__(self, other):
        return self._tto[0] == other.tto[0] and self._tto[1] == other.tto[1] and self._tto[2] == other.tto[2]

    def __getitem__(self, item):
        return self._tto[item]

    def __hash__(self):
        return self._tto[0] * 100 + self._tto[1]

    def __ne__(self, other):
        return self._tto[0] != other.tto[0] or self._tto[1] != other.tto[1] or self._tto[2] != other.tto[2]

    def __repr__(self):
        if self._tto[1] and self._tto[2]:
            return f"T{self._tto[0]}MI"
        elif self._tto[2]:
            return f"T{self._tto[0]}I"
        elif self._tto[3]:
            return f"T{self._tto[0]}M"
        else:
            return f"T{self._tto[0]}"

    def __str__(self):
        if self._tto[1] and self._tto[2]:
            return f"T{self._tto[0]}MI"
        elif self._tto[2]:
            return f"T{self._tto[0]}I"
        elif self._tto[3]:
            return f"T{self._tto[0]}M"
        else:
            return f"T{self._tto[0]}"

    @property
    def tto(self):
        """
        Gets the TTO as a list. Index 0 is the index of transposition, and index 1
        is the multiplier.
        :return: The TTO
        """
        return self._tto

    @tto.setter
    def tto(self, value):
        """
        Sets the TTO using a list
        :param value: A list
        :return:
        """
        self._tto = value
        self._tto[0] %= 12

    def cycles12(self):
        """
        Gets the cycles of the TTO
        :return: The cycles, as a list of lists
        """
        int_list = [i for i in range(12)]
        cycles = []
        while len(int_list) > 0:
            cycle = [pitch.PitchClass24(int_list[0])]
            n = cycle[0].pc
            if self._tto[2]:
                n *= 11
            if self._tto[1]:
                n *= 5
            n = (n + self._tto[0]) % 12
            while n != cycle[0].pc:
                cycle.append(pitch.PitchClass24(n))
                int_list.remove(n)
                n = cycle[len(cycle) - 1].pc
                if self._tto[2]:
                    n *= 11
                if self._tto[1]:
                    n *= 5
                n = (n + self._tto[0]) % 12
            del int_list[0]
            cycles.append(cycle)
        return cycles

    def cycles24(self):
        """
        Gets the cycles of the TTO
        :return: The cycles, as a list of lists
        """
        int_list = [i for i in range(24)]
        cycles = []
        while len(int_list) > 0:
            cycle = [pitch.PitchClass24(int_list[0])]
            n = cycle[0].pc
            if self._tto[2]:
                n *= 23
            if self._tto[1]:
                n *= 17
            n = (n + self._tto[0]) % 24
            while n != cycle[0].pc:
                cycle.append(pitch.PitchClass24(n))
                int_list.remove(n)
                n = cycle[len(cycle)-1].pc
                if self._tto[2]:
                    n *= 23
                if self._tto[1]:
                    n *= 17
                n = (n + self._tto[0]) % 24
            del int_list[0]
            cycles.append(cycle)
        return cycles

    def inverse(self):
        """
        Gets the inverse of the TTO
        :return: The inverse
        """
        return TTO((self._tto[0] * self._tto[1] * -1) % 12, self._tto[1])

    def transform(self, item):
        """
        Transforms a pcset, pcseg, or pc
        :param item: A pcset, pcseg, or pc
        :return: The transformed item
        """
        if type(item) == set:
            pcset2 = set()
            if len(item) > 0:
                t = type(next(iter(item)))
                if t == pitch.PitchClass12:
                    for pc in item:
                        pcn = pc.pc
                        if self._tto[2]:
                            pcn *= 11
                        if self._tto[1]:
                            pcn *= 5
                        pcset2.add(pitch.PitchClass12(pcn + self._tto[0]))
                else:
                    for pc in item:
                        pcn = pc.pc
                        if self._tto[2]:
                            pcn *= 23
                        if self._tto[1]:
                            pcn *= 17
                        pcset2.add(pitch.PitchClass24(pcn + self._tto[0]))
            return pcset2
        elif type(item) == list:
            pcseg2 = list()
            if len(item) > 0:
                t = type(next(iter(item)))
                if t == pitch.PitchClass12:
                    for pc in item:
                        pcn = pc.pc
                        if self._tto[2]:
                            pcn *= 11
                        if self._tto[1]:
                            pcn *= 5
                        pcseg2.append(pitch.PitchClass12(pcn + self._tto[0]))
                else:
                    for pc in item:
                        pcn = pc.pc
                        if self._tto[2]:
                            pcn *= 23
                        if self._tto[1]:
                            pcn *= 17
                        pcseg2.append(pitch.PitchClass24(pcn + self._tto[0]))
            return pcseg2
        elif type(item) == pitch.PitchClass12:
            pcn = item.pc
            if self._tto[2]:
                pcn *= 11
            if self._tto[1]:
                pcn *= 5
            return pitch.PitchClass12(pcn + self._tto[0])
        elif type(item) == pitch.PitchClass24:
            pcn = item.pc
            if self._tto[2]:
                pcn *= 23
            if self._tto[1]:
                pcn *= 17
            return pitch.PitchClass24(pcn + self._tto[0])
        else:
            return None


def find_ttos(pcset1: set, pcset2: set):
    """
    Finds the TTOS that transform pcset1 into pcset2
    :param pcset1: A pcset
    :param pcset2: A transformed pcset
    :return: A list of TTOS
    """
    ttos = get_ttos12()
    ttos_final = {}
    for t in ttos:
        if ttos[t].transform(pcset1) == pcset2:
            ttos_final[t] = ttos[t]
    return ttos_final


def get_ros():
    """
    Gets ROs
    :return: A list of ROs
    """
    ros = {}
    for i in range(12):
        ros[f"T{i}"] = RO(i)
        ros[f"T{i}R"] = RO(i, 1)
        ros[f"T{i}I"] = RO(i, 0, 0, 1)
        ros[f"T{i}RI"] = RO(i, 1, 0, 1)
        ros[f"T{i}M"] = RO(i, 0, 1, 0)
        ros[f"T{i}RM"] = RO(i, 1, 1, 0)
        ros[f"T{i}MI"] = RO(i, 0, 1, 1)
        ros[f"T{i}RMI"] = RO(i, 1, 1, 1)
    return ros


def get_ttos12():
    """
    Gets the TTOs
    :return: A dictionary of TTOs
    """
    ttos = {}
    for i in range(12):
        ttos[f"T{i}"] = TTO(i, 0, 0)
        ttos[f"T{i}I"] = TTO(i, 0, 1)
        ttos[f"T{i}M"] = TTO(i, 1, 0)
        ttos[f"T{i}MI"] = TTO(i, 1, 1)
    return ttos


def get_ttos24():
    """
    Gets the TTOs
    :return: A dictionary of TTOs
    """
    ttos = {}
    for i in range(24):
        ttos[f"T{i}"] = TTO(i, 0, 0)
        ttos[f"T{i}I"] = TTO(i, 0, 1)
        ttos[f"T{i}M"] = TTO(i, 1, 0)
        ttos[f"T{i}MI"] = TTO(i, 1, 1)
    return ttos


def left_multiply_ttos(*args):
    """
    NOTE: this function needs to be updated since TTOs were changed. Need a way to support microtonal TTOs.
    Left-multiplies a list of TTOs
    :param args: A collection of TTOs (can be one argument as a list, or multiple TTOs separated by commas.
    The highest index is evaluated first, and the lowest index is evaluated last.
    :return: The result
    """
    ttos = args

    # If the user provided a list object
    if len(args) == 1:
        if type(args[0]) == list:
            ttos = args[0]

    if len(ttos) == 0:
        return None
    elif len(ttos) == 1:
        return ttos[0]
    else:
        m = ttos[len(ttos)-1].transpose_n
        n = ttos[len(ttos)-1].multiply_n
        for i in range(len(ttos)-2, -1, -1):
            m = m * ttos[i].multiply_n + ttos[i].transpose_n
            n *= ttos[i].multiply_n
        return TTO(m % 12, n % 12)


def make_tto_list(*args):
    """
    Makes a TTO list
    :return: A TTO list
    """
    tto_list = []
    for tto in args:
        tto_list.append(TTO(tto[0], tto[1], tto[2]))
    return tto_list
