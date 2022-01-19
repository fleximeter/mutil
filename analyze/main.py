"""
File: VerticalAnalyzer.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for analyzing MusicXML scores.
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

import analyze
import chart
import time

if __name__ == "__main__":
    print("################### Vertical Analyzer ####################\n" + \
          "Copyright (c) 2021 by Jeffrey Martin. All rights reserved.\nhttps://jeffreymartincomposer.com\n")
    print("Enter path of MusicXML file to analyze:")
    xml = input()
    print("Enter destination file name (should end in .csv or .txt):")
    output = input()
    whole = input("Analyze entire piece (y/n)? ")
    first = -1
    last = -1
    use_local = "N"
    if whole.upper() == "N":
        first = int(input("Enter first measure # to analyze: "))
        last = int(input("Enter last measure # to analyze: "))
        use_local = str(input("Use local bounds (y/n)? ")).upper()
    if use_local == "Y":
        use_local = True
    else:
        use_local = False
    start = time.time()
    print("Analyzing...")
    results = analyze.v_analyze(xml, first, last, use_local=use_local)
    analyze.write_report(output, results)
    finish = time.time() - start
    print("Done")
    # print(int(finish / 60), "minutes,", finish % 60, "seconds")
