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


name_tables = tables.create_tables_row()


def are_combinatorial2(row1: list, row2: list):
    """
    Determines if two rows are hexachordally combinatorial
    :param row1: A row
    :param row2: A row
    :return: True or False
    """
    s1 = set(row1[:6] + row2[:6])
    s2 = set(row1[6:] + row2[6:])
    if len(s1) == len(s2) == 12:
        return True
    else:
        return False


def are_combinatorial3(row1: list, row2: list, row3: list):
    """
    Determines if three rows are tetrachordally combinatorial
    :param row1: A row
    :param row2: A row
    :param row3: A row
    :return: True or False
    """
    s1 = set(row1[:4] + row2[:4] + row3[:4])
    s2 = set(row1[4:8] + row2[4:8] + row3[4:8])
    s3 = set(row1[8:] + row2[8:] + row3[8:])
    if len(s1) == len(s2) == len(s3) == 12:
        return True
    else:
        return False


def are_combinatorial4(row1: list, row2: list, row3: list, row4: list):
    """
    Determines if four rows are trichordally combinatorial
    :param row1: A row
    :param row2: A row
    :param row3: A row
    :param row4: A row
    :return: True or False
    """
    s1 = set(row1[:3] + row2[:3] + row3[:3] + row4[:3])
    s2 = set(row1[3:6] + row2[3:6] + row3[3:6] + row4[3:6])
    s3 = set(row1[6:9] + row2[6:9] + row3[6:9] + row4[6:9])
    s4 = set(row1[9:] + row2[9:] + row3[9:] + row4[9:])
    if len(s1) == len(s2) == len(s3) == len(s4) == 12:
        return True
    else:
        return False


def bip_n(imb: list):
    """
    Gets the BIP_n of a list of set-classes generated by IMB_n
    :param imb: The IMB_n list
    :return: The BIP_n
    """
    bip = []
    if len(imb) > 0:
        for sc in imb:
            name = sc.name_forte.split('-')[1]
            name = name.replace("Z", "")
            bip.append(int(name))
        bip.sort()
    return bip


def create_ormap(pcseg: list):
    """
    Creates the ORMAP of a row
    :param pcseg: A row
    :return: The ORMAP
    """
    omap = {}
    t = type(pcseg[0])
    for i in range(len(pcseg)):
        omap[t(pcseg[i].pc)] = i
    return omap


def find_otos(pcseg1: list, pcseg2: list):
    """
    Gets all OTO transformations of pcseg1 that contain pcseg2
    :param pcseg1: A pcseg
    :param pcseg2: A pcseg
    :return: A set of OTOs that transform pcseg1 so that it contains pcseg2.
    """
    otos = transformations.get_otos12()
    oto_set = set()

    for oto in otos:
        pcseg3 = otos[oto].transform(pcseg1)
        # Search each transformation in t
        done_searching = False
        for i in range(len(pcseg3)):
            if len(pcseg2) > len(pcseg3) - i:
                break
            done_searching = True
            for j in range(i, i + len(pcseg2)):
                if pcseg3[j] != pcseg2[j - i]:
                    done_searching = False
                    break
            if done_searching:
                oto_set.add(otos[oto])
                break

    return oto_set


def generate_pcseg12_from_interval_list(interval_list: list, starting_pc=None):
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


def generate_pcseg24_from_interval_list(interval_list: list, starting_pc=None):
    """
    Generates a pcseg from an interval list
    :param interval_list: The interval list
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: A pcseg
    """
    if starting_pc is None:
        random.seed()
        pcseg = [pitch.PitchClass24(random.randrange(24))]
        for i in range(len(interval_list)):
            pcseg.append(pitch.PitchClass24(pcseg[i].pc + interval_list[i]))
        return pcseg
    else:
        pcseg = [pitch.PitchClass24(starting_pc)]
        for i in range(len(interval_list)):
            pcseg.append(pitch.PitchClass24(pcseg[i].pc + interval_list[i]))
        return pcseg


def generate_random_all_interval_row(starting_pc=None):
    """
    Generates a random all-interval row
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: An all-interval row
    """
    global name_tables
    random.seed()
    row = []

    # Establish the starting pitch of the row
    if starting_pc is not None:
        if type(starting_pc) == pitch.PitchClass12:
            row.append(pitch.PitchClass12(starting_pc.pc))
        else:
            row.append(pitch.PitchClass12(starting_pc))
    else:
        row.append(pitch.PitchClass12(random.randrange(12)))
    generator = name_tables["elevenIntervalRowGenerators"][random.randrange(
        len(name_tables["elevenIntervalRowGenerators"]))]

    # Randomly choose to invert the row generator
    if random.randrange(1) == 1:
        generator = [i * 11 % 12 for i in generator]

    # Build the row
    for i in range(1, 12):
        row.append(pitch.PitchClass12(row[i - 1].pc + generator[i - 1]))
    return row


