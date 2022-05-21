"""
File: pcseg.py
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

from pctheory import pcset, pitch, tables, transformations
import random


def bip_n(imb_n: list):
    """
    Gets the BIP_n of a list of set-classes generated by IMB_n
    :param imb_n: The IMB_n list
    :return: The BIP_n
    """
    bip = []
    if len(imb_n) > 0:
        for sc in imb_n:
            name = sc.name_forte.split('-')[1]
            name = name.replace("Z", "")
            bip.append(int(name))
        bip.sort()
    return bip


def create_ormap(row: list):
    """
    Creates the ORMAP of a row
    :param row: A row
    :return: The ORMAP
    """
    omap = {}
    for i in range(len(row)):
        omap[pitch.PitchClass12(row[i].pc)] = i
    return omap


def generate_pcseg_from_interval_list(interval_list: list, starting_pc=None):
    """
    Generates a pcseg from an interval list
    :param interval_list: The interval list
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: A pcseg
    """
    if starting_pc is None:
        random.seed()
        pcseg = [pitch.PitchClass12(random.randrange(12))]
        for i in range(len(interval_list)):
            pcseg.append(pitch.PitchClass12(pcseg[i].pc + interval_list[i]))
        return pcseg
    else:
        pcseg = [pitch.PitchClass12(starting_pc)]
        for i in range(len(interval_list)):
            pcseg.append(pitch.PitchClass12(pcseg[i].pc + interval_list[i]))
        return pcseg


def generate_random_all_interval_row(name_tables=None, starting_pc=None):
    """
    Generates a random all-interval row
    :param name_tables: A dictionary of name tables
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: An all-interval row
    """
    _tables = name_tables if name_tables is not None else tables.create_tables()
    random.seed()
    generator = _tables["allIntervalRowGenerators"][random.randrange(len(_tables["allIntervalRowGenerators"]))]
    row = [pitch.PitchClass12(random.randrange(12) if starting_pc is None else starting_pc)]
    for i in range(1, 12):
        row.append(pitch.PitchClass12(row[i - 1].pc + generator[i - 1]))
    return row


def generate_random_pcseg(length: int, non_duplicative=False, starting_pc=None):
    """
    Generates a random pcseg
    :param length: The length of the pcseg
    :param non_duplicative: Whether or not duplicate pcs may occur (must be True to generate a row)
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: A random pcseg
    """
    random.seed()
    pcseg = [pitch.PitchClass12(random.randrange(12) if starting_pc is None else starting_pc)]
    if non_duplicative and 0 < length < 12:
        pcs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        del pcs[pcseg[0].pc]
        for i in range(length - 1):
            j = random.randrange(len(pcs))
            pcseg.append(pitch.PitchClass12(pcs[j]))
            del pcs[j]
    elif not non_duplicative and 0 < length:
        for i in range(length - 1):
            pcseg.append(pitch.PitchClass12(random.randrange(12)))
    else:
        raise ValueError("Invalid length")
    return pcseg


def generate_random_pcseg_from_pcset(pcset: set):
    """
    Generates a random pcseg from a pcset
    :param pcset: A pcset
    :return: A pcseg
    """
    random.seed()
    pcseg = []
    setseg = list(pcset)
    for i in range(len(setseg)):
        j = random.randrange(len(setseg))
        pcseg.append(pitch.PitchClass12(setseg[j].pc))
        del setseg[j]
    return pcseg


def get_intervals(pcseg: list):
    """
    Gets the interval sequence of a pcseg
    :param pcseg: The pcseg
    :return: The interval sequence
    """
    intervals = []
    for i in range(1, len(pcseg)):
        intervals.append(pcseg[i].pc - pcseg[i - 1].pc)
    return intervals


def get_secondary_forms(pcseg: list, subseg: list):
    """
    Gets all secondary forms that contain the provided ordered subseg
    :param pcseg: A pcseg
    :param subseg: A subseg
    :return: A list of secondary forms that contain the subseg, as well as their RO transformations
    """
    secondary_forms = []

    # Get different transformations
    m5 = multiply(pcseg, 5)
    m7 = multiply(pcseg, 7)
    m11 = multiply(pcseg, 11)
    r = retrograde(pcseg)
    rm5 = retrograde(multiply(pcseg, 5))
    rm7 = retrograde(multiply(pcseg, 7))
    rm11 = retrograde(multiply(pcseg, 11))

    # Exhaust all transformations and search them
    for i in range(12):
        t = [[transformations.RO(i, 0, 1), transpose(pcseg, i)], [transformations.RO(i, 0, 5), transpose(m5, i)],
             [transformations.RO(i, 0, 7), transpose(m7, i)], [transformations.RO(i, 0, 11), transpose(m11, i)],
             [transformations.RO(i, 1, 1), transpose(r, i)], [transformations.RO(i, 1, 5), transpose(rm5, i)],
             [transformations.RO(i, 1, 7), transpose(rm7, i)], [transformations.RO(i, 1, 11), transpose(rm11, i)]]

        # Search each transformation in t
        for item in t:
            is_valid = False
            for i in range(len(item[1]) - len(subseg)):
                for j in range(i, i + len(subseg)):
                    if item[1][j] == subseg[j - i]:
                        is_valid = True
                    if not is_valid:
                        break
                if is_valid:
                    secondary_forms.append(item)
                    break

    return secondary_forms


def invert(pcseg: list):
    """
    Inverts a pcseg
    :param pcseg: The pcseg
    :return: The inverted pcseg
    """
    pcseg2 = []
    for pc in pcseg:
        pcseg2.append(pitch.PitchClass12(pc.pc * 11))
    return pcseg2


def imb_n(pcseg: list, n: int, name_tables=None):
    """
    Gets the IMB_n of a pcseg. The IMB_n is the segment of imbricated set-classes of cardinality n.
    :param pcseg: The pcseg
    :param n: The cardinality of imbrication
    :param name_tables: Name tables
    :return: The IMB_n
    """
    imb = set()
    scs = []
    if name_tables is None:
        name_tables = tables.create_tables()
    for i in range(len(pcseg) + 1 - n):
        for j in range(i, i + n):
            imb.add(pcseg[j])
        scs.append(pcset.SetClass12(name_tables, imb))
        imb.clear()
    return scs


def is_valid_row(pcseg: list):
    """
    Determines if a pcseg is a row
    :param pcseg: The pcseg
    :return: Whether or not the pcseg is a row
    """
    if len(pcseg) != 12:
        return False
    pcset = set([pc.pc for pc in pcseg])
    if len(pcset) < 12:
        return False
    return True


def is_valid_rgen(rgen: list):
    """
    Determines if a row generator is valid
    :param rgen: A row generator
    :return: True if the row generator is valid; false otherwise
    """
    for i in range(len(list) - 1):
        rgen_sum = rgen[i]
        for j in range(i + 1, len(list)):
            rgen_sum += rgen[j]
            if rgen_sum % 12 == 0:
                return False
    return True


def make_pcseg(*args):
    """
    Makes a pcseg
    :param *args: Pcs
    :return: A pcseg
    """
    return [pitch.PitchClass12(pc) for pc in args]


def multiply(pcseg: list, n: int):
    """
    Multiplies a pcseg
    :param pcseg: The pcseg
    :param n: The multiplier
    :return: The multiplied pcseg
    """
    pcseg2 = []
    for pc in pcseg:
        pcseg2.append(pitch.PitchClass12(pc.pc * n))
    return pcseg2


def multiply_order(pcseg: list, n: int):
    """
    Multiplies a pcseg's order
    :param pcseg: The pcseg
    :param n: The multiplier
    :return: The order-multiplied pcseg
    """
    pcseg2 = []
    for i in range(len(pcseg)):
        pcseg2.append(pitch.PitchClass12(pcseg[(i * n) % len(pcseg)].pc))
    return pcseg2


def ormap(row: list, ormap: dict):
    """
    Performs the ORMAP mapping on a row, given a provided ORMAP
    :param row: A row
    :param ormap:
    :return: The ORMAP mapping for the row
    """
    mapping = []
    for item in row:
        mapping.append(ormap[item])
    return mapping


def prot(pcseg: list):
    """
    Generates the protocol pairs for a pcseg
    :param pcseg: A pcseg
    :return: A set of protocol pairs
    """
    pp = set()
    for i in range(len(pcseg)):
        for j in range(i, len(pcseg)):
            pp.add((pcseg[i], pcseg[j]))
    return pp


def retrograde(pcseg: list):
    """
    Retrogrades a pcseg
    :param pcseg: The pcseg
    :return: The retrograded pcseg
    """
    pcseg2 = []
    for i in range(len(pcseg) - 1, -1, -1):
        pcseg2.append(pitch.PitchClass12(pcseg[i].pc))
    return pcseg2


def rotate(pcseg: list, n: int):
    """
    Rotates a pcseg
    :param pcseg: The pcseg
    :param n: The index of rotation
    :return: The rotated pcseg
    """
    pcseg2 = []
    for i in range(len(pcseg)):
        pcseg2.append(pitch.PitchClass12(pcseg[(i - n) % len(pcseg)].pc))
    return pcseg2


def transpose(pcseg: list, n: int):
    """
    Transposes a pcseg
    :param pcseg: The pcseg
    :param n: The index of transposition
    :return: The transposed pcseg
    """
    pcseg2 = []
    for pc in pcseg:
        pcseg2.append(pitch.PitchClass12(pc.pc + n))
    return pcseg2


class InvarianceMatrix:
    """
    Represents an invariance matrix
    """
    def __init__(self, mx_type="T", a=None, c=None):
        """
        Creates an invariance matrix
        :param mx_type: The matrix type (T, I, M, or MI)
        :param a: Pcseg A
        :param c: Pcseg B
        """
        self._a = None
        self._b = None
        self._c = None
        self._mx_type = mx_type.upper()
        self._mx = []
        if a is not None and c is not None:
            self.load_matrix(a, c)

    def __repr__(self):
        """
        Gets a representation of the InvarianceMatrix object
        :returns: A string representation of the InvarianceMatrix object
        """
        return "<pctheory.pcseg.InvarianceMatrix object at " + str(id(self)) + ">: " + str(self._mx)

    def __str__(self):
        """
        Converts the InvarianceMatrix object to string
        :returns: A string conversion of the InvarianceMatrix object
        """
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']
        lines = "    "
        for pc in self._a:
            lines += chars[pc.pc] + " "
        lines += "\n   "
        for i in range(2 * len(self._a)):
            lines += "-"
        lines += "\n"
        for i in range(len(self._mx) - 1):
            lines += chars[self._b[i].pc] + " | "
            for j in range(len(self._mx[i])):
                lines += chars[self._mx[i][j].pc] + " "
            lines += "\n"
        lines += chars[self._b[len(self._mx) - 1].pc] + " | "
        for j in range(len(self._mx[len(self._mx) - 1])):
            lines += chars[self._mx[len(self._mx) - 1][j].pc] + " "
        return lines

    @property
    def mx(self):
        """
        Gets the invariance matrix
        :return: The invariance matrix
        """
        return self._mx

    @property
    def pcseg_a(self):
        """
        Gets the pcseg A
        :return: The pcseg A
        """
        return self._a

    @property
    def pcseg_b(self):
        """
        Gets the pcseg B
        :return: The pcseg B
        """
        return self._b

    @property
    def pcseg_c(self):
        """
        Gets the pcseg C
        :return: The pcseg C
        """
        return self._c

    def at(self, i, j):
        """
        Gets the pc at the specified row and column
        :param i: The row
        :param j: The column
        :return: The pc
        """
        return self._mx[i][j]

    def get_column(self, j):
        """
        Gets a column of the matrix
        :param j: The column index
        :return: The column
        """
        pcseg = []
        for i in range(len(self._mx)):
            pcseg.append(pitch.PitchClass12(self._mx[i][j].pc))
        return pcseg

    def get_row(self, i):
        """
        Gets a row of the matrix
        :param i: The row index
        :return: The row
        """
        return self._mx[i].copy()

    def load_matrix(self, a: list, c: list):
        """
        Loads the matrix
        :param a: Pcseg A
        :param c: Pcseg C
        :return: None
        """
        ro = transformations.RO()
        if self._mx_type == "T":
            ro.ro = [0, 0, 11]
        elif self._mx_type == "I":
            ro.ro = [0, 0, 1]
        elif self._mx_type == "M":
            ro.ro = [0, 0, 7]
        elif self._mx_type == "MI":
            ro.ro = [0, 0, 5]
        b = ro.transform(c)
        for i in range(len(c)):
            mx_row = []
            for j in range(len(a)):
                mx_row.append(pitch.PitchClass12(b[i].pc + a[j].pc))
            self._mx.append(mx_row)
        self._a = a.copy()
        self._b = b
        self._c = c.copy()

    def print(self, include: list = None):
        """
        Prints the invariance matrix
        :param include: The pcs to include (if None, all pcs will be printed)
        :returns: None
        """
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']
        lines = "    "
        for pc in self._a:
            lines += chars[pc.pc] + " "
        lines += "\n   "
        for i in range(2 * len(self._a)):
            lines += "-"
        lines += "\n"
        if include is None:
            for i in range(len(self._mx) - 1):
                lines += chars[self._b[i].pc] + " | "
                for j in range(len(self._mx[i])):
                    lines += chars[self._mx[i][j].pc] + " "
                lines += "\n"
            lines += chars[self._b[len(self._mx) - 1].pc] + " | "
            for j in range(len(self._mx[len(self._mx) - 1])):
                lines += chars[self._mx[len(self._mx) - 1][j].pc] + " "
        else:
            for i in range(len(self._mx) - 1):
                lines += chars[self._b[i].pc] + " | "
                for j in range(len(self._mx[i])):
                    if self._mx[i][j] in include:
                        lines += chars[self._mx[i][j].pc] + " "
                    else:
                        lines += "  "
                lines += "\n"
            lines += chars[self._b[len(self._mx) - 1].pc] + " | "
            for j in range(len(self._mx[len(self._mx) - 1])):
                if self._mx[len(self._mx) - 1][j] in include:
                    lines += chars[self._mx[len(self._mx) - 1][j].pc] + " "
                else:
                    lines += "  "
        print(lines)


class RotationalArray:
    """
    Represents a rotational array
    """
    def __init__(self, pcseg=None):
        """
        Creates a rotational array
        :param pcseg: A pcseg to import
        """
        self._array = []
        self._pcseg = None
        if pcseg is not None:
            self.import_pcseg(pcseg)

    def __repr__(self):
        return "<pctheory.pcseg.RotationalArray object at " + str(id(self)) + ">: " + str(self._array)

    def __str__(self):
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']
        lines = ""
        for i in range(len(self._array) - 1):
            for j in range(len(self._array[i])):
                lines += chars[self._array[i][j].pc] + " "
            lines += "\n"
        for j in range(len(self._array[len(self._array) - 1])):
            lines += chars[self._array[len(self._array) - 1][j].pc] + " "
        return lines

    @property
    def array(self):
        """
        Gets the rotational array
        :return: The rotational array
        """
        return self._array

    @property
    def pcseg(self):
        """
        Gets the pcseg
        :return: The pcseg
        """
        return self._pcseg

    def at(self, i, j):
        """
        Gets the pc at the specified row and column
        :param i: The row
        :param j: The column
        :return: The pc
        """
        return self._array[i][j]

    def get_column(self, j):
        """
        Gets a column of the rotational array
        :param j: The column index
        :return: The column
        """
        pcseg = []
        for i in range(len(self._array)):
            pcseg.append(pitch.PitchClass12(self._array[i][j].pc))
        return pcseg

    def get_row(self, i):
        """
        Gets a row of the rotational array
        :param i: The row index
        :return: The row
        """
        return self._array[i].copy()

    def import_pcseg(self, pcseg: list):
        """
        Imports a pcseg
        :param pcseg: A pcseg
        :return: None
        """
        self._pcseg = transpose(pcseg, 12 - pcseg[0].pc)
        self._array.clear()
        for i in range(len(self._pcseg)):
            self._array.append(rotate(transpose(self._pcseg, -self._pcseg[i].pc), len(self._pcseg) - i))


class TwelveToneMatrix:
    """
    Represents a twelve-tone matrix
    """
    def __init__(self, row=None):
        """
        Creates a twelve-tone matrix
        :param row: A row to import
        """
        self._labels_left = []
        self._labels_right = []
        self._labels_top = []
        self._labels_bottom = []
        self._mx = []
        self._row = None
        if row is not None:
            self.import_row(row)

    def __str__(self):
        """
        Generates a string representation of the TwelveToneMatrix that can be printed
        :return: A string representation of the TwelveToneMatrix
        """
        lines = "     "
        for i in range(12):
            lines += f"{self._labels_top[i]: <5} "
        lines += "\n"
        for i in range(12):
            lines += f"{self._labels_left[i]: <4}"
            for j in range(12):
                lines += f"  {str(self._mx[i][j])}   "
            lines += f"{self._labels_right[i]: >4}"
            lines += "\n"
        lines += "     "
        for i in range(12):
            lines += f"{self._labels_bottom[i]: <5} "
        return lines

    @property
    def labels_bottom(self):
        """
        Gets the bottom matrix labels
        :return: The bottom matrix labels
        """
        return self._labels_bottom

    @property
    def labels_left(self):
        """
        Gets the left matrix labels
        :return: The left matrix labels
        """
        return self._labels_left

    @property
    def labels_right(self):
        """
        Gets the right matrix labels
        :return: The right matrix labels
        """
        return self._labels_right

    @property
    def labels_top(self):
        """
        Gets the top matrix labels
        :return: The top matrix labels
        """
        return self._labels_top

    @property
    def matrix(self):
        """
        Gets the matrix
        :return: The matrix
        """
        return self._mx

    @property
    def row(self):
        """
        Gets the row
        :return: The row
        """
        return self._row

    def at(self, i, j):
        """
        Gets the pc at the specified row and column
        :param i: The row
        :param j: The column
        :return: The pc
        """
        return self._mx[i][j]

    def get_column(self, j):
        """
        Gets a column of the matrix
        :param j: The column index
        :return: The column
        """
        pcseg = []
        for i in range(len(self._mx)):
            pcseg.append(pitch.PitchClass12(self._mx[i][j].pc))
        return pcseg

    def get_row(self, i):
        """
        Gets a row of the matrix
        :param i: The row index
        :return: The row
        """
        return self._mx[i].copy()

    def import_row(self, row: list):
        """
        Imports a row
        :param row: The row to import
        :return:
        """
        # We need the starting pitch to be 0 for the P0 form
        self._row = transpose(row, -row[0].pc)
        inv = invert(self._row)

        for i in range(len(self._row)):
            self._mx.append(transpose(self._row, inv[i].pc))

        for i in range(len(self._row)):
            p_lbl = self._mx[i][0] - self._mx[0][0]
            i_lbl = self._mx[0][i] - self._mx[0][0]
            r_lbl = self._mx[i][len(self._row) - 1] - self._mx[0][len(self._row) - 1]
            ri_lbl = self._mx[len(self._row) - 1][i] - self._mx[len(self._row) - 1][0]
            self._labels_bottom.append(f"T{ri_lbl.pc}RI")
            self._labels_left.append(f"T{p_lbl.pc}")
            self._labels_right.append(f"T{r_lbl.pc}R")
            self._labels_top.append(f"T{i_lbl.pc}I")
