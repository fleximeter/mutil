"""
File: v_analyze.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for experimenting with music21.
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

xml = r"D:\Google Drive (jmartin8@umbc.edu)\Composition\Carter Paper\Flows from String Quartet No. 5\Carter " \
      r"String Quartet 5 - Full score - 01 Introduction.xml"

stream = music21.converter.parse(xml)
parts = []
for item in stream:
    if type(item) == music21.stream.Part:
        parts.append(item)
for item in parts[1]:
    if type(item) == music21.stream.Measure:
        for item2 in item:
            print(type(item2))