def generate_random_pcseg12(length: int, non_duplicative=False, starting_pc=None):
    """
    Generates a random pcseg
    :param length: The length of the pcseg
    :param non_duplicative: Whether or not duplicate pcs may occur (must be True to generate a row)
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: A random pcseg
    """
    random.seed()
    pcseg = [pitch.PitchClass12(random.randrange(12) if starting_pc is None else starting_pc)]
    if non_duplicative and 0 < length <= 12:
        pcs = [i for i in range(12)]
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


def generate_random_pcseg24(length: int, non_duplicative=False, starting_pc=None):
    """
    Generates a random pcseg
    :param length: The length of the pcseg
    :param non_duplicative: Whether or not duplicate pcs may occur (must be True to generate a row)
    :param starting_pc: The starting pitch-class. If None, a random starting pitch-class is used.
    :return: A random pcseg
    """
    random.seed()
    pcseg = [pitch.PitchClass24(random.randrange(24) if starting_pc is None else starting_pc)]
    if non_duplicative and 0 < length <= 24:
        pcs = [i for i in range(24)]
        del pcs[pcseg[0].pc]
        for i in range(length - 1):
            j = random.randrange(len(pcs))
            pcseg.append(pitch.PitchClass24(pcs[j]))
            del pcs[j]
    elif not non_duplicative and 0 < length:
        for i in range(length - 1):
            pcseg.append(pitch.PitchClass24(random.randrange(24)))
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
    t = type(setseg[0])
    for i in range(len(setseg)):
        j = random.randrange(len(setseg))
        pcseg.append(t(setseg[j].pc))
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


def invert(pcseg: list):
    """
    Inverts a pcseg
    :param pcseg: The pcseg
    :return: The inverted pcseg
    """
    pcseg2 = []
    if len(pcseg) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcseg)))
        for pc in pcseg:
            pcseg2.append(t(pc.pc * -1))
    return pcseg2


def imb_n(pcseg: list, n: int):
    """
    Gets the IMB_n of a pcseg. The IMB_n is the segment of imbricated set-classes of cardinality n.
    :param pcseg: The pcseg
    :param n: The cardinality of imbrication
    :return: The IMB_n
    """
    imb = set()
    scs = []
    if type(pcseg[0]) == pitch.PitchClass12:
        for i in range(len(pcseg) + 1 - n):
            for j in range(i, i + n):
                imb.add(pcseg[j])
            scs.append(pcset.SetClass12(imb))
            imb.clear()
    elif type(pcseg[0]) == pitch.PitchClass24:
        for i in range(len(pcseg) + 1 - n):
            for j in range(i, i + n):
                imb.add(pcseg[j])
            scs.append(pcset.SetClass24(imb))
            imb.clear()
    return scs


def is_all_interval_row(pcseg: list):
    """
    Determines if a pcseg is an all-interval row
    :param pcseg: The pcseg
    :return: Whether or not the pcseg is an all-interval row
    """
    pcs = set([pc.pc for pc in pcseg])
    if type(pcseg[0]) == pitch.PitchClass12:
        if len(pcs) != 12 or len(pcs) != len(pcseg):
            return False
        else:
            ints = {(pcseg[i].pc - pcseg[i-1].pc) % 12 for i in range(1, len(pcseg))}
            if len(ints) == 11:
                return True
    elif type(pcseg[0]) == pitch.PitchClass24:
        if len(pcs) != 24 or len(pcs) != len(pcseg):
            return False
        else:
            ints = {(pcseg[i].pc - pcseg[i-1].pc) % 24 for i in range(1, len(pcseg))}
            if len(ints) == 23:
                return True
    return False


def is_link_chord(pcseg: list):
    """
    Determines if a row is a Link chord (an all-interval row containing the all-trichord hexachord as a subset)
    :param pcseg: A pcset
    :return: True or False
    """
    if is_all_interval_row(pcseg):
        imb = imb_n(pcseg, 6)
        for sc in imb:
            if sc.name_forte == "6-Z17":
                return True
    return False


def is_row(pcseg: list):
    """
    Determines if a pcseg is a row
    :param pcseg: The pcseg
    :return: Whether or not the pcseg is a row
    """
    pcs = set([pc.pc for pc in pcseg])
    if type(pcseg[0]) == pitch.PitchClass12:
        if len(pcs) != 12 or len(pcs) != len(pcseg):
            return False
        else:
            return True
    elif type(pcseg[0]) == pitch.PitchClass24:
        if len(pcs) != 24 or len(pcs) != len(pcseg):
            return False
        else:
            return True
    return False


def is_row_generator(rgen: list):
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


def make_pcseg12(*args):
    """
    Makes a pcseg
    :param args: Pcs
    :return: A pcseg
    """
    if type(args[0]) == list:
        args = args[0]
    return [pitch.PitchClass12(pc) for pc in args]


