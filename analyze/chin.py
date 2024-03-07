"""
File: chin.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for analyzing register for Chin's Piano Etude (In C).
Copyright (c) 2024 by Jeff Martin.

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

import salami_slice_analyze
import chart
import time
from fractions import Fraction
from decimal import Decimal


def c_analyze():
    """
    Analyzes Chin's "In C" without analyzing each section separately
    """
    
    # Path names
    path = "D:\\chin_paper\\"
    path_laptop = "C:\\Users\\jeffr\\chin_paper\\"
    path = path_laptop
    xml = f"{path}chin_etude_1_6staff.musicxml"
    output = f"{path}analysis\\entire_piece.csv"
    output_general = f"{path}analysis\\statistics.csv"
    results_path = f"{path}analysis\\data.json"
    
    # Record starting time
    start = time.time()

    # Analyze
    print("Analyzing entire piece...")
    results = None

    results = salami_slice_analyze.analyze(xml)
    results_staff = [salami_slice_analyze.analyze(xml, staff_indices=[i]) for i in range(0, 6)]

    salami_slice_analyze.write_general_report("Full piece", output_general, "w", results[0], results[0].lower_bound,
                                   results[0].upper_bound)
    salami_slice_analyze.write_report(output, results[0])
    salami_slice_analyze.write_statistics(f"{path}\\analysis\\csegs.csv", "Cseg,Frequency,Duration\n",
                               [results[0].cseg_frequency, results[0].cseg_duration])
    salami_slice_analyze.write_statistics(f"{path}\\analysis\\psets.csv", "Pset,Frequency,Duration\n",
                               [results[0].pset_frequency, results[0].pset_duration])
    salami_slice_analyze.write_statistics(f"{path}\\analysis\\pscs.csv", "PSC,Frequency,Duration\n",
                               [results[0].psc_frequency, results[0].psc_duration])
    salami_slice_analyze.write_statistics(f"{path}\\analysis\\pcscs.csv", "SC,Frequency,Duration\n",
                               [results[0].pcsc_frequency, results[0].pcsc_duration])

    make_charts_general(results[0], f"{path}analysis\\graphs")
    
    for i, result in enumerate(results_staff):
        salami_slice_analyze.write_report(f"{path}analysis\\entire_piece_staff{i+1}.csv", result[0])
        salami_slice_analyze.write_statistics(f"{path}\\analysis\\psets_staff{i+1}.csv", "Pset,Frequency,Duration\n",
                                [result[0].pset_frequency, result[0].pset_duration])
        make_charts_specific(result[0], f"{path}analysis\\graphs_staff{i+1}")
    
    # Print elapsed time
    finish = time.time() - start
    print(f"\nTotal elapsed time: {int(finish / 60)} minutes, {round(finish % 60, 3)} seconds")


def make_charts_general(results, path):
    """
    Makes general charts
    :param results: A Results object
    :param path: The file path
    :return:
    """
    chart.chart_cardinality(results, False, "Pset Cardinality Graph for Unsuk Chin’s \"In C\"",
                            size=(6.5, 3), path=f"{path}\\card_m")
    chart.chart_cardinality(results, True, "Pset Cardinality Graph for Unsuk Chin’s \"In C\"",
                            size=(6.5, 3), path=f"{path}\\card_t")
    chart.chart_pitch_onset(results, False, "Pitch Onsets in Unsuk Chin’s \"In C\"", (6.5, 3),
                            f"{path}\\onset_measure")
    chart.chart_pset_spacing_index(results, False, "Pset Spacing Indices in Unsuk Chin’s \"In C\"",
                                   (6.5, 3), f"{path}\\pset_spacing_index_m")
    chart.chart_pset_spacing_index(results, True, "Pset Spacing Indices in Unsuk Chin’s \"In C\"",
                                   (6.5, 3), f"{path}\\pset_spacing_index_t")
    chart.chart_pitch_onset(results, True, "Pitch Onsets in Unsuk Chin’s \"In C\"", (6.5, 3),
                            f"{path}\\onset_time")
    chart.chart_pitch_duration(results, "Pitch Duration in Unsuk Chin’s \"In C\"", (6.5, 3),
                               f"{path}\\pitch_duration")
    chart.chart_pc_duration(results, "Pitch-Class Duration in Unsuk Chin’s \"In C\"", (6.5, 3),
                            f"{path}\\pc_duration")
                            

def make_charts_specific(results, path):
    """
    Make specific charts
    :param results: A Results object
    :param path: The file path
    :return:
    """
    chart.chart_cardinality(results, False, "Pset Cardinality Graph for Unsuk Chin’s \"In C\"",
                            size=(6.5, 3), path=f"{path}\\card_m")
    chart.chart_cardinality(results, True, "Pset Cardinality Graph for Unsuk Chin’s \"In C\"",
                            size=(6.5, 3), path=f"{path}\\card_t")
    chart.chart_pitch_onset(results, False, "Pitch Onsets in Unsuk Chin’s \"In C\"", (6.5, 3),
                            f"{path}\\onset_measure")
    chart.chart_pitch_onset(results, True, "Pitch Onsets in Unsuk Chin’s \"In C\"", (6.5, 3),
                            f"{path}\\onset_time")
    chart.chart_pitch_duration(results, "Pitch Duration in Unsuk Chin’s \"In C\"", (6.5, 3),
                               f"{path}\\pitch_duration")
    chart.chart_pc_duration(results, "Pitch-Class Duration in Unsuk Chin’s \"In C\"", (6.5, 3),
                            f"{path}\\pc_duration")
    

if __name__ == "__main__":
    print("################### Salami Slice Analyzer ####################\n" + \
          "Copyright (c) 2024 by Jeffrey Martin. All rights reserved.\nhttps://www.jeffreymartincomposer.com\n")
    c_analyze()
