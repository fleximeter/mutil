"""
File: pcset.py
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

import networkx
import pyvis
import multiprocessing as mp

from pctheory import pitch, tables, transformations


class SetClass12:
    """
    Represents a pc-set-class
    """

    def __init__(self, name_tables=None, pcset=None):
        """
        Creates a SetClass
        :param name_tables: A list of name tables
        :param pcset: A pcset to initialize the SetClass
        """
        self._ic_vector = [0, 0, 0, 0, 0, 0, 0]
        self._name_carter = ""
        self._name_forte = ""
        self._name_morris = ""
        self._name_prime = ""
        self._num_forte = 0
        self._pcset = set()
        self._weight_right = True
        self._tables = name_tables if name_tables is not None else tables.create_tables_set()
        if pcset is not None:
            self.pcset = pcset

    def __eq__(self, other):
        return self.pcset == other.pcset

    def __hash__(self):
        return len(self) * 100 + self.num_forte

    def __len__(self):
        return len(self._pcset)

    def __lt__(self, other):
        if len(self) < len(other) or (len(self) == len(other) and self.num_forte < other.num_forte):
            return True
        return False

    def __ne__(self, other):
        return self.pcset != other.pcset

    def __repr__(self):
        # return "<pctheory.pcset.SetClass12 object at " + str(id(self)) + ">: " + repr(self._pcset)
        return self._name_morris

    def __str__(self):
        return str([str(pc) for pc in self._pcset])

    @property
    def derived_core(self):
        """
        Gets derived core associations
        :return: The derived core associations (or None if not derived core)
        """
        if self.name_prime in self._tables["carterDerivedCoreTable"]:
            return [name for name in self._tables["carterDerivedCoreTable"][self.name_prime]]
        else:
            return None

    @property
    def ic_vector(self):
        """
        Gets the IC vector
        :return: The IC vector
        """
        return self._ic_vector

    @property
    def ic_vector_string(self):
        """
        Gets the IC vector
        :return: The IC vector
        """
        s = "["
        for a in self._ic_vector:
            s += str(a)
        s += "]"
        return s

    @property
    def is_z_relation(self):
        """
        Whether or not this set-class is Z-related to another set-class
        :return: A boolean
        """
        if "Z" in self.name_forte:
            return True
        return False

    @property
    def name_carter(self):
        """
        Generates the Carter name for a set-class
        :return: The Carter name
        """
        return self._name_carter

    @property
    def name_forte(self):
        """
        Generates the Forte name for a set-class
        :return: The Forte name
        """
        return self._name_forte

    @property
    def name_morris(self):
        """
        Generates the Morris name for a set-class
        :return: The Morris name
        """
        return self._name_morris

    @property
    def name_prime(self):
        """
        Generates the prime-form name (Rahn) for a set-class
        :return: The prime-form name
        """
        return self._name_prime

    @property
    def num_forte(self):
        """
        Generates the number part of the Forte name
        :return: The number part of the Forte name
        """
        return self._num_forte

    @property
    def pcset(self):
        """
        Gets the pcset prime form
        :return: The pcset prime form
        """
        return self._pcset

    @pcset.setter
    def pcset(self, value):
        """
        Updates the pcset prime form
        :param value: The new pcset
        :return:
        """
        self._pcset = SetClass12.calculate_prime_form(value, self._weight_right)
        self._make_names()

    @property
    def weight_right(self):
        """
        Whether or not to weight from the right
        :return: A Boolean
        """
        return self._weight_right

    @weight_right.setter
    def weight_right(self, value: bool):
        """
        Whether or not to weight from the right
        :param value: A Boolean
        :return:
        """
        self._weight_right = value
        self._pcset = SetClass12.calculate_prime_form(self._pcset, self._weight_right)

    @staticmethod
    def calculate_prime_form(pcset: set, weight_from_right: bool = True):
        """
        Calculates the prime form of a pcset
        :param pcset: The pcset
        :param weight_from_right: Whether or not to pack from the right
        :return: The prime form
        """
        prime_set = set()
        if len(pcset) > 0:
            lists_to_weight = []
            int_set = SetClass12._make_int_set(pcset)
            pclist = list(int_set)
            inverted = list(SetClass12._make_int_set(set(SetClass12._invert(pclist))))
            prime_list = None

            # Add regular forms
            for i in range(len(pclist)):
                lists_to_weight.append([])
                for i2 in range(i, len(pclist)):
                    lists_to_weight[i].append(pclist[i2])
                for i2 in range(0, i):
                    lists_to_weight[i].append(pclist[i2])
                initial_pitch = lists_to_weight[i][0]
                for i2 in range(0, len(lists_to_weight[i])):
                    lists_to_weight[i][i2] -= initial_pitch
                    if lists_to_weight[i][i2] < 0:
                        lists_to_weight[i][i2] += 12
                lists_to_weight[i].sort()

            # Add inverted forms
            for i in range(len(pclist)):
                lists_to_weight.append([])
                for i2 in range(i, len(pclist)):
                    lists_to_weight[i + len(pclist)].append(inverted[i2])
                for i2 in range(0, i):
                    lists_to_weight[i + len(pclist)].append(inverted[i2])
                initial_pitch = lists_to_weight[i + len(pclist)][0]
                for i2 in range(0, len(lists_to_weight[i])):
                    lists_to_weight[i + len(pclist)][i2] -= initial_pitch
                    if lists_to_weight[i + len(pclist)][i2] < 0:
                        lists_to_weight[i + len(pclist)][i2] += 12
                lists_to_weight[i + len(pclist)].sort()

            # Weight lists
            if weight_from_right:
                prime_list = SetClass12._weight_from_right(lists_to_weight)
            else:
                prime_list = SetClass12._weight_left(lists_to_weight)

            # Create pcset
            for pc in prime_list:
                prime_set.add(pitch.PitchClass12(pc))

        return prime_set

    def contains_abstract_subset(self, sc):
        """
        Determines if a set-class is an abstract subset of this set-class
        :param sc: A set-class
        :return: A boolean
        """
        tr = []
        inv = invert(sc.pcset)
        for i in range(12):
            tr.append(transpose(sc.pcset, i))
            tr.append(transpose(inv, i))
        for pcs in tr:
            if pcs.issubset(self.pcset):
                return True
        return False

    def get_abstract_complement(self):
        """
        Gets the abstract complement of the SetClass
        :return: The abstract complement SetClass
        """
        csc = SetClass12(self._tables)
        csc.pcset = get_complement(self._pcset)
        return csc

    def get_invariance_vector(self):
        """
        Gets the invariance vector of the SetClass
        :return: The invariance vector
        """
        iv = [0, 0, 0, 0, 0, 0, 0, 0]
        c = get_complement(self._pcset)
        ttos = transformations.get_ttos12()
        for i in range(12):
            h = [ttos[f"T{i}"].transform(self._pcset), ttos[f"T{i}I"].transform(self._pcset),
                 ttos[f"T{i}M"].transform(self._pcset), ttos[f"T{i}MI"].transform(self._pcset)]
            for j in range(4):
                if h[j] == self._pcset:
                    iv[j] += 1
                if h[j].issubset(c):
                    iv[4 + j] += 1
        return iv

    def get_subset_classes(self):
        """
        Gets a set of subset-classes contained in this SetClass
        :return:
        """
        sub = subsets(self._pcset)
        subset_classes = set()
        for s in sub:
            subset_classes.add(SetClass12(self._tables, s))
        return subset_classes

    def get_partition2_subset_classes(self):
        """
        Gets a set of set-class partitions of this SetClass
        :return:
        """
        p = partitions2(self._pcset)
        p_set = set()
        for part in p:
            p_set.add((SetClass12(self._tables, part[0]), SetClass12(self._tables, part[1])))
        return p_set

    def get_z_relation(self):
        """
        Gets the Z-relation of the SetClass
        :return: The Z-relation of the SetClass
        """
        zset = SetClass12(self._tables)
        f = self.name_forte
        if "Z" in f:
            zset.load_from_name(self._tables["zNameTable"][f])
        return zset

    def is_valid_name(self, name: str):
        """
        Determines if a set-class name is valid. Validates prime form, Forte, and Morris names.
        Prime form name format: [xxxx]
        Forte name format: x-x
        Morris name format: (x-x)[xxxx]
        :param name: The name
        :return: A boolean
        """
        if "[" in name and "-" in name:
            name = name.split(")")
            name.split[0] = name.split[0].replace("(", "")
            if name[0] in self._tables["forteToSetNameTable"] and name[1] in self._tables["setToForteNameTable"]:
                return True
        elif "-" in name:
            if name in self._tables["forteToSetNameTable"]:
                return True
        elif name in self._tables["setToForteNameTable"] or name in self._tables["setToForteNameTableLeftPacking"]:
            return True
        return False

    def load_from_name(self, name: str):
        """
        Loads a set-class from a prime-form, Morris, or Forte name
        :param name: The name
        :return:
        """
        pname = ""
        if "[" in name and "-" in name:
            pname = name.split("[")[1]
        elif "-" in name:
            if name in self._tables["forteToSetNameTable"]:
                pname = self._tables["forteToSetNameTable"][name]
        elif name in self._tables["setToForteNameTable"]:
            pname = name
        pname = pname.replace("[", "")
        pname = pname.replace("]", "")
        pname = [c for c in pname]
        pcset = set([pitch.PitchClass12(self._tables["hexToInt"][pn]) for pn in pname])
        self.pcset = pcset

    @staticmethod
    def _invert(pcseg: list):
        """
        Inverts a pcseg
        :param pcset: The pcseg
        :return: The inverted pcseg
        """
        pcseg2 = []
        for pc in pcseg:
            pcseg2.append(pitch.PitchClass12((pc * 11) % 12))
        return pcseg2

    @staticmethod
    def _make_int_set(pcset: set):
        """
        Makes an int set
        :param pcset: A pcset
        :return: An int set
        """
        pcset2 = set()
        for pc in pcset:
            pcset2.add(pc.pc)
        return pcset2

    def _make_names(self):
        """
        Makes the names for the set-class
        :return:
        """
        pc_name_list = [self._tables["hexChars"][pc.pc] for pc in self._pcset]
        pc_name_list.sort()
        self._name_prime = "[" + "".join(pc_name_list) + "]"
        if self._name_prime != "[]":
            if self._name_prime in self._tables["setToForteNameTableLeftPacking"]:
                self._name_forte = self._tables["setToForteNameTableLeftPacking"][self._name_prime]
            else:
                self._name_forte = self._tables["setToForteNameTable"][self._name_prime]
        else:
            self._name_forte = "0-1"
        self._name_carter = ""
        if self._name_forte in self._tables["forteToCarterNameTable"]:
            self._name_carter = self._tables["forteToCarterNameTable"][self._name_forte]
        self._name_morris = "(" + self._name_forte + ")" + self._name_prime
        forte_num = self.name_forte.split('-')[1]
        forte_num = forte_num.strip('Z')
        self._num_forte = int(forte_num)
        self._ic_vector = [0, 0, 0, 0, 0, 0, 0]
        for pc in self._pcset:
            for pc2 in self._pcset:
                interval = (pc2.pc - pc.pc) % 12
                if interval < 0:
                    interval += 12
                if interval > 6:
                    interval = interval * -1 + 12
                self._ic_vector[interval] += 1
        for i in range(1, 7):
            self._ic_vector[i] //= 2

    @staticmethod
    def _weight_from_right(pclists: list):
        """
        Weights pclists from the right
        :param pclists: Pclists
        :return: The most weighted form
        """
        for i in range(len(pclists[0]) - 1, -1, -1):
            if len(pclists) > 1:
                # The smallest item at the current index
                smallest_item = 11

                # Identify the smallest item at the current index
                for j in range(len(pclists)):
                    if pclists[j][i] < smallest_item:
                        smallest_item = pclists[j][i]

                # Remove all lists with larger items at the current index
                j = 0
                while j < len(pclists):
                    if pclists[j][i] > smallest_item:
                        del pclists[j]
                    else:
                        j += 1

            else:
                break
        return pclists[0]

    @staticmethod
    def _weight_left(pclists: list):
        """
        Weights pclists left
        :param pclists: Pclists
        :return: The most weighted form
        """
        if len(pclists) > 1:
            # The smallest item at the current index
            smallest_item = 11

            # Identify the smallest item at the last index
            for j in range(0, len(pclists)):
                if pclists[j][len(pclists[0]) - 1] < smallest_item:
                    smallest_item = pclists[j][len(pclists[0]) - 1]

            # Remove all lists with larger items at the current index
            j = 0
            while j < len(pclists):
                if pclists[j][len(pclists[0]) - 1] > smallest_item:
                    del pclists[j]
                else:
                    j += 1

            # Continue processing, but now pack from the left
            for i in range(0, len(pclists[0])):
                if len(pclists) > 1:
                    smallest_item = 11

                    # Identify the smallest item at the current index
                    for j in range(len(pclists)):
                        if pclists[j][i] < smallest_item:
                            smallest_item = pclists[j][i]

                    # Remove all lists with larger items at the current index
                    j = 0
                    while j < len(pclists):
                        if pclists[j][i] > smallest_item:
                            del pclists[j]
                        else:
                            j += 1
                else:
                    break
        return pclists[0]


class SetClass24:
    """
    Represents a pc-set-class
    """

    def __init__(self, pcset=None):
        """
        Creates a SetClass
        :param pcset: A pcset to initialize the SetClass
        """
        self._ic_vector = [0 for i in range(13)]
        self._name_prime = ""
        self._pcset = set()
        self._weight_right = True
        if pcset is not None:
            self.pcset = pcset

    def __eq__(self, other):
        return self.pcset == other.pcset

    def __hash__(self):
        return hash(self.name_prime)

    def __len__(self):
        return len(self._pcset)

    def __lt__(self, other):
        if len(self) < len(other) or (len(self) == len(other) and self.name_prime < other.name_prime):
            return True
        return False

    def __ne__(self, other):
        return self.pcset != other.pcset

    def __repr__(self):
        return "<pctheory.pcset.SetClass24 object at " + str(id(self)) + ">: " + repr(self._pcset)

    def __str__(self):
        return self._name_prime

    @property
    def ic_vector(self):
        """
        Gets the IC vector
        :return: The IC vector
        """
        return self._ic_vector

    @property
    def ic_vector_string(self):
        """
        Gets the IC vector
        :return: The IC vector
        """
        s = "["
        for a in self._ic_vector:
            s += str(a)
        s += "]"
        return s

    @property
    def name_prime(self):
        """
        Generates the prime-form name (Rahn) for a set-class
        :return: The prime-form name
        """
        return self._name_prime

    @property
    def pcset(self):
        """
        Gets the pcset prime form
        :return: The pcset prime form
        """
        return self._pcset

    @pcset.setter
    def pcset(self, value):
        """
        Updates the pcset prime form
        :param value: The new pcset
        :return:
        """
        self._pcset = SetClass24.calculate_prime_form(value, self._weight_right)
        self._make_names()

    @property
    def weight_right(self):
        """
        Whether or not to weight from the right
        :return: A Boolean
        """
        return self._weight_right

    @weight_right.setter
    def weight_right(self, value: bool):
        """
        Whether or not to weight from the right
        :param value: A Boolean
        :return:
        """
        self._weight_right = value
        self._pcset = SetClass24.calculate_prime_form(self._pcset, self._weight_right)

    @staticmethod
    def calculate_prime_form(pcset: set, weight_from_right: bool = True):
        """
        Calculates the prime form of a pcset
        :param pcset: The pcset
        :param weight_from_right: Whether or not to pack from the right
        :return: The prime form
        """
        prime_set = set()
        if len(pcset) > 0:
            lists_to_weight = []
            int_set = SetClass24._make_int_set(pcset)
            pclist = list(int_set)
            inverted = list(SetClass24._make_int_set(set(SetClass24._invert(pclist))))
            prime_list = None

            # Add regular forms
            for i in range(len(pclist)):
                lists_to_weight.append([])
                for i2 in range(i, len(pclist)):
                    lists_to_weight[i].append(pclist[i2])
                for i2 in range(0, i):
                    lists_to_weight[i].append(pclist[i2])
                initial_pitch = lists_to_weight[i][0]
                for i2 in range(0, len(lists_to_weight[i])):
                    lists_to_weight[i][i2] -= initial_pitch
                    if lists_to_weight[i][i2] < 0:
                        lists_to_weight[i][i2] += 24
                lists_to_weight[i].sort()

            # Add inverted forms
            for i in range(len(pclist)):
                lists_to_weight.append([])
                for i2 in range(i, len(pclist)):
                    lists_to_weight[i + len(pclist)].append(inverted[i2])
                for i2 in range(0, i):
                    lists_to_weight[i + len(pclist)].append(inverted[i2])
                initial_pitch = lists_to_weight[i + len(pclist)][0]
                for i2 in range(0, len(lists_to_weight[i])):
                    lists_to_weight[i + len(pclist)][i2] -= initial_pitch
                    if lists_to_weight[i + len(pclist)][i2] < 0:
                        lists_to_weight[i + len(pclist)][i2] += 24
                lists_to_weight[i + len(pclist)].sort()

            # Weight lists
            if weight_from_right:
                prime_list = SetClass24._weight_from_right(lists_to_weight)
            else:
                prime_list = SetClass24._weight_left(lists_to_weight)

            # Create pcset
            for pc in prime_list:
                prime_set.add(pitch.PitchClass24(pc))

        return prime_set

    def contains_abstract_subset(self, sc):
        """
        Determines if a set-class is an abstract subset of this set-class
        :param sc: A set-class
        :return: A boolean
        """
        tr = []
        inv = invert(sc.pcset)
        for i in range(24):
            tr.append(transpose(sc.pcset, i))
            tr.append(transpose(inv, i))
        for pcs in tr:
            if pcs.issubset(self.pcset):
                return True
        return False

    def get_abstract_complement(self):
        """
        Gets the abstract complement of the SetClass
        :return: The abstract complement SetClass
        """
        csc = SetClass24()
        csc.pcset = get_complement(self._pcset)
        return csc

    def get_subset_classes(self):
        """
        Gets a set of subset-classes contained in this SetClass
        :return:
        """
        sub = subsets(self._pcset)
        sc = SetClass24()
        subset_classes = {}
        for s in sub:
            sc.pcset = s
            if sc.name_prime not in subset_classes:
                subset_classes[sc.name_prime] = SetClass24(s)
        subset_classes_set = set()
        for s in subset_classes:
            subset_classes_set.add(subset_classes[s])
        return subset_classes_set

    def get_partition_subset_classes(self):
        """
        Gets a set of set-class partitions of this SetClass
        :return:
        """
        p = partitions2(self._pcset)
        p_set = set()
        for part in p:
            p_set.add((SetClass24(part[0]), SetClass24(part[1])))
        return p_set

    @staticmethod
    def _invert(pcseg: list):
        """
        Inverts a pcseg
        :param pcset: The pcseg
        :return: The inverted pcseg
        """
        pcseg2 = []
        for pc in pcseg:
            pcseg2.append(pitch.PitchClass24((pc * 23) % 24))
        return pcseg2

    @staticmethod
    def _make_int_set(pcset: set):
        """
        Makes an int set
        :param pcset: A pcset
        :return: An int set
        """
        pcset2 = set()
        for pc in pcset:
            pcset2.add(pc.pc)
        return pcset2

    def _make_names(self):
        """
        Makes the names for the set-class
        :return:
        """
        pcseg = list(self._pcset)
        pcseg.sort()
        self._name_prime = str(pcseg)
        self._ic_vector = [0 for i in range(13)]
        for pc in self._pcset:
            for pc2 in self._pcset:
                interval = (pc2.pc - pc.pc) % 24
                if interval > 12:
                    interval = (interval * 11) % 12
                self._ic_vector[interval] += 1
        for i in range(1, 13):
            self._ic_vector[i] //= 2

    @staticmethod
    def _weight_from_right(pclists: list):
        """
        Weights pclists from the right
        :param pclists: Pclists
        :return: The most weighted form
        """
        for i in range(len(pclists[0]) - 1, -1, -1):
            if len(pclists) > 1:
                # The smallest item at the current index
                smallest_item = 23

                # Identify the smallest item at the current index
                for j in range(len(pclists)):
                    if pclists[j][i] < smallest_item:
                        smallest_item = pclists[j][i]

                # Remove all lists with larger items at the current index
                j = 0
                while j < len(pclists):
                    if pclists[j][i] > smallest_item:
                        del pclists[j]
                    else:
                        j += 1

            else:
                break
        return pclists[0]

    @staticmethod
    def _weight_left(pclists: list):
        """
        Weights pclists left
        :param pclists: Pclists
        :return: The most weighted form
        """
        if len(pclists) > 1:
            # The smallest item at the current index
            smallest_item = 11

            # Identify the smallest item at the last index
            for j in range(0, len(pclists)):
                if pclists[j][len(pclists[0]) - 1] < smallest_item:
                    smallest_item = pclists[j][len(pclists[0]) - 1]

            # Remove all lists with larger items at the current index
            j = 0
            while j < len(pclists):
                if pclists[j][len(pclists[0]) - 1] > smallest_item:
                    del pclists[j]
                else:
                    j += 1

            # Continue processing, but now pack from the left
            for i in range(0, len(pclists[0])):
                if len(pclists) > 1:
                    smallest_item = 11

                    # Identify the smallest item at the current index
                    for j in range(len(pclists)):
                        if pclists[j][i] < smallest_item:
                            smallest_item = pclists[j][i]

                    # Remove all lists with larger items at the current index
                    j = 0
                    while j < len(pclists):
                        if pclists[j][i] > smallest_item:
                            del pclists[j]
                        else:
                            j += 1
                else:
                    break
        return pclists[0]


def get_complement(pcset: set):
    """
    Gets the complement of a pcset
    :param pcset: A pcset
    :return: The complement pcset
    """
    universal = set()
    if len(pcset) > 0:
        t = type(next(iter(pcset)))
        if t == pitch.PitchClass12:
            for i in range(12):
                universal.add(pitch.PitchClass12(i))
        else:
            for i in range(24):
                universal.add(pitch.PitchClass24(i))
    return universal - pcset


def get_corpus(pcset: set):
    """
    Gets all transformations of a provided pcset
    :param pcset: A pcset
    :return: A set of all transformations of the pcset
    """
    tto = transformations.get_ttos12()
    pcsets = set()
    if len(pcset) > 0:
        n = 12
        t = type(next(iter(pcset)))
        if t == pitch.PitchClass24:
            n = 24
        for i in range(n):
            pcsets.add(frozenset(tto[f"T{i}"].transform(pcset)))
            pcsets.add(frozenset(tto[f"T{i}I"].transform(pcset)))
    return pcsets


def get_uto(original_pcset: set, transformed_pcset: set):
    """
    Finds all UTOs that produce a set that contains transformed_pcset as a proper or improper subset.
    If the list of UTOs is empty, transformed_pcset is not an abstract subset of original_pcset.
    :param original_pcset: The original pcset
    :param transformed_pcset: The new pcset
    :return: A list of UTOs
    """
    utos = None
    utos_final = {}
    if len(original_pcset) == len(transformed_pcset) == 0:
        return utos
    else:
        t = type(next(iter(original_pcset)))
        if t == pitch.PitchClass12:
            utos = transformations.get_utos12()
        else:
            utos = transformations.get_utos24()
        for u in utos:
            if transformed_pcset.issubset(utos[u].transform(original_pcset)):
                utos_final[u] = utos[u]
        return utos_final


def invert(pcset: set):
    """
    Inverts a pcset
    :param pcset: The pcset
    :return: The inverted pcset
    """
    pcset2 = set()
    if len(pcset) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcset)))
        for pc in pcset:
            pcset2.add(t(pc.pc * -1))
    return pcset2


def make_pcset12(*args):
    """
    Makes a pcset
    :param *args: Pcs
    :return: A pcset
    """
    pcset = set()
    if type(args[0]) == list:
        args = args[0]
    for pc in args:
        pcset.add(pitch.PitchClass12(pc))
    return pcset


def make_pcset24(*args):
    """
    Makes a pcset
    :param *args: Pcs
    :return: A pcset
    """
    pcset = set()
    if type(args[0]) == list:
        args = args[0]
    for pc in args:
        pcset.add(pitch.PitchClass24(pc))
    return pcset


def make_subset_graph(set_class, smallest_cardinality=1, show_graph=False, size=(800, 1100)):
    """
    Makes a subset graph
    :param set_class: A set-class
    :param smallest_cardinality: The smallest cardinality to include in the graph
    :param show_graph: Whether or not to generate a visualization of the graph
    :param size: The size of the visualized graph
    :return: A graph
    """
    g = networkx.DiGraph()
    scs = list(set_class.get_subset_classes())
    for s in scs:
        if len(s.pcset) >= smallest_cardinality:
            g.add_node(s.name_prime)
    for i in range(0, len(scs)):
        for j in range(0, i):
            if scs[i].contains_abstract_subset(scs[j]) and len(scs[j].pcset) >= smallest_cardinality:
                g.add_edge(scs[i].name_prime, scs[j].name_prime)
        for j in range(i + 1, len(scs)):
            if scs[i].contains_abstract_subset(scs[j]) and len(scs[j].pcset) >= smallest_cardinality:
                g.add_edge(scs[i].name_prime, scs[j].name_prime)
    if show_graph:
        net = pyvis.network.Network(f"{size[0]}px", f"{size[1]}px", directed=True, bgcolor="#eeeeee",
                                    font_color="#333333", heading="Subset Graph")
        net.toggle_hide_edges_on_drag(False)
        net.barnes_hut()
        net.from_nx(g, default_node_size=40)
        for node in net.nodes:
            node["title"] = node["id"]
            node["color"] = "#41b535"
        for edge in net.edges:
            edge["color"] = "#1c4219"
        net.show("subset_graph.html")
    return g


def multiply(pcset: set, n: int):
    """
    Multiplies a pcset
    :param pcset: The pcset
    :param n: The multiplier
    :return: The multiplied pcset
    """
    pcset2 = set()
    if len(pcset) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcset)))
        for pc in pcset:
            pcset2.add(t(pc.pc * n))
    return pcset2


def partitions2(pcset: set):
    """
    Gets all partitions of a pcset (size 2 or 1)
    :param pcset: A pcset
    :return: A list of all partitions
    """
    subs = subsets(pcset)
    partitions_dict = {}
    partitions_list = []
    len_pcset = (len(pcset) + 1) // 2 if len(pcset) % 2 else len(pcset) // 2
    for sub in subs:
        if len(sub) <= len_pcset:
            s = frozenset(sub)
            d = frozenset(pcset.difference(sub))
            if d not in partitions_dict:
                partitions_dict[s] = d
    for s in partitions_dict:
        partitions_list.append((set(s), set(partitions_dict[s])))
    return partitions_list


def set_class_filter12(name: str, sets: list):
    """
    Filters a list of pcsets
    :param name: The name to find
    :param sets: A list of sets to filter
    :return: A filtered list
    """
    newlist = []
    sc = SetClass12()
    for s in sets:
        sc.pcset = s
        if sc.name_prime == name or sc.name_forte == name or sc.name_morris == name:
            newlist.append(s)
    return newlist


def subsets(pcset: set):
    """
    Gets all subsets of a pcset, using the bit masking solution from
    https://afteracademy.com/blog/print-all-subsets-of-a-given-set
    :param pcset: A pcset
    :return: A list containing all subsets of the pcset
    """
    total = 2 ** len(pcset)
    sub = []
    if total > 1:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcset)))
        pcseg = list(pcset)
        pcseg.sort()
        for index in range(total):
            sub.append([])
            for i in range(len(pcset)):
                if index & (1 << i):
                    sub[index].append(t(pcseg[i].pc))
        sub.sort()
    return sub


def transpose(pcset: set, n: int):
    """
    Transposes a pcset
    :param pcset: The pcset
    :param n: The index of transposition
    :return: The transposed pcset
    """
    pcset2 = set()
    if len(pcset) > 0:
        # Need to support both PitchClass12 and PitchClass24, so use a type alias
        t = type(next(iter(pcset)))
        for pc in pcset:
            pcset2.add(t(pc.pc + n))
    return pcset2


def visualize(pcset: set):
    """
    Visualizes a pcset
    :param pcset: A pcset
    :return: A visualization
    """
    line = ""
    if len(pcset) > 0:
        t = type(next(iter(pcset)))
        n = 12
        if t == pitch.PitchClass24:
            n = 24
        for i in range(n):
            if t(i) in pcset:
                line += "X"
            else:
                line += " "
    return line
