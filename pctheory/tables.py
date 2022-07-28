"""
File: tables.py
Author: Jeff Martin
Date: 10/31/2021

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

import importlib.resources
import json


def create_tables_sc12():
    """
    Creates tables for SetClass12 objects
    :return: Tables
    """
    with importlib.resources.open_text("pctheory", "sc12.json") as table_json:
        return json.loads(table_json.read())


def create_tables_row():
    """
    Creates tables for twelve-tone rows
    :return: Tables
    """
    with importlib.resources.open_text("pctheory", "row12.json") as table_json:
        return json.loads(table_json.read())
