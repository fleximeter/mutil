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
    def __init__(self, transpose=0, retrograde=0, multiply=1):
        """
        Creates a RO
        :param transpose: The index of transposition
        :param retrograde: Whether or not to retrograde
        :param multiply: The multiplier
        """
        self._ro = [transpose, retrograde, multiply]

    def __eq__(self, other):
        return self._ro[0] == other.tto[0] and self._ro[1] == other.tto[1] and self._ro[2] == other.tto[2]

    def __getitem__(self, item):
        return self._ro[item]

    def __hash__(self):
        return self._ro[0] * 1000 + self._ro[1] * 100 + self._ro[2]

    def __ne__(self, other):
        return self._ro[0] != other.tto[0] or self._ro[1] != other.tto[1] or self._ro[2] != other.tto[2]

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
        self._ro[0] %= 12
        self._ro[2] %= 12
        if self._ro[0] < 0:
            self._ro[0] += 12
        if self._ro[2] < 0:
            self._ro[2] += 12

    @property
    def transpose_n(self):
        """
        The index of transposition
        :return: The index of transposition
        """
        return self._ro[0]

    @property
    def multiply_n(self):
        """
        The multiplier
        :return: The multiplier
        """
        return self._ro[2]

    @property
    def invert(self):
        """
        Whether or not this RO has an inversion operator
        :return: A boolean
        """
        return self._ro[1] == 11 or self._ro == 7

    def transform(self, pcseg: list):
        """
        Transforms a pcseg
        :param pcseg: A pcseg
        :return: The transformed pcseg
        """
        pcseg2 = list()
        for i in range(len(pcseg)):
            pcseg2.append(pitch.PitchClass(pcseg[i].pc * self._ro[2] + self._ro[0]))
        if self._ro[1]:
            pcseg2.reverse()
        return pcseg2


class TTO:
    """
    Represents a twelve-tone operator (TTO). Objects of this class are subscriptable.
    [0] is the index of transposition. [1] is the multiplier. Multiplication is performed first,
    then transposition.
    """
    def __init__(self, transpose=0, multiply=1):
        """
        Creates a TTO
        :param transpose: The index of transposition
        :param multiply: The multiplier
        """
        self._tto = [transpose, multiply]

    def __eq__(self, other):
        return self._tto[0] == other.tto[0] and self._tto[1] == other.tto[1]

    def __getitem__(self, item):
        return self._tto[item]

    def __ge__(self, other):
        return self._tto[1] > other[1] or (self._tto[1] == other[1] and self._tto[0] >= other[0])

    def __gt__(self, other):
        return self._tto[1] > other[1] or (self._tto[1] == other[1] and self._tto[0] > other[0])

    def __hash__(self):
        return self._tto[0] * 100 + self._tto[1]

    def __le__(self, other):
        return self._tto[1] < other[1] or (self._tto[1] == other[1] and self._tto[0] <= other[0])

    def __lt__(self, other):
        return self._tto[1] < other[1] or (self._tto[1] == other[1] and self._tto[0] < other[0])

    def __ne__(self, other):
        return self._tto[0] != other.tto[0] or self._tto[1] != other.tto[1]

    def __repr__(self):
        return f"T{self._tto[0]}M{self._tto[1]}"

    def __str__(self):
        return f"T{self._tto[0]}M{self._tto[1]}"

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
        self._tto[1] %= 12
        if self._tto[0] < 0:
            self._tto[0] += 12
        if self._tto[1] < 0:
            self._tto[1] += 12

    @property
    def transpose_n(self):
        """
        The index of transposition
        :return: The index of transposition
        """
        return self._tto[0]

    @property
    def multiply_n(self):
        """
        The multiplier
        :return: The multiplier
        """
        return self._tto[1]

    @property
    def has_invert(self):
        """
        Whether or not this TTO has an inversion operator
        :return: A boolean
        """
        return self._tto[1] == 11 or self._tto == 7

    @property
    def type(self):
        """
        The OperatorType of the TTO
        :return: The OperatorType
        """
        match self._tto[1]:
            case 5:
                return OperatorType.TnM5
            case 7:
                return OperatorType.TnM7
            case 11:
                return OperatorType.TnI
            case _:
                return OperatorType.Tn

    def cycles(self):
        """
        Gets the cycles of the TTO
        :return: The cycles, as a list of lists
        """
        int_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        cycles = []
        while len(int_list) > 0:
            cycle = [pitch.PitchClass(int_list[0])]
            n = (cycle[0].pc * self._tto[1] + self._tto[0]) % 12
            while n != cycle[0].pc:
                cycle.append(pitch.PitchClass(n))
                int_list.remove(n)
                n = (cycle[len(cycle)-1].pc * self._tto[1] + self._tto[0]) % 12
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
            for pc in item:
                pcset2.add(pitch.PitchClass(pc.pc * self._tto[1] + self._tto[0]))
            return pcset2
        elif type(item) == list:
            pcseg2 = list()
            for pc in item:
                pcseg2.append(pitch.PitchClass(pc.pc * self._tto[1] + self._tto[0]))
            return pcseg2
        elif type(item) == pitch.PitchClass:
            return pitch.PitchClass(item.pc * self._tto[1] + self._tto[0])
        else:
            return (item * self._tto[1] + self._tto[0]) % 12


def get_ros(*args):
    """
    Gets ROs
    :param args: One or more RO categories (OperatorType)
    :return: A list of ROs
    """
    arg_set = set(args)
    ros = []
    if OperatorType.Tn in arg_set:
        for i in range(12):
            ros.append(RO(i))
    if OperatorType.TnI in arg_set:
        for i in range(12):
            ros.append(RO(i, 0, 11))
    if OperatorType.TnM5 in arg_set:
        for i in range(12):
            ros.append(RO(i, 0, 5))
    if OperatorType.TnM7 in arg_set:
        for i in range(12):
            ros.append(RO(i, 0, 7))
    if OperatorType.RTn in arg_set:
        for i in range(12):
            ros.append(RO(i, 1))
    if OperatorType.RTnI in arg_set:
        for i in range(12):
            ros.append(RO(i, 1, 11))
    if OperatorType.RTnM5 in arg_set:
        for i in range(12):
            ros.append(RO(i, 1, 5))
    if OperatorType.RTnM7 in arg_set:
        for i in range(12):
            ros.append(RO(i, 1, 7))
    return ros


def get_ttos(*args):
    """
    Gets TTOs
    :param args: One or more TTO categories (OperatorType)
    :return: A list of TTOs
    """
    arg_set = set(args)
    ttos = []
    if OperatorType.Tn in arg_set:
        for i in range(12):
            ttos.append(TTO(i))
    if OperatorType.TnI in arg_set:
        for i in range(12):
            ttos.append(TTO(i, 11))
    if OperatorType.TnM5 in arg_set:
        for i in range(12):
            ttos.append(TTO(i, 5))
    if OperatorType.TnM7 in arg_set:
        for i in range(12):
            ttos.append(TTO(i, 7))
    return ttos


def left_multiply_ttos(*args):
    """
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
        tto_list.append(TTO(tto[0], tto[1]))
    return tto_list
