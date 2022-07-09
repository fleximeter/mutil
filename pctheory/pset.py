"""
File: pset.py
Author: Jeff Martin
Date: 11/1/2021

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

from pctheory import pitch, transformations, util
import music21
import numpy


class Sieve12:
    """
    Represents a chromatic sieve
    """
    def __init__(self, tuples, base_pitch):
        """
        Creates a Sieve12
        :param tuples: A collection of tuples to add to the sieve.
        :param base_pitch: Pitch 0 for the sieve. This pitch does not actually have to be
        in the sieve - it will just serve as the 0 reference point.
        """
        self._tuples = set()
        self._ints = []
        self._period = 0
        self._base_pitch = pitch.Pitch12(base_pitch.p) if type(base_pitch) == pitch.Pitch12 \
            else pitch.Pitch12(base_pitch)
        self.add_tuples(tuples)

    @property
    def base_pitch(self):
        """
        The base pitch of the Sieve12 (pitch 0)
        :return: The base pitch
        """
        return self._base_pitch

    @property
    def ints(self):
        """
        The intervallic succession of the Sieve12
        :return: The intervallic succession
        """
        return self._ints

    @property
    def period(self):
        """
        The period of the Sieve12
        :return: The period
        """
        return self._period

    @property
    def tuples(self):
        """
        The tuples in the Sieve12
        :return: The tuples
        """
        return self._tuples

    def add_tuples(self, *args):
        """
        Adds one or more tuples to the Sieve12
        :param args: One or more tuples
        :return:
        """
        lcm_list = set()
        if type(args[0]) == set or type(args[0]) == list or type(args[0]) == tuple:
            args = args[0]
        for tup in args:
            self._tuples.add(tup)
        for tup in self._tuples:
            lcm_list.add(tup[0])
        self._period = util.lcm(lcm_list)
        r = self.get_range(pitch.Pitch12(self._base_pitch.p), pitch.Pitch12(self._base_pitch.p + self._period))
        r = list(r)
        r.sort()
        for i in range(1, len(r)):
            self._ints.append(r[i].p - r[i-1].p)

    def get_range(self, p0, p1):
        """
        Gets all pitches in the sieve between p0 and p1
        :param p0: The low pitch
        :param p1: The high pitch
        :return: A pset
        """
        ps = set()
        p_low = p0.p if type(p0) == pitch.Pitch12 else p0
        p_high = p1.p + 1 if type(p1) == pitch.Pitch12 else p1 + 1
        for j in range(p_low, p_high):
            i = j - self._base_pitch.p
            if i >= 0:
                for tup in self._tuples:
                    if i % tup[0] == tup[1]:
                        ps.add(pitch.Pitch12(j))
        return ps

    def intersection(self, sieve):
        """
        Intersects two Sieve12s
        :param sieve: A Sieve12
        :return: A new Sieve12. It will have the same base pitch as self.
        """
        t = set()
        for tup1 in self._tuples:
            for tup2 in sieve.tuples:
                if tup1 == tup2:
                    t.add(tup1)
        return Sieve12(t, self._base_pitch)

    def is_in_sieve(self, p):
        """
        Whether or not a pitch or pset is in the sieve
        :param p: A pitch (Pitch12 or int) or pset
        :return: True or False
        """
        ps = None
        if type(p) == set:
            ps = p
        elif type(p) == pitch.Pitch12:
            ps = {p}
        elif type(p) == int:
            ps = {pitch.Pitch12(p)}
        for q in ps:
            i = q.p - self._base_pitch.p
            if i < 0:
                return False
            else:
                for tup in self._tuples:
                    if i % tup[0] == tup[1]:
                        break
                else:
                    return False
        return True

    def union(self, sieve):
        """
        Unions two Sieve12s
        :param sieve: A Sieve12
        :return: A new Sieve12. It will have the same base pitch as self.
        """
        t = set()
        for tup in self._tuples:
            t.add(tup)
        for tup in sieve.tuples:
            t.add(tup)
        return Sieve12(t, self._base_pitch)


class Sieve24:
    """
    Represents a microtonal sieve
    """
    def __init__(self, tuples, base_pitch):
        """
        Creates a Sieve24
        :param tuples: A collection of tuples to add to the sieve.
        :param base_pitch: Pitch 0 for the sieve. This pitch does not actually have to be
        in the sieve - it will just serve as the 0 reference point.
        """
        self._tuples = set()
        self._ints = []
        self._period = 0
        self._base_pitch = pitch.Pitch24(base_pitch.p) if type(base_pitch) == pitch.Pitch24 \
            else pitch.Pitch24(base_pitch)
        self.add_tuples(tuples)

    @property
    def base_pitch(self):
        """
        The base pitch of the Sieve24 (pitch 0)
        :return: The base pitch
        """
        return self._base_pitch

    @property
    def ints(self):
        """
        The intervallic succession of the Sieve24
        :return: The intervallic succession
        """
        return self._ints

    @property
    def period(self):
        """
        The period of the Sieve24
        :return: The period
        """
        return self._period

    @property
    def tuples(self):
        """
        The tuples in the Sieve24
        :return: The tuples
        """
        return self._tuples

    def add_tuples(self, *args):
        """
        Adds one or more tuples to the Sieve24
        :param args: One or more tuples
        :return:
        """
        lcm_list = set()
        if type(args[0]) == set or type(args[0]) == list or type(args[0]) == tuple:
            args = args[0]
        for tup in args:
            self._tuples.add(tup)
        for tup in self._tuples:
            lcm_list.add(tup[0])
        self._period = util.lcm(lcm_list)
        r = self.get_range(pitch.Pitch24(self._base_pitch.p), pitch.Pitch24(self._base_pitch.p + self._period))
        r = list(r)
        r.sort()
        for i in range(1, len(r)):
            self._ints.append(r[i].p - r[i-1].p)

    def get_range(self, p0, p1):
        """
        Gets all pitches in the sieve between p0 and p1
        :param p0: The low pitch
        :param p1: The high pitch
        :return: A pset
        """
        ps = set()
        p_low = p0.p if type(p0) == pitch.Pitch24 else p0
        p_high = p1.p + 1 if type(p1) == pitch.Pitch24 else p1 + 1
        for j in range(p_low, p_high):
            i = j - self._base_pitch.p
            if i >= 0:
                for tup in self._tuples:
                    if i % tup[0] == tup[1]:
                        ps.add(pitch.Pitch24(j))
        return ps

    def intersection(self, sieve):
        """
        Intersects two Sieve24s
        :param sieve: A Sieve24
        :return: A new Sieve24. It will have the same base pitch as self.
        """
        t = set()
        for tup1 in self._tuples:
            for tup2 in sieve.tuples:
                if tup1 == tup2:
                    t.add(tup1)
        return Sieve24(t, self._base_pitch)

    def is_in_sieve(self, p):
        """
        Whether or not a pitch or pset is in the sieve
        :param p: A pitch (Pitch24 or int) or pset
        :return: True or False
        """
        ps = None
        if type(p) == set:
            ps = p
        elif type(p) == pitch.Pitch24:
            ps = {p}
        elif type(p) == int:
            ps = {pitch.Pitch24(p)}
        for q in ps:
            i = q.p - self._base_pitch.p
            if i < 0:
                return False
            else:
                for tup in self._tuples:
                    if i % tup[0] == tup[1]:
                        break
                else:
                    return False
        return True

    def union(self, sieve):
        """
        Unions two Sieve24s
        :param sieve: A Sieve24
        :return: A new Sieve24. It will have the same base pitch as self.
        """
        t = set()
        for tup in self._tuples:
            t.add(tup)
        for tup in sieve.tuples:
            t.add(tup)
        return Sieve24(t, self._base_pitch)


def fb_class(pset: set, p0: int):
    """
    Gets the FB-class of a pset
    :param pset: The pset
    :param p0: The lowest pitch
    :return: The FB-class as a list of integers
    """
    intlist = []
    n = 12 if type(next(iter(pset))) == pitch.PitchClass12 else 24
    for p in pset:
        intlist.append((p.p - p0) % n)
    intlist.sort()
    if len(intlist) > 0:
        del intlist[0]
    return intlist


def invert(pset: set):
    """
    Inverts a pset
    :param pset: The pset
    :return: The inverted pset
    """
    pset2 = set()
    t = type(next(iter(pset)))
    for p in pset:
        pset2.add(t(p.p * -1))
    return pset2


def m21_make_pset(item):
    """
    Makes a pset from a music21 object
    :param item: A music21 object
    :return: A pset
    """
    pset2 = set()
    if type(item) == music21.note.Note:
        pset2.add(pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.pitch.Pitch:
        pset2.add(pitch.Pitch12(item.pitch.midi - 60))
    elif type(item) == music21.chord.Chord:
        for p in item.pitches:
            pset2.add(pitch.Pitch12(p.midi - 60))
    else:
        raise TypeError("Unsupported music21 type")
    return pset2


def make_pset12(*args):
    """
    Makes a pset
    :param *args: Ps
    :return: A pset
    """
    if type(args[0]) == list:
        args = args[0]
    return {pitch.Pitch12(p) for p in args}


def make_pset24(*args):
    """
    Makes a pset
    :param *args: Ps
    :return: A pset
    """
    if type(args[0]) == list:
        args = args[0]
    return {pitch.Pitch24(p) for p in args}


def p_ic_matrix(pset: set):
    """
    Gets the pitch ic-matrix
    :param pset: The pset
    :return: The ic-matrix as a list of lists
    """
    mx = numpy.empty((len(pset), len(pset)))
    pseg = list(pset)
    pseg.sort()
    for i in range(mx.shape[0]):
        for j in range(mx.shape[1]):
            mx[i][j] = abs(pseg[i].p - pseg[j].p)
    return mx


def p_ic_roster(pset: set):
    """
    Gets the pitch ic-roster
    :param pset: The pset
    :return: The ic-roster as a dictionary
    """
    pseg = list(pset)
    roster = {}
    pseg.sort()
    for i in range(len(pseg) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            interval = abs(pseg[i].p - pseg[j].p)
            if interval not in roster:
                roster[interval] = 1
            else:
                roster[interval] += 1
    return roster


def p_set_class(pset: set):
    """
    Gets the set-class of a pset
    :param pset: The pset
    :return: The set-class as a list of integers
    """
    pseg = list(pset)
    pseg.sort()
    intlist = []
    for i in range(1, len(pseg)):
        intlist.append(pseg[i].p - pseg[i - 1].p)
    return intlist


def pcint_class(pset: set):
    """
    Gets the PCINT-class of a pset
    :param pset: The pset
    :return: The PCINT-class as a list of integers
    """
    pseg = list(pset)
    pseg.sort()
    n = 12 if type(next(iter(pset))) == pitch.PitchClass12 else 24
    intlist = []
    for i in range(1, len(pseg)):
        intlist.append((pseg[i].p - pseg[i - 1].p) % n)
    return intlist


def pm_similarity(pset1: set, pset2: set, ic_roster1=None, ic_roster2=None):
    """
    Gets the pitch-measure (PM) similarity between pset1 and pset2
    :param pset1: A pset
    :param pset2: A pset
    :param ic_roster1: The ic_roster for pset 1. If None, will be calculated.
    :param ic_roster2: The ic_roster for pset 2. If None, will be calculated.
    :return: The PM similarity as a tuple of integers
    """
    cint = len(pset1.intersection(pset2))
    ic_shared = 0
    if ic_roster1 is None:
        ic_roster1 = p_ic_roster(pset1)
    if ic_roster2 is None:
        ic_roster2 = p_ic_roster(pset2)
    for ic in ic_roster1:
        if ic in ic_roster2:
            if ic_roster1[ic] < ic_roster2[ic]:
                ic_shared += ic_roster1[ic]
            else:
                ic_shared += ic_roster2[ic]
    return (cint, ic_shared)


def subsets(pset: set):
    """
    Gets all subsets of a pset, using the bit masking solution from
    https://afteracademy.com/blog/print-all-subsets-of-a-given-set
    :param pset: A pset
    :return: A list containing all subsets of the pset
    """
    total = 2 ** len(pset)
    t = type(next(iter(pset)))
    sub = []
    pseg = list(pset)
    pseg.sort()
    for index in range(total):
        sub.append([])
        for i in range(len(pset)):
            if index & (1 << i):
                sub[index].append(t(pseg[i].p))
    sub.sort()
    return sub


def to_pcset(pset: set):
    """
    Makes a pcset out of a pset
    :param pset: A pset
    :return: A pcset
    """
    if type(next(iter(pset))) == pitch.Pitch12:
        return {pitch.PitchClass12(p.pc) for p in pset}
    else:
        return {pitch.PitchClass24(p.pc) for p in pset}


def transform(pset: set, transformation: transformations.UTO):
    """
    Transforms a pset
    :param pset: A pset
    :param transformation: A transformation
    :return: The transformed set
    """
    pset2 = set()
    for p in pset:
        pset2.add(pitch.Pitch12(p.p * transformation[1] + transformation[0]))
    return pset2


def transpose(pset: set, n: int):
    """
    Transposes a pset
    :param pset: The pset
    :param n: The index of transposition
    :return: The transposed pset
    """
    pset2 = set()
    t = type(next(iter(pset)))
    for p in pset:
        pset2.add(t(p.p + n))
    return pset2