def make_pcseg24(*args):
    """
    Makes a pcseg
    :param args: Pcs
    :return: A pcseg
    """
    if type(args[0]) == list:
        args = args[0]
    return [pitch.PitchClass24(pc) for pc in args]


def multiply(pcseg: list, n: int):
    """
    Multiplies a pcseg
    :param pcseg: The pcseg
    :param n: The multiplier
    :return: The multiplied pcseg
    """
    pcseg2 = []
    if len(pcseg) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcseg)))
        for pc in pcseg:
            pcseg2.append(t(pc.pc * n))
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
    if len(pcseg) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcseg)))
        for i in range(len(pcseg) - 1, -1, -1):
            pcseg2.append(t(pcseg[i].pc))
    return pcseg2


def rotate(pcseg: list, n: int):
    """
    Rotates a pcseg
    :param pcseg: The pcseg
    :param n: The index of rotation
    :return: The rotated pcseg
    """
    pcseg2 = []
    if len(pcseg) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcseg)))
        for i in range(len(pcseg)):
            pcseg2.append(t(pcseg[(i - n) % len(pcseg)].pc))
    return pcseg2


def transpose(pcseg: list, n: int):
    """
    Transposes a pcseg
    :param pcseg: The pcseg
    :param n: The index of transposition
    :return: The transposed pcseg
    """
    pcseg2 = []
    if len(pcseg) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcseg)))
        for pc in pcseg:
            pcseg2.append(t(pc.pc + n))
    return pcseg2


def transpositional_combination(pcseg1: list, pcseg2: list):
    """
    Transpositionally combines (TC) two pcsegs. This is Boulez's "multiplication."
    :param pcseg1: A pcseg
    :param pcseg2: A pcseg
    :return: The TC pcset
    """
    pcseg3 = []
    if len(pcseg1) > 0 and len(pcseg2) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcseg1)))
        for pc2 in pcseg2:
            for pc1 in pcseg1:
                pcseg3.append(t(pc1.pc + pc2.pc))
    return pcseg3


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
        self._mx = None
        self._t = None
        if a is not None and c is not None:
            self.load_matrix(a, c)

    def __getitem__(self, i, j):
        """
        Gets the pc at the specified row and column
        :param i: The row
        :param j: The column
        :return: The pc
        """
        return self._mx[i][j]

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

    def get_column(self, j):
        """
        Gets a column of the matrix
        :param j: The column index
        :return: The column
        """
        c = []
        for i in range(len(self._mx)):
            c.append(self._mx[i][j])
        return c

    def get_row(self, i):
        """
        Gets a row of the matrix
        :param i: The row index
        :return: The row
        """
        return self._mx[i]

    def load_matrix(self, a: list, c: list):
        """
        Loads the matrix
        :param a: Pcseg A
        :param c: Pcseg C
        :return: None
        """
        self._t = type(a[0])
        ro = transformations.OTO()
        if self._t == pitch.PitchClass12:
            INVERT = 11
            if self._mx_type == "T":
                ro.oto = [0, 0, 1 * INVERT % 12]
            elif self._mx_type == "M" or self._mx_type == "M5":
                ro.oto = [0, 0, 5 * INVERT % 12]
            elif self._mx_type == "MI" or self._mx_type == "M7":
                ro.oto = [0, 0, 7 * INVERT % 12]
            elif self._mx_type == "I" or self._mx_type == "M11":
                ro.oto = [0, 0, 11 * INVERT % 12]
            b = ro.transform(c)
        if self._t == pitch.PitchClass24:
            INVERT = 23
            if self._mx_type == "T":
                ro.oto = [0, 0, 1 * INVERT % 24]
            elif self._mx_type == "M5":
                ro.oto = [0, 0, 5 * INVERT % 24]
            elif self._mx_type == "M7":
                ro.oto = [0, 0, 7 * INVERT % 24]
            elif self._mx_type == "M11":
                ro.oto = [0, 0, 11 * INVERT % 24]
            elif self._mx_type == "M13":
                ro.oto = [0, 0, 13 * INVERT % 24]
            elif self._mx_type == "M17":
                ro.oto = [0, 0, 17 * INVERT % 24]
            elif self._mx_type == "M19":
                ro.oto = [0, 0, 19 * INVERT % 24]
            elif self._mx_type == "I" or self._mx_type == "M23":
                ro.oto = [0, 0, 23 * INVERT % 24]
            b = ro.transform(c)
        self._mx = []
        for i in range(len(b)):
            mxrow = []
            for j in range(len(a)):
                mxrow.append(self._t(b[i].pc + a[j].pc))
            self._mx.append(mxrow)
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

    def __getitem__(self, i, j):
        """
        Gets the pc at the specified row and column
        :param i: The row
        :param j: The column
        :return: The pc
        """
        return self._mx[i][j]

    def __repr__(self):
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
