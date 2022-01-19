"""
File: poset.py
Author: Jeff Martin
Date: 11/7/2021

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

from pctheory import pitch, pcset, pcseg, tables, transformations


class PoPcSet:
    """
    Represents a partially ordered pcset
    """
    _MAX_N = 12

    def __init__(self):
        self._poset = []
        self._set = set()

    def append(self, item: set):
        """
        Appends a pcset to the poset
        :param item: A pcset
        :return: A boolean representing the success of the append operation
        """
        for pc in item:
            if pc in self._set:
                return False
        new_set = item.copy()
        self._poset.append(new_set)
        self._set = self._set.union(new_set)
        return True

    def insert(self, item: set, index: int):
        """
        Inserts a pcset into the poset
        :param item: A pcset
        :param index: The insertion index
        :return: A boolean representing the success of the insert operation
        """
        for pc in item:
            if pc in self._set:
                return False
        new_set = item.copy()
        self._poset.insert(index, new_set)
        self._set = self._set.union(new_set)
        return True
