"""
File: group.py
Author: Jeff Martin
Date: 12/23/2021

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

import numpy
from pctheory import pitch, transformations


class OperatorGroup:
    """
    Represents a group of operators
    """
    def __init__(self, utos: list = None, num_pcs: int = 12):
        """
        Creates an OperatorGroup
        :param utos: TTOs
        :param num_pcs: The number of pcs in the system of the group (chromatic: 12, microtonal: 24)
        """
        self._MNUM_12 = {1, 5, 7, 11}
        self._MNUM_24 = {1, 5, 7, 11, 13, 17, 19, 23}
        self._name = ""
        self._num_pcs = num_pcs
        self._operators = [[] for i in range(len(self._MNUM_12))]
        self._utos = {}
        if utos is not None:
            self.load_utos(utos)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def name(self):
        """
        Gets the group name
        :return: The group name
        """
        group_name = "G"
        if self._num_pcs == 12:
            for i in range(len(self._MNUM_12) - 1):
                if len(self._operators[i]) == 12:
                    group_name += "*"
                else:
                    for uto in self._operators[i]:
                        group_name += str(uto[0])
                group_name += "/"
            if len(self._operators[len(self._MNUM_12) - 1]) == 12:
                group_name += "*"
            else:
                for uto in self._operators[len(self._MNUM_12) - 1]:
                    group_name += str(uto[0])
        else:
            for i in range(len(self._MNUM_24) - 1):
                if len(self._operators[i]) == 24:
                    group_name += "*"
                else:
                    for j in range(len(self._operators[i]) - 1):
                        group_name += f"{self._operators[i][j][0]},"
                    if len(self._operators[i]) > 0:
                        group_name += str(self._operators[i][len(self._operators[i]) - 1][0])
                group_name += "/"
            if len(self._operators[len(self._MNUM_24) - 1]) == 24:
                group_name += "*"
            else:
                for j in range(len(self._operators[len(self._MNUM_24) - 1]) - 1):
                    group_name += f"{self._operators[len(self._MNUM_24) - 1][j][0]},"
                if len(self._operators[len(self._MNUM_24) - 1]) > 0:
                    group_name += str(self._operators[len(self._MNUM_24) - 1][len(self._operators[len(self._MNUM_24) - 1]) - 1][0])
        return group_name

    def get_orbits(self):
        """
        Gets the orbits of the group
        :return: The orbits, as a list of sets
        """
        orbits = []
        n = len(self._tn) + len(self._tni) + len(self._tnm5) + len(self._tnm7)
        operator_table = numpy.empty((n, 12), dtype=numpy.int32)

        # Populate the operator table
        for i in range(12):
            operator_table[0][i] = i
        for i in range(1, n):
            for j in range(0, 12):
                operator_table[i][j] = self._utos[i].transform(operator_table[0][j])

        # Compute the orbits
        for i in range(12):
            orbit = set()
            for j in range(n):
                orbit.add(pitch.PitchClass12(int(operator_table[j][i])))
            if orbit not in orbits:
                orbits.append(orbit)
        return orbits

    def left_coset(self, tto):
        """
        Gets a left coset of the group
        :param tto: A TTO
        :return: The left coset
        """
        coset = []
        for t in self._utos:
            coset.append(transformations.left_multiply_utos(tto, t))
        coset.sort()
        return coset

    def load_utos(self, utos: list):
        """
        Loads TTOs into the group
        :param utos: TTOs
        :return:
        """
        for uto in utos:
            match uto[1]:
                case 1:
                    self._tn.append(uto)
                case 5:
                    self._tnm5.append(uto)
                case 7:
                    self._tnm7.append(uto)
                case 11:
                    self._tni.append(uto)
            self._utos.append(uto)
        self._tn.sort()
        self._tni.sort()
        self._tnm5.sort()
        self._tnm7.sort()
        self._utos.sort()

    def right_coset(self, uto):
        """
        Gets a right coset of the group
        :param uto: A UTO
        :return: The right coset
        """
        coset = []
        for u in self._utos:
            coset.append(transformations.left_multiply_utos(u, uto))
        coset.sort()
        return coset
