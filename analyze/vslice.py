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
from statistics import pstdev


class VSlice:
    def __init__(self, duration=1, quarter_duration=1, measure=None, aslice=None):
        """
        Creates a v_slice
        :param duration: The duration of the slice, in seconds
        :param quarter_duration: The duration of the slice, in quarter notes
        :param measure: The measure number
        :param aslice: An existing slice if using copy constructor functionality
        """
        if aslice is not None:
            self._cardinality = aslice.cardinality
            self._chord = aslice.chord
            self._duration = aslice.duration
            self._forte = aslice.forte
            self._ins = aslice.ins
            self._inversion_number = aslice.inversion_number
            self._ipseg = aslice.ipseg
            self._lns = aslice.lns
            self._lower_bound = aslice.lower_bound
            self._measure = aslice.measure
            self._mediant = aslice.mediant
            self._meant = aslice.meant
            self._ns = aslice.ns
            self._pcset_set = aslice.pcset_set
            self._pitch_list = list(aslice.pitch_list)
            self._pitched_common_name = aslice.pitched_common_name
            self._pitches = set(aslice.pitches)
            self._pitches_sorted = list(aslice.pitches_sorted)
            self._prime_form = aslice.prime_form
            self._ps = aslice.ps
            self._quarter_duration = aslice.quarter_duration
            self._start_position = aslice.start_position
            self._time_signature = aslice.time_signature
            self._uns = aslice.uns
            self._upper_bound = aslice.upper_bound
        else:
            self._cardinality = 0  # The cardinality of the slice
            self._chord = None  # The chord
            self._duration = duration  # The duration of the slice in seconds
            self._forte = None  # The Forte name of the chord
            self._ins = None  # The INS of the slice
            self._inversion_number = 0  # The inversion number of the chord if it is a tertian sonority
            self._ipseg = []  # The ipseg of the slice
            self._lns = None  # The LNS of the slice
            self._lower_bound = None  # The lower bound of the slice.
            self._measure = measure  # The measure number in which the slice begins
            self._mediant = None  # The MT of the slice
            self._meant = None  # The mT of the slice
            self._ns = None  # The NS of the slice. If the lower and upper bounds are defined, but LNS and UNS are not,
            # the NS represents the entire pitch area encompassed by the piece. Otherwise it is None.
            self._pcset_set = set()  # The pcset of the current v_slice
            self._pitch_list = []  # A list of pitches in the chord
            self._pitched_common_name = ""  # The pitched common name
            self._pitches = set()  # A list of distinct p-integers represented in the slice
            self._pitches_sorted = []  # A sorted list of pitches
            self._prime_form = None  # The prime form of the slice
            self._ps = None  # The PS of the slice
            self._quarter_duration = quarter_duration  # The duration in quarters
            self._start_position = None  # The start position in quarter notes relative to the current measure
            self._time_signature = None  # The time signature of the slice
            self._uns = None  # The UNS of the slice
            self._upper_bound = None  # The upper bound of the slice.

    @property
    def cardinality(self):
        """
        The cardinality (number of pitches, including doublings)
        :return: The cardinality
        """
        return self._cardinality

    @property
    def chord(self):
        """
        A music21 Chord object representing the VSlice
        :return: A music21 Chord object representing the VSlice
        """
        return self._chord

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
    def forte(self):
        """
        The Forte name
        :return: The Forte name
        """
        return self._forte

    @property
    def ins(self):
        """
        The internal negative space (INS)
        :return: The internal negative space (INS)
        """
        return self._ins

    @property
    def inversion_number(self):
        """
        The inversion number (as in triads)
        :return: The inversion number
        """
        return self._inversion_number

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
    def meant(self):
        """
        The mean trajectory (NT)
        :return: The mean trajectory (NT)
        """
        return self._meant

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
    def pcset_set(self):
        """
        The pcset
        :return: A set
        """
        return self._pcset_set

    @property
    def pitch_list(self):
        """
        A list of pitch names as strings (with duplicates)
        :return: A list of pitch names as strings
        """
        return self._pitch_list

    @property
    def pitched_common_name(self):
        """
        The common name of the chord
        :return: The common name of the chord
        """
        return self._pitched_common_name

    @property
    def pitches(self):
        """
        A set of pitches
        :return: A set of pitches
        """
        return self._pitches

    @property
    def pitches_sorted(self):
        """
        A sorted list of pitches
        :return: A sorted list of pitches
        """
        return self._pitches_sorted

    @property
    def prime_form(self):
        """
        The prime form
        :return: The prime form
        """
        return self._prime_form

    @property
    def ps(self):
        """
        The positive space (PS)
        :return: The positive space (PS)
        """
        return self._ps

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
        for p in pitch_names:
            self._pitch_list.append(p)
        self._cardinality = len(self._pitch_list)
        for pitch in pitches:
            self._pitches.add(pitch)

    def calculate_meant(self):
        """
        Calculates the mean trajectory
        """
        if self._ps > 0 and self._upper_bound != None and self._lower_bound != None:
            mean = 0
            for p in self._pitches:
                mean += p
            mean /= self._ps
            self._meant = mean - (self._upper_bound + self._lower_bound) / 2

    def get_ipseg_stdev(self):
        """
        Gets the population standard deviation of the v_slice ipseg
        :return: The standard deviation
        """
        if len(self._ipseg) > 0:
            return pstdev(self._ipseg)
        else:
            return None

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

    def make_pitches_sorted(self):
        """
        Makes a sorted pitch list
        :return: None
        """
        self._pitches_sorted = list(self._pitches)
        self._pitches_sorted.sort()
        for i in range(1, len(self._pitches_sorted)):
            self._ipseg.append(self._pitches_sorted[i] - self._pitches_sorted[i - 1])

    def get_pcset_str(self):
        """
        The pcset
        :return: The pcset
        """
        pcset_str = "{"
        sorted_pcset = list(self._pcset_set)
        sorted_pcset.sort()
        for pc in sorted_pcset:
            if pc == 10:
                pcset_str += "A"
            elif pc == 11:
                pcset_str += "B"
            else:
                pcset_str += str(pc)
        pcset_str += "}"
        return pcset_str

    def run_calculations(self):
        """
        Calculates information about the v_slice. You must set the lower and upper bounds before running this
        method. You should also combine any v_slices that you want to combine before running this method,
        to avoid making unnecessary computations.
        :return: None
        """
        if len(self._pitches_sorted) < len(self._pitches):
            self.make_pitches_sorted()

        # Calculate ps and ins
        self._ps = len(self._pitches)
        if self._ps > 0:
            self._ins = self._pitches_sorted[len(self._pitches_sorted) - 1] - self._pitches_sorted[0] + 1 - self._ps
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
                self._lns = self._pitches_sorted[0] - self._lower_bound
                self._uns = self._upper_bound - self._pitches_sorted[len(self._pitches_sorted) - 1]
                self._mediant = (self._lns - self._uns) / 2

        # Create music21 Chord object to represent the v_slice
        self._chord = music21.chord.Chord()
        for p in self._pitch_list:
            self._chord.add(p)
        if self._cardinality > 0:
            self._pitched_common_name = self._chord.pitchedCommonName
            self._inversion_number = self._chord.inversion()

        # Calculate set theory info
        self._forte = self._chord.forteClass
        self._prime_form = "["
        for pc in self._chord.primeForm:
            if pc == 10:
                self._prime_form += "A"
            elif pc == 11:
                self._prime_form += "B"
            else:
                self._prime_form += str(pc)
        self._prime_form += "]"
        for p in self._pitches:
            pc = p % 12
            if pc < 0:
                pc += 12
            self._pcset_set.add(pc)
