"""
File: vslice.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains the v_slice class for vertical slicing with music21.
Copyright (c) 2021 by Jeff Martin.

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

import music21
from pctheory import pitch, pcset, pset, tables


class VSlice:
    def __init__(self, duration=1, quarter_duration=1, measure=None, aslice=None):
        """
        Creates a v_slice
        :param duration: The duration of the slice, in seconds
        :param quarter_duration: The duration of the slice, in quarter notes
        :param measure: The measure number
        :param aslice: An existing slice if using copy constructor functionality
        """
        self._core = False                      # Whether or not the chord is a core harmony
        self._derived_core = False              # Whether or not the chord is a derived core harmony
        self._derived_core_associations = None  # Derived core associations, if any
        self._duration = duration    # The duration of the slice in seconds
        self._ipseg = []             # The ipseg of the slice
        self._measure = measure      # The measure number in which the slice begins
        self._p_cardinality = 0      # The number of distinct pitches present (excluding duplicates)
        self._p_count = 0            # The number of pitches present (including duplicates)
        self._pc_cardinality = 0     # The number of distinct pitch-classes present (excluding duplicates)
        self._pcseg = None           # The pcseg
        self._pcset = None           # The pcset
        self._pitchseg = []          # The pitch seg (contains duplicates)
        self._pnameseg = []          # A list of pitch names
        self._pset = None            # The pset
        self._pseg = None            # The pseg
        self._quarter_duration = quarter_duration  # The duration in quarters
        self._sc_name = None         # The set-class name of the pcset
        self._sc_name_carter = None  # The Carter set-class name of the pcset

        self._ins = None  # The INS of the slice
        self._lns = None  # The LNS of the slice
        self._lower_bound = None  # The lower bound of the slice.
        self._mediant = None  # The MT of the slice
        self._ns = None  # The NS of the slice. If the lower and upper bounds are defined, but LNS and UNS are not,
        # the NS represents the entire pitch area encompassed by the piece. Otherwise it is None.
        self._ps = None  # The PS of the slice
        self._start_position = None  # The start position in quarter notes relative to the current measure
        self._time_signature = None  # The time signature of the slice
        self._uns = None  # The UNS of the slice
        self._upper_bound = None  # The upper bound of the slice.

    @property
    def core(self):
        """
        Whether or not the chord is a core harmony
        :return: True or False
        """
        return self._core

    @property
    def derived_core(self):
        """
        Whether or not the chord is a derived core harmony
        :return: True or False
        """
        return self._derived_core

    @property
    def derived_core_associations(self):
        """
        Derived core associations, if any
        :return: Derived core associations, if any
        """
        return self._derived_core_associations

    @property
    def duration(self):
        """
        The duration
        :return: The duration
        """
        return self._duration

    @duration.setter
    def duration(self, value):
        """
        The duration
        :param value: The new duration
        :return: None
        """
        self._duration = value

    @property
    def ins(self):
        """
        The internal negative space (INS)
        :return: The internal negative space (INS)
        """
        return self._ins

    @property
    def ipseg(self):
        """
        The ipseg (ordered interval succession between adjacent pitches from low to high)
        :return: The ipseg
        """
        return self._ipseg

    @property
    def lns(self):
        """
        The lower negative space (LNS)
        :return: The lower negative space (LNS)
        """
        return self._lns

    @property
    def lower_bound(self):
        """
        The lower bound
        :return: The lower bound
        """
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value):
        """
        The lower bound
        :param value: The new lower bound
        :return: None
        """
        self._lower_bound = value

    @property
    def measure(self):
        """
        The measure number
        :return: The measure number
        """
        return self._measure

    @property
    def mediant(self):
        """
        The median trajectory (MT)
        :return: The median trajectory (MT)
        """
        return self._mediant

    @property
    def ns(self):
        """
        The negative space (NS)
        :return: The negative space (NS)
        """
        return self._ns

    @property
    def p_cardinality(self):
        """
        The pitch cardinality of the VSlice (excludes duplicates)
        :return: The pitch cardinality
        """
        return self._p_cardinality

    @property
    def p_count(self):
        """
        The pitch count of the VSlice (contains duplicates)
        :return: The pitch count
        """
        return self._p_count

    @property
    def pc_cardinality(self):
        """
        The pitch-class cardinality of the VSlice (excludes duplicates)
        :return:
        """
        return self._pc_cardinality

    @property
    def ps(self):
        """
        The positive space (PS)
        :return: The positive space (PS)
        """
        return self._ps

    @property
    def pcseg(self):
        """
        The pcseg of the VSlice
        :return: The pcseg
        """
        return self._pcseg

    @property
    def pcset(self):
        """
        The pcset of the VSlice
        :return: The pcset
        """
        return self._pcset

    @property
    def pitchseg(self):
        """
        The pitchseg of the VSlice
        :return: The pitchseg
        """
        return self._pitchseg

    @property
    def pnameseg(self):
        """
        A list of pitch names
        :return: A list of pitch names
        """
        return self._pnameseg

    @property
    def pseg(self):
        """
        The pseg of the VSlice (contains duplicates)
        :return: The pseg
        """
        return self._pseg

    @property
    def pset(self):
        """
        The pset of the VSlice
        :return: The pset
        """
        return self._pset

    @property
    def quarter_duration(self):
        """
        The duration in quarter notes
        :return: The duration in quarter notes
        """
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        """
        The duration in quarter notes
        :param value: The new duration
        :return: None
        """
        self._quarter_duration = value

    @property
    def sc_name(self):
        """
        The set-class name of the VSlice
        :return: The set-class name
        """
        return self._sc_name

    @property
    def sc_name_carter(self):
        """
        The Carter name of the VSlice
        :return: The Carter name
        """
        return self._sc_name_carter

    @property
    def start_position(self):
        """
        The start position in the measure
        :return: The start position in the measure
        """
        return self._start_position

    @start_position.setter
    def start_position(self, value):
        """
        The start position in the measure
        :param value: The new start position
        :return: None
        """
        self._start_position = value

    @property
    def time_signature(self):
        """
        The time signature (music21.meter.TimeSignature)
        :return: The time signature
        """
        return self._time_signature

    @time_signature.setter
    def time_signature(self, value):
        """
        The time signature (music21.meter.TimeSignature)
        :param value: The new time signature
        :return: None
        """
        self._time_signature = value

    @property
    def uns(self):
        """
        The upper negative space (UNS)
        :return: The upper negative space (UNS)
        """
        return self._uns

    @property
    def upper_bound(self):
        """
        The upper bound
        :return: The upper bound
        """
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, value):
        """
        The upper bound
        :param value: The new upper bound
        :return: None
        """
        self._upper_bound = value

    def add_pitches(self, pitches, pitch_names=None):
        """
        Adds pitches to the v_slice
        :param pitches: A collection of pitches to add
        :param pitch_names: A collection of pitch names (as strings) corresponding to the pitch collection
        """
        # Add each pitch to the chord
        for i in range(len(pitches)):
            self._pitchseg.append(pitches[i])
            self._pnameseg.append(pitch_names[i])
            self._p_count += 1

    def get_ipseg_string(self):
        """
        Gets the ipseg as a string
        :return: The ipseg as a string
        """
        ipseg = "\"<"
        for ip in self._ipseg:
            ipseg += str(ip) + ", "
        if ipseg[len(ipseg) - 1] == " ":
            ipseg = ipseg[:-2]
        ipseg += ">\""
        return ipseg

    def get_pcset_str(self):
        """
        The pcset
        :return: The pcset
        """
        pcset_str = "{"
        sorted_pcset = list(self._pcset)
        sorted_pcset.sort()
        for pc in sorted_pcset:
            pcset_str += str(pc)
        pcset_str += "}"
        return pcset_str

    def make_sets(self):
        """
        Makes the pctheory objects. Run this function before calculating lower and upper bounds for the piece.
        :return:
        """
        self._pset = set()
        self._pcseg = []
        self._pcset = set()
        for p in self._pitchseg:
            self._pset.add(pitch.Pitch(p))
            self._pcset.add(pitch.PitchClass(p))
        self._pseg = list(self._pset)
        self._pseg.sort()
        for p in self._pseg:
            self._pcseg.append(pitch.PitchClass(p.pc))
        if len(self._ipseg) > 0:
            self._ipseg.clear()
        for i in range(1, len(self._pseg)):
            self._ipseg.append(self._pseg[i].p - self._pseg[i - 1].p)

        # Calculate values
        self._p_cardinality = len(self._pset)
        self._pc_cardinality = len(self._pcset)


    def run_calculations(self, sc):
        """
        Calculates information about the v_slice. You must set the lower and upper bounds before running this
        method. You should also combine any v_slices that you want to combine before running this method,
        to avoid making unnecessary computations.
        :param sc: A SetClass object
        :return: None
        """
        # Calculate ps and ins
        self._ps = len(self._pset)
        if self._ps > 0:
            self._ins = self._pseg[len(self._pseg) - 1].p - self._pseg[0].p + 1 - self._ps
        else:
            self._ins = 0

        # Calculate uns, lns, ns, and mt
        if self._lower_bound is not None and self._upper_bound is not None:
            if self._ps is None or self._ps == 0:
                self._lns = None
                self._uns = None
                self._mediant = None
                self._ns = self._upper_bound - self._lower_bound + 1
            else:
                self._lns = self._pseg[0].p - self._lower_bound
                self._uns = self._upper_bound - self._pseg[len(self._pseg) - 1].p
                self._mediant = (self._lns - self._uns) / 2

        # Calculate set theory info
        sc.pcset = self._pcset
        self._sc_name = sc.name_morris
        if 1 < self.pc_cardinality < 11:
            self._sc_name_carter = sc.name_carter
        else:
            self._sc_name_carter = ""
        if (self._sc_name_carter == "18" or self._sc_name_carter == "23") and self._pc_cardinality == 4:
            self._core = True
        if self._sc_name_carter == "35" and self._pc_cardinality == 6:
            self._core = True
        self._derived_core_associations = sc.derived_core
        if self._derived_core_associations is not None:
            self._derived_core = True
