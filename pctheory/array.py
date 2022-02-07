"""
File: array.py
Author: Jeff Martin
Date: 2/2/2022

Copyright © 2022 by Jeffrey Martin. All rights reserved.
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

from pctheory import pcset, pcset, poset, pitch, tables, transformations


def transform_row_content(array: list, ro: transformations.RO):
    """
    Transforms a 2D array with no nestings
    :param array: An array
    :param ro: A row operator
    :return: The transformed array
    """
    array1 = []
    for i in range(len(array)):
        row = []
        for j in range(len(array[i])):
            if type(array[i][j]) == list:
                row.append(ro.transform(array[i][j]))
            elif type(array[i][j]) == set:
                cell = set()
                for item in array[i][j]:
                    cell.add(pitch.PitchClass(item.pc * ro[2] + ro[0]))
                row.append(cell)
            elif type(array[i][j]) == pitch.PitchClass:
                row.append(pitch.PitchClass(array[i][j].pc * ro[2] + ro[0]))
        array1.append(row)
    return array1


def make_array_chain(array: list, length: int, alt_ret=True):
    """
    Makes a chain of arrays
    :param array: An array
    :param length: The length
    :param alt_ret: Whether or not to alternately retrograde the arrays.
    :return: A chained array
    """
    array1 = []  # The final array
    pcset_start = set()  # The begin-set of the array
    pcset_end = set()  # The end-set of the array

    # Populate the begin-set and end-set
    for i in range(len(array)):
        pcset_start.add(array[i][0])
        pcset_end.add(array[i][len(array[i]) - 1])

    # Add the first array to the final array
    for i in range(len(array)):
        row = []
        for j in range(len(array[i])):
            if type(array[i][j]) == list:
                row.append(list(array[i][j]))
            elif type(array[i][j]) == set:
                row.append(set(array[i][j]))
            else:
                row.append(array[i][j])
        array1.append(row)

    # Add the other arrays
    for i in range(1, length):
        # Get the current end-set
        pcset_end_temp = set()
        for j in range(len(array1)):
            pcset_end_temp.add(array1[j][len(array1[j]) - 1])

        # Get the row operator we need for the transformation, and transform the array
        r = transformations.RO()
        m = None
        if alt_ret and i % 2:
            transformation = transformations.find_ttos(pcset_end, pcset_end_temp)
            r.ro = [transformation[0][0], 0, transformation[0][1]]
            m = transform_row_content(array1, r)
            for j in range(len(m)):
                m[j].reverse()
        else:
            transformation = transformations.find_ttos(pcset_start, pcset_end_temp)
            r.ro = [transformation[0][0], 0, transformation[0][1]]
            m = transform_row_content(array1, r)
        m.reverse()

        # Add the transformed array content to the end of the large array
        for j in range(len(array1)):
            for k in range(len(m)):
                if m[k][0] == array1[j][len(array1[j]) - 1]:
                    for n in range(1, len(m[k])):
                        array1[j].append(m[k][n])
                    del m[k]
                    break

    return array1
