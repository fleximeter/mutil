"""
File: pitch.py
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


class PitchClass12:
    def __init__(self, pc: int = 0):
        """
        Creates a PitchClass
        :param pc: The pitch class integer
        """
        self._pc = pc % 12

    def __add__(self, other):
        return PitchClass12(self.pc + other.pc)

    def __eq__(self, other):
        return self.pc == other.pc

    def __ge__(self, other):
        return self.pc >= other.pc

    def __gt__(self, other):
        return self.pc > other.pc

    def __hash__(self):
        return self.pc

    def __le__(self, other):
        return self.pc <= other.pc

    def __lt__(self, other):
        return self.pc < other.pc

    def __mul__(self, other):
        return PitchClass12(self.pc * other.pc)

    def __ne__(self, other):
        return self.pc != other.pc

    def __repr__(self):
        # return "<pctheory.pitch.PitchClass object at " + str(id(self)) + ">: " + self.pc_char
        return self.pc_str

    def __str__(self):
        return self.pc_str

    def __sub__(self, other):
        return PitchClass12(self.pc - other.pc)

    @property
    def pc(self):
        """
        The pitch-class integer
        :return: The pitch-class integer
        """
        return self._pc

    @pc.setter
    def pc(self, value: int):
        """
        The pitch-class integer
        :param value: The new pitch-class integer
        :return:
        """
        self._pc = value % 12
        if self._pc < 0:
            self._pc += 12

    @property
    def pc_str(self):
        """
        The pitch-class string
        :return: The pitch-class string
        """
        if self._pc == 10:
            return 'A'
        elif self._pc == 11:
            return 'B'
        else:
            return str(self._pc)


class PitchClass24:
    def __init__(self, pc: int = 0):
        """
        Creates a quarter-tone PitchClass
        :param pc: The pitch class integer
        """
        self._pc = pc % 24

    def __add__(self, other):
        return PitchClass24(self.pc + other.pc)

    def __eq__(self, other):
        return self.pc == other.pc

    def __ge__(self, other):
        return self.pc >= other.pc

    def __gt__(self, other):
        return self.pc > other.pc

    def __hash__(self):
        return self.pc

    def __le__(self, other):
        return self.pc <= other.pc

    def __lt__(self, other):
        return self.pc < other.pc

    def __mul__(self, other):
        return PitchClass24(self.pc * other.pc)

    def __ne__(self, other):
        return self.pc != other.pc

    def __repr__(self):
        # return "<pctheory.pitch.PitchClass24 object at " + str(id(self)) + ">: " + self.pc_char
        return self.pc_str

    def __str__(self):
        return self.pc_str

    def __sub__(self, other):
        return PitchClass24(self.pc - other.pc)

    @property
    def pc(self):
        """
        The pitch-class integer
        :return: The pitch-class integer
        """
        return self._pc

    @pc.setter
    def pc(self, value: int):
        """
        The pitch-class integer
        :param value: The new pitch-class integer
        :return:
        """
        self._pc = value % 24
        if self._pc < 0:
            self._pc += 24

    @property
    def pc_str(self):
        """
        The pitch-class string
        :return: The pitch-class string
        """
        if self._pc < 10:
            return f"0{self._pc}"
        else:
            return str(self._pc)


class Pitch12(PitchClass12):
    """
    Represents a pitch
    """
    def __init__(self, p: int = 0, pname: str = 0):
        """
        Creates a Pitch
        :param p: The pitch integer
        :param pname: The pitch name as a string
        """
        pc = p % 12
        super().__init__(pc)
        self._p = p
        self._pname = pname
        self.pc = p

    def __add__(self, other):
        return Pitch12(self.p + other.p)

    def __eq__(self, other):
        return self.p == other.p

    def __ge__(self, other):
        return self.p >= other.p

    def __gt__(self, other):
        return self.p > other.p

    def __hash__(self):
        return self.p

    def __le__(self, other):
        return self.p <= other.p

    def __lt__(self, other):
        return self.p < other.p

    def __mul__(self, other):
        return Pitch12(self.p * other.p)

    def __ne__(self, other):
        return self.p != other.p

    def __repr__(self):
        # return "<pctheory.pitch.Pitch object at " + str(id(self)) + ">: " + str(self._p)
        return str(self._p)

    def __str__(self):
        return str(self._p)

    def __sub__(self, other):
        return Pitch12(self.p - other.p)

    @property
    def p(self):
        """
        The pitch integer
        :return: The pitch integer
        """
        return self._p

    @p.setter
    def p(self, value: int):
        """
        The pitch integer
        :param value: The new pitch integer
        :return:
        """
        self._p = value
        self.pc = self._p

    @property
    def pname(self):
        """
        The pitch name of the pitch
        :return: The pitch name
        """
        return self._pname

    @pname.setter
    def pname(self, value: str):
        """
        The pitch name of the pitch
        :param value: The new name
        :return:
        """
        self._pname = value

    @property
    def midi(self):
        """
        The MIDI version of the pitch integer
        :return: The MIDI version of the pitch integer
        """
        return self._p + 60

    @midi.setter
    def midi(self, value):
        """
        The MIDI version of the pitch integer
        :param value: The new MIDI version of the pitch integer
        :return:
        """
        self._p = value - 60
        self.pc = self._p


class Pitch24(PitchClass24):
    """
    Represents a pitch
    """
    def __init__(self, p: int = 0, pname: str = 0):
        """
        Creates a Pitch
        :param p: The pitch integer
        :param pname: The pitch name as a string
        """
        pc = p % 24
        super().__init__(pc)
        self._p = p
        self._pname = pname
        self.pc = p

    def __add__(self, other):
        return Pitch24(self.p + other.p)

    def __eq__(self, other):
        return self.p == other.p

    def __ge__(self, other):
        return self.p >= other.p

    def __gt__(self, other):
        return self.p > other.p

    def __hash__(self):
        return self.p

    def __le__(self, other):
        return self.p <= other.p

    def __lt__(self, other):
        return self.p < other.p

    def __mul__(self, other):
        return Pitch24(self.p * other.p)

    def __ne__(self, other):
        return self.p != other.p

    def __repr__(self):
        # return "<pctheory.pitch.Pitch object at " + str(id(self)) + ">: " + str(self._p)
        return str(self._p)

    def __str__(self):
        return str(self._p)

    def __sub__(self, other):
        return Pitch24(self.p - other.p)

    @property
    def p(self):
        """
        The pitch integer
        :return: The pitch integer
        """
        return self._p

    @p.setter
    def p(self, value: int):
        """
        The pitch integer
        :param value: The new pitch integer
        :return:
        """
        self._p = value
        self.pc = self._p

    @property
    def pname(self):
        """
        The pitch name of the pitch
        :return: The pitch name
        """
        return self._pname

    @pname.setter
    def pname(self, value: str):
        """
        The pitch name of the pitch
        :param value: The new name
        :return:
        """
        self._pname = value
