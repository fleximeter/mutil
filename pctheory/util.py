"""
File: util.py
Author: Jeff Martin
Date: 11/13/2021

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


def map_to_chromatic(scale_map, sequence):
    """
    Maps a diatonic collection to the chromatic collection
    :param scale_map: The scale map
    :param sequence: The sequence to map
    :return: The mapped sequence
    """
    CMOD = 12
    smod = len(scale_map)
    sequence2 = []
    for p in sequence:
        pc = ((p % smod) + smod) % smod
        p2 = (p // smod) * CMOD + scale_map[pc]
        sequence2.append(p2)
    return sequence2


def norgard(n: int):
    """
    Generates the first n numbers of OEIS A004718 (Per Nørgård's infinity series)
    :param n: The number of terms to compute
    :return: The series
    """
    n_list = [0 for i in range(n)]
    i = 0
    m = 0
    while m < n:
        m = 2 * i
        if m < n:
            n_list[m] = -n_list[i]
        m += 1
        if m < n:
            n_list[m] = n_list[i] + 1
        i += 1
    return n_list
