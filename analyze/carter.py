"""
File: carter.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for analyzing register for Carter's fifth string quartet.
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

import v_analyze
import chart
import time
from fractions import Fraction
from decimal import Decimal


def c_analyze():
    """
    Analyzes Carter's fifth string quartet without analyzing each section separately
    """
    xml = r"D:\Carter Paper\Flows from String Quartet No. 5\Carter " \
          r"String Quartet 5 - Full score - 01 Introduction.xml "
    output = r"D:\Carter Paper\RegisterAnalyzer\results_carter.csv"
    start = time.time()
    v_analyze.analyze(xml, output)
    finish = time.time() - start
    print(int(finish / 60), "minutes,", round(finish % 60, 3), "seconds")


def c_analyze_with_sections():
    """
    Analyzes Carter's fifth string quartet, as well as analyzing each section separately
    """
    # Sections
    measure_nos = [
        (1, 24), (25, 64), (65, 85), (86, 110), (111, 132), (133, 164), (165, 192), (193, 222), (223, 250),
        (251, 281), (282, 308), (309, 331)
    ]
    sections = [
        (1, 24), (25, 64), (65, 85), (86, 110), (111, 132), (133, 164), (165, 192), (193, 222), (223, 250),
        (251, 281), (282, 308), (309, 331), (1, 24), (25, 64), (65, 85), (86, 110), (111, 132), (133, 164),
        (165, 192), (193, 222), (223, 250), (251, 281), (282, 308), (309, 331)
    ]
    section_names = [
        "Introduction", "Giocoso", "Interlude I", "Lento espressivo", "Interlude II", "Presto scorrevole",
        "Interlude III", "Allegro energico", "Interlude IV", "Adagio sereno", "Interlude V", "Capriccioso"
    ]
    bound_prefs = [
        False, False, False, False, False, False, False, False, False, False, False, False,
        True, True, True, True, True, True, True, True, True, True, True, True
    ]
    voices = ["Violin 1", "Violin 2", "Viola", "Cello"]

    # Path names
    path = "D:\\Carter Paper\\"
    path_laptop = "C:\\Users\\Jeff Martin\\Documents\\Carter Paper\\"
    # path = path_laptop
    xml = path + "Flows from String Quartet No. 5\\Carter String Quartet 5 - Full score - 01 Introduction.xml "
    output = path + "Register Analysis Files\\entire_piece.csv"
    output_general = path + "Register Analysis Files\\statistics.csv"
    results_path = path + "Register Analysis Files\\data.json"
    output_global = []
    for i in range(12):
        cname = section_names[i].split(" ")
        c_path = path + f"Register Analysis Files\\{i + 1}_"
        for j in range(len(cname) - 1):
            c_path += cname[j] + "_"
        c_path += cname[len(cname) - 1] + "_broad.csv"
        output_global.append(c_path)
    output_local = []
    for i in range(12):
        cname = section_names[i].split(" ")
        c_path = path + f"Register Analysis Files\\{i + 1}_"
        for j in range(len(cname) - 1):
            c_path += cname[j] + "_"
        c_path += cname[len(cname) - 1] + "_local.csv"
        output_local.append(c_path)

    # Record starting time
    start = time.time()
    use_cache = True

    # Analyze
    print("Analyzing...")
    results = None

    if use_cache:
        results = v_analyze.read_analysis_from_file(results_path)
    else:
        results = v_analyze.analyze_with_sections(xml, sections, bound_prefs)
    v_analyze.write_analysis_to_file(results, results_path)

    v_analyze.write_general_report("Full piece", output_general, "w", results[0], results[0].lower_bound,
                                   results[0].upper_bound)
    v_analyze.write_report(output, results[0])
    for i in range(1, len(output_global) + 1):
        v_analyze.write_general_report("Section " + str(i) + " global", output_general, "a", results[i],
                                       results[0].lower_bound, results[0].upper_bound)
        v_analyze.write_report(output_global[i - 1], results[i])
    for i in range(13, len(output_local) + 13):
        v_analyze.write_general_report("Section " + str(i - 12) + " local", output_general, "a", results[i],
                                       results[0].lower_bound, results[0].upper_bound)
        v_analyze.write_report(output_local[i - 13], results[i])

    # Make charts
    chart.chart_cardinality(results[0], False, "Pset Cardinality Graph for Elliott Carter’s Fifth String Quartet",
                            size=(14, 6), path=path + f"Register Analysis Files\\Graphs\\card_m")
    chart.chart_cardinality(results[0], True, "Pset Cardinality Graph for Elliott Carter’s Fifth String Quartet",
                            size=(14, 6), path=path + f"Register Analysis Files\\Graphs\\card_t")
    chart.chart_pitch_onset(results[0], False, "Pitch Onsets in Elliott Carter’s Fifth String Quartet", (14, 6),
                            path + f"Register Analysis Files\\Graphs\\onset_measure")
    for i in range(len(voices)):
        chart.chart_pitch_onset(results[0], False, f"Pitch Onsets in Elliott Carter’s Fifth String Quartet "
                                                   f"({voices[i]})", (14, 6),
                                path + f"Register Analysis Files\\Graphs\\onset_measure_{voices[i]}", i)
    chart.chart_pitch_onset(results[0], True, "Pitch Onsets in Elliott Carter’s Fifth String Quartet", (14, 6),
                            path + f"Register Analysis Files\\Graphs\\onset_time")
    for i in range(len(voices)):
        chart.chart_pitch_onset(results[0], True, f"Pitch Onsets in Elliott Carter’s Fifth String Quartet "
                                                   f"({voices[i]})", (14, 6),
                                path + f"Register Analysis Files\\Graphs\\onset_time_{voices[i]}", i)
    chart.chart_pitch_duration(results[0], "Pitch Duration in Elliott Carter’s Fifth String Quartet", (14, 6),
                               path + f"Register Analysis Files\\Graphs\\pitch_duration")
    for i in range(len(voices)):
        chart.chart_pitch_duration(results[0], f"Pitch Duration in Elliott Carter’s Fifth String Quartet "
                                               f"({voices[i]})", (14, 6),
                                   path + f"Register Analysis Files\\Graphs\\pitch_duration_{voices[i]}", i)
    chart.chart_pc_duration(results[0], "Pitch-Class Duration in Elliott Carter’s Fifth String Quartet", (8, 6),
                            path + f"Register Analysis Files\\Graphs\\pc_duration")
    for i in range(len(voices)):
        chart.chart_pc_duration(results[0], f"Pitch-Class Duration in Elliott Carter’s Fifth String Quartet "
                                            f"({voices[i]})", (8, 6),
                                path + f"Register Analysis Files\\Graphs\\pc_duration_{voices[i]}", i)

    for i in range(1, 13):
        cname = section_names[i - 1].split(" ")
        cm_path = path + f"Register Analysis Files\\Graphs\\card_m_{i}_"
        ct_path = path + f"Register Analysis Files\\Graphs\\card_t_{i}_"
        om_path = path + f"Register Analysis Files\\Graphs\\onset_m_{i}_"
        ot_path = path + f"Register Analysis Files\\Graphs\\onset_t_{i}_"
        dp_path = path + f"Register Analysis Files\\Graphs\\dur_pitch_{i}_"
        dpc_path = path + f"Register Analysis Files\\Graphs\\dur_pc_{i}_"
        for j in range(len(cname) - 1):
            cm_path += cname[j] + "_"
            ct_path += cname[j] + "_"
            om_path += cname[j] + "_"
            ot_path += cname[j] + "_"
            dp_path += cname[j] + "_"
            dpc_path += cname[j] + "_"
        cm_path += cname[len(cname) - 1]
        ct_path += cname[len(cname) - 1]
        om_path += cname[len(cname) - 1]
        ot_path += cname[len(cname) - 1]
        dp_path += cname[len(cname) - 1]
        dpc_path += cname[len(cname) - 1]
        chart.chart_cardinality(results[i], False, f"Pset Cardinality Graph for Section {i} – " + section_names[i - 1],
                                path=cm_path)
        chart.chart_cardinality(results[i], True, f"Pset Cardinality Graph for Section {i} – " + section_names[i - 1],
                                path=ct_path)
        chart.chart_pitch_onset(results[i], False, f"Pitch Onsets in Section {i} – " + section_names[i - 1],
                                path=om_path)
        for j in range(len(voices)):
            chart.chart_pitch_onset(results[i], False, f"Pitch Onsets in Section {i} ({voices[j]}) – " +
                                    section_names[i - 1], path=om_path + f"_{voices[j]}", voice=j)
        chart.chart_pitch_onset(results[i], True, f"Pitch Onsets in Section {i} – " + section_names[i - 1],
                                path=ot_path)
        for j in range(len(voices)):
            chart.chart_pitch_onset(results[i], True, f"Pitch Onsets in Section {i} ({voices[j]}) – " +
                                    section_names[i - 1], path=ot_path + f"_{voices[j]}", voice=j)
        chart.chart_pitch_duration(results[i], f"Pitch Durations in Section {i} – " + section_names[i - 1],
                                   path=dp_path)
        for j in range(len(voices)):
            chart.chart_pitch_duration(results[i], f"Pitch Durations in Section {i} ({voices[j]}) – " +
                                       section_names[i - 1], path=dp_path + f"_{voices[j]}", voice=j)
        chart.chart_pc_duration(results[i], f"Pitch-Class Durations in Section {i} – " + section_names[i - 1],
                                path=dpc_path)
        for j in range(len(voices)):
            chart.chart_pc_duration(results[i], f"Pitch-Class Durations in Section {i} ({voices[j]}) – " +
                                    section_names[i - 1], path=dpc_path + f"_{voices[j]}", voice=j)

    for i in range(results[0].lower_bound, results[0].upper_bound + 1):
        total = Decimal(0)
        parts = Decimal(0)
        if i in results[0].pitch_duration:
            total = results[0].pitch_duration[i]
        for j in range(4):
            if i in results[0].pitch_duration_voices[j]:
                parts += results[0].pitch_duration_voices[j][i]
        print(f"{i}: {total - parts}")

    # Print elapsed time
    finish = time.time() - start
    print("\nTotal elapsed time:", int(finish / 60), "minutes,", round(finish % 60, 3), "seconds")


def metric_modulation():
    # Carter Quartet 5
    m = {}

    # q = 72
    m[24] = Fraction(Fraction(3, 4), 1)  # q = 96
    m[25] = Fraction(Fraction(1, 4), Fraction(1, 6))  # q = 64
    m[45] = Fraction(Fraction(1, 8), Fraction(1, 7))  # q = 73+ (512/7)
    m[65] = Fraction(Fraction(4, 3), 1)  # q = 55- (384/7)
    m[71] = Fraction(Fraction(4, 7), 1)  # q = 96
    m[77] = Fraction(Fraction(8, 5), 1)  # q = 60
    m[123] = Fraction(Fraction(5, 4), 1)  # q = 48
    m[127] = Fraction(Fraction(Fraction(5, 2), 3), 2)  # h = 57.6
    m[174] = Fraction(Fraction(8, 5), 1)  # q = 72
    m[231] = Fraction(Fraction(2, 3), 1)  # q = 108
    m[238] = Fraction(Fraction(3, 2), 1)  # q = 72
    m[241] = Fraction(Fraction(3, 4), Fraction(1, 2))  # q = 48
    m[282] = Fraction(Fraction(1, 2), 1)  # q = 96
    m[308] = Fraction(Fraction(4, 5), Fraction(1, 2))  # q = 60

    for i in m:
        print(i, m[i])


if __name__ == "__main__":
    print("################### Vertical Analyzer ####################\n" + \
          "Copyright (c) 2022 by Jeffrey Martin. All rights reserved.\nhttps://jeffreymartincomposer.com\n")
    # c_analyze()
    c_analyze_with_sections()
    # metric_modulation()
