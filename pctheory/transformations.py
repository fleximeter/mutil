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


class OTO:
    """
    Represents an ordered tone operator (OTO). If used with a twelve-tone row, it is a row operator (RO).
    Objects of this class are subscriptable. [0] is the index of transposition. [1] is whether or not to
    retrograde (0-no or 1-yes). [2] is the multiplier. Multiplication is performed first, then retrograding,
    then transposition. These operators can be used with pcsegs.
    """
    def __init__(self, T=0, R=0, M=0):
        """
        Creates an OTO
        :param T: The index of transposition
        :param R: Whether or not to retrograde
        :param M: The multiplier
        """
        self._oto = [T, R, M]

    def __eq__(self, other):
        return self._oto[0] == other.oto[0] and self._oto[1] == other.oto[1] and self._oto[2] == other.oto[2]

    def __getitem__(self, item):
        return self._oto[item]

    def __hash__(self):
        return self._oto[0] * 1000 + self._oto[1] * 100 + self._oto[2]

    def __ne__(self, other):
        return self._oto[0] != other.oto[0] or self._oto[1] != other.oto[1] or self._oto[2] != other.oto[2]

    def __repr__(self):
        if self._oto[1] and self._oto[2] != 1:
            return f"T{self._oto[0]}RM{self._oto[2]}"
        elif self._oto[2] != 1:
            return f"T{self._oto[0]}M{self._oto[2]}"
        elif self._oto[1]:
            return f"T{self._oto[0]}R"
        else:
            return f"T{self._oto[0]}"

    def __str__(self):
        if self._oto[1] and self._oto[2] != 1:
            return f"T{self._oto[0]}RM{self._oto[2]}"
        elif self._oto[2] != 1:
            return f"T{self._oto[0]}M{self._oto[2]}"
        elif self._oto[1]:
            return f"T{self._oto[0]}R"
        else:
            return f"T{self._oto[0]}"

    @property
    def oto(self):
        """
        Gets the OTO as a list. Index 0 is the index of transposition, index 1 is whether or not to retrograde, and
        index 2 is the multiplier.
        :return: The OTO
        """
        return self._oto

    @oto.setter
    def oto(self, value):
        """
        Sets the OTO using a list
        :param value: A list
        :return:
        """
        self._oto = value

    def transform(self, pcseg: list):
        """
        Transforms a pcseg
        :param pcseg: A pcseg
        :return: The transformed pcseg
        """
        pcseg2 = list()
        if len(pcseg) > 0:
            if type(pcseg[0]) == pitch.PitchClass24:
                for i in range(len(pcseg)):
                    pcseg2.append(pitch.PitchClass24(pcseg[i].pc * self._oto[2] + self._oto[0]))
            else:
                for i in range(len(pcseg)):
                    pcseg2.append(pitch.PitchClass12(pcseg[i].pc * self._oto[2] + self._oto[0]))
        if self._oto[1]:
            pcseg2.reverse()
        return pcseg2


class UTO:
    """
    Represents an unordered tone operator (UTO), which can be used as a twelve-tone operator (TTO)
    or 24-tone operator (24TO). Objects of this class are subscriptable.
    [0] is the index of transposition. [1] is the multiplier. Multiplication is performed first,
    then transposition.
    """
    def __init__(self, T=0, M=1):
        """
        Creates a UTO
        :param T: The index of transposition
        :param M: Whether or not to multiply
        :param I: Whether or not to invert
        """
        self._uto = [T, M]

    def __eq__(self, other):
        return self._uto[0] == other.uto[0] and self._uto[1] == other.uto[1]

    def __getitem__(self, item):
        return self._uto[item]

    def __hash__(self):
        return self._uto[0] * 100 + self._uto[1]

    def __ne__(self, other):
        return self._uto[0] != other.uto[0] or self._uto[1] != other.uto[1]

    def __repr__(self):
        if self._uto[1] != 1:
            return f"T{self._uto[0]}M{self._uto[1]}"
        else:
            return f"T{self._uto[0]}"

    def __str__(self):
        if self._uto[1] != 1:
            return f"T{self._uto[0]}M{self._uto[1]}"
        else:
            return f"T{self._uto[0]}"

    @property
    def uto(self):
        """
        Gets the UTO as a list. Index 0 is the index of transposition, and index 1
        is the multiplier.
        :return: The UTO
        """
        return self._uto

    @uto.setter
    def uto(self, value):
        """
        Sets the UTO using a list
        :param value: A list
        :return:
        """
        self._uto = value

    def cycles(self, num_pcs=12):
        """
        Gets the cycles of the UTO
        :param num_pcs: The number of possible pcs
        :return: The cycles, as a list of lists
        """
        int_list = [i for i in range(num_pcs)]
        cycles = []
        while len(int_list) > 0:
            cycle = [int_list[0]]
            pc = cycle[0]
            pc = (pc * self._uto[1] + self._uto[0]) % num_pcs
            while pc != cycle[0]:
                cycle.append(pc)
                int_list.remove(pc)
                pc = cycle[len(cycle) - 1]
                pc = (pc * self._uto[1] + self._uto[0]) % num_pcs
            cycles.append(cycle)
            del int_list[0]
        return cycles

    def inverse12(self):
        """
        Gets the inverse of the UTO
        :return: The inverse
        """
        return UTO((self._uto[0] * self._uto[1] * -1) % 12, self._uto[1])

    def transform(self, item):
        """
        Transforms a pcset, pcseg, or pc
        :param item: A pcset, pcseg, or pc
        :return: The transformed item
        """
        t = type(item)
        if t == pitch.PitchClass12:
            return pitch.PitchClass12(item.pc * self._uto[1] + self._uto[0])
        elif t == pitch.PitchClass24:
            return pitch.PitchClass24(item.pc * self._uto[1] + self._uto[0])
        else:
            new_item = t()
            if t == set:
                for i in item:
                    new_item.add(self.transform(i))
            if t == list:
                for i in item:
                    new_item.append(self.transform(i))
            return new_item


