"""
File: schutz.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for analyzing Schutz's "Ein Kind Ist Uns Geboren".
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

import analyze.salami_slice_analyze as salami_slice_analyze
import chart
import music21
import time

if __name__ == "__main__":
    google_drive_desktop = r"H:\My Drive"
    google_drive_laptop = r"C:\Users\Jeffrey Martin\Google Drive (jmartin8@umbc.edu)"
    google_drive = google_drive_desktop
    print("################### Vertical Analyzer ####################\n" +
          "Copyright (c) 2021 by Jeffrey Martin. All rights reserved.\nhttps://jeffreymartincomposer.com\n")
    xml = google_drive + r"\Composition\Carter Paper\Flows from String Quartet No. 5\Schutz - " \
                         r"Ein Kind Ist Uns Geboren - Full score - 01 Ein Kind Ist Uns Geboren.xml"
    xml2 = r"C:\Users\Jeffrey Martin\Desktop\Mozart Symphony 41 - Full score - 01 .xml"
    xml_corpus = "beethoven/opus59no3/movement1.mxl"
    output = google_drive + r"\Composition\Carter Paper\RegisterAnalyzer\results_schutz.csv"
    output2 = r"C:\Users\Jeffrey Martin\Desktop\mozart.csv"
    output3 = r"C:\Users\Jeffrey Martin\Desktop\beethoven.csv"
    start = time.time()
    results = salami_slice_analyze.analyze(xml)
    salami_slice_analyze.write_report(output, results)
    finish = time.time() - start
    print(int(finish / 60), "minutes,", finish % 60, "seconds")
    #chart.chart_cardinality(results)
    chart.chart_pitch_onset_measure(results)
    #chart.chart_spaces(results)
