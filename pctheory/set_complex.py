"""
File: set_complex.py
Author: Jeff Martin
Date: 11/5/2021

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


class SetComplex:
    """
    Represents a Forte set-complex K or Kh around a nexus set
    """

    def __init__(self, nexus_set: pcset.SetClass12 = None):
        """
        Creates a set-complex around a nexus set
        :param nexus_set: A nexus set
        """
        self._nexus = []

    @staticmethod
    def assert_k(s: pcset.SetClass12, t: pcset.SetClass12):
        """
        Asserts that s and t are in a K-relationship
        Source: Morris, "Class Notes for Atonal Music Theory," p. 49
        :param s: A set-class
        :param t: A set-class
        :return: A boolean
        """
        s_bar = s.get_abstract_complement()
        t_bar = t.get_abstract_complement()
        return t.contains_abstract_subset(s) or \
               t_bar.contains_abstract_subset(s) or \
               s.contains_abstract_subset(t) or \
               s_bar.contains_abstract_subset(t)

    @staticmethod
    def assert_kh(s: pcset.SetClass12, t: pcset.SetClass12):
        """
        Asserts that s and t are in a Kh-relationship
        Source: Morris, "Class Notes for Atonal Music Theory," p. 49
        :param s: A set-class
        :param t: A set-class
        :return: A boolean
        """
        s_bar = s.get_abstract_complement()
        t_bar = t.get_abstract_complement()
        return (t.contains_abstract_subset(s) and t_bar.contains_abstract_subset(s)) or \
               (s.contains_abstract_subset(t) and s_bar.contains_abstract_subset(t)) or \
               (s_bar.contains_abstract_subset(t) and s_bar.contains_abstract_subset(t_bar)) or \
               (t_bar.contains_abstract_subset(s) and t_bar.contains_abstract_subset(s_bar))