def find_utos(pcset1: set, pcset2: set):
    """
    Finds the UTOS that transform pcset1 into pcset2
    :param pcset1: A pcset
    :param pcset2: A transformed pcset
    :return: A list of UTOS
    """
    utos = get_utos12()
    utos_final = {}
    for u in utos:
        if utos[u].transform(pcset1) == pcset2:
            utos_final[u] = utos[u]
    return utos_final


def get_otos12():
    """
    Gets OTOs
    :return: A list of OTOs
    """
    otos = {}
    for i in range(12):
        otos[f"T{i}"] = OTO(i)
        otos[f"T{i}R"] = OTO(i, 1)
        otos[f"T{i}M11"] = OTO(i, 0, 11)
        otos[f"T{i}RM11"] = OTO(i, 1, 11)
        otos[f"T{i}M5"] = OTO(i, 0, 5)
        otos[f"T{i}RM5"] = OTO(i, 1, 5)
        otos[f"T{i}M7"] = OTO(i, 0, 7)
        otos[f"T{i}RM7"] = OTO(i, 1, 7)
        otos[f"T{i}I"] = otos[f"T{i}M11"]
        otos[f"T{i}RI"] = otos[f"T{i}RM11"]
    return otos


def get_otos24():
    """
    Gets chromatic OTOs
    :return: A list of microtonal OTOs
    """
    otos = {}
    for i in range(24):
        otos[f"T{i}"] = OTO(i)
        otos[f"T{i}R"] = OTO(i, 1)
        otos[f"T{i}M5"] = OTO(i, 0, 5)
        otos[f"T{i}RM5"] = OTO(i, 1, 5)
        otos[f"T{i}M7"] = OTO(i, 0, 7)
        otos[f"T{i}RM7"] = OTO(i, 1, 7)
        otos[f"T{i}M11"] = OTO(i, 0, 11)
        otos[f"T{i}RM11"] = OTO(i, 1, 11)
        otos[f"T{i}M13"] = OTO(i, 0, 11)
        otos[f"T{i}RM13"] = OTO(i, 1, 11)
        otos[f"T{i}M17"] = OTO(i, 0, 11)
        otos[f"T{i}RM17"] = OTO(i, 1, 11)
        otos[f"T{i}M19"] = OTO(i, 0, 11)
        otos[f"T{i}RM19"] = OTO(i, 1, 11)
        otos[f"T{i}M23"] = OTO(i, 0, 11)
        otos[f"T{i}RM23"] = OTO(i, 1, 11)
        otos[f"T{i}I"] = otos[f"T{i}M23"]
        otos[f"T{i}RI"] = otos[f"T{i}RM23"]
    return otos


def get_utos12():
    """
    Gets the twelve-tone UTOs (TTOs)
    :return: A dictionary of UTOs
    """
    utos = {}
    for i in range(12):
        utos[f"T{i}"] = UTO(i, 1)
        utos[f"T{i}M5"] = UTO(i, 5)
        utos[f"T{i}M7"] = UTO(i, 7)
        utos[f"T{i}M11"] = UTO(i, 11)
    return utos


def get_utos24():
    """
    Gets the 24-tone UTOs (24TOs)
    :return: A dictionary of UTOs
    """
    utos = {}
    for i in range(24):
        utos[f"T{i}"] = UTO(i, 1)
        utos[f"T{i}M5"] = UTO(i, 5)
        utos[f"T{i}M7"] = UTO(i, 7)
        utos[f"T{i}M11"] = UTO(i, 11)
        utos[f"T{i}M13"] = UTO(i, 13)
        utos[f"T{i}M17"] = UTO(i, 17)
        utos[f"T{i}M19"] = UTO(i, 19)
        utos[f"T{i}M23"] = UTO(i, 23)
    return utos


def left_multiply_utos(*args, num_pcs=12):
    """
    Left-multiplies a list of UTOs
    :param args: A collection of UTOs (can be one argument as a list, or multiple UTOs separated by commas.
    The highest index is evaluated first, and the lowest index is evaluated last.
    :param num_pcs: The number of pcs in the system
    :return: The result
    """
    utos = args

    # If the user provided a list object
    if len(args) == 1:
        if type(args[0]) == list:
            utos = args[0]

    if len(utos) == 0:
        return None
    elif len(utos) == 1:
        return utos[0]
    else:
        n = utos[len(utos) - 1][0]
        m = utos[len(utos)-1][1]
        for i in range(len(utos)-2, -1, -1):
            tr_n = utos[i][0]
            mul_n = utos[i][1]
            m = m * mul_n + tr_n
            n *= mul_n
        return UTO(n % num_pcs, m % num_pcs)


def make_uto_list(*args):
    """
    Makes a UTO list
    :return: A UTO list
    """
    uto_list = []
    for uto in args:
        uto_list.append(UTO(uto[0], uto[1]))
    return uto_list
