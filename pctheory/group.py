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
    def __init__(self, ttos: list = None):
        """
        Creates an OperatorGroup
        :param ttos: TTOs
        """
        self._name = ""
        self._ttos = []
        self._tn = []
        self._tni = []
        self._tnm5 = []
        self._tnm7 = []
        self._ttos = []
        if ttos is not None:
            self.load_ttos(ttos)

    @property
    def name(self):
        """
        Gets the group name
        :return: The group name
        """
        group_name = "G"
        if len(self._tn) == 12:
            group_name += "*"
        else:
            for tto in self._tn:
                group_name += str(tto[0])
        if len(self._tni) > 0 or len(self._tnm5) > 0 or len(self._tnm7) > 0:
            group_name += "/"
        if len(self._tni) == 12:
            group_name += "*"
        else:
            for tto in self._tni:
                group_name += str(tto[0])
        if len(self._tnm5) > 0 or len(self._tnm7) > 0:
            group_name += "/"
        if len(self._tnm5) == 12:
            group_name += "*"
        else:
            for tto in self._tnm5:
                group_name += str(tto[0])
        if len(self._tnm7) > 0:
            group_name += "/"
        if len(self._tnm7) == 12:
            group_name += "*"
        else:
            for tto in self._tnm7:
                group_name += str(tto[0])
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
                operator_table[i][j] = self._ttos[i].transform(operator_table[0][j])

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
        for t in self._ttos:
            coset.append(transformations.left_multiply_utos(tto, t))
        coset.sort()
        return coset

    def load_ttos(self, ttos: list):
        """
        Loads TTOs into the group
        :param ttos: TTOs
        :return:
        """
        for tto in ttos:
            match tto[1]:
                case 1:
                    self._tn.append(tto)
                case 5:
                    self._tnm5.append(tto)
                case 7:
                    self._tnm7.append(tto)
                case 11:
                    self._tni.append(tto)
            self._ttos.append(tto)
        self._tn.sort()
        self._tni.sort()
        self._tnm5.sort()
        self._tnm7.sort()
        self._ttos.sort()

    def right_coset(self, tto):
        """
        Gets a right coset of the group
        :param tto: A TTO
        :return: The right coset
        """
        coset = []
        for t in self._ttos:
            coset.append(transformations.left_multiply_utos(t, tto))
        coset.sort()
        return coset
