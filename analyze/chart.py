"""
File: chart.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for making analysis charts.
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

import matplotlib.pyplot
import numpy


def chart_cardinality(results, title="Cardinality Chart", size=(8, 6), path=None):
    """
    Makes a step plot of cardinality
    :param results: A Results object
    :param title: The title of the plot
    :param size: The size of the plot
    :param path: A path to save the chart
    :return: None
    """
    matplotlib.pyplot.clf()
    matplotlib.pyplot.rcParams["font.family"] = "Academico"
    ps_s = []
    x = []
    for s in results.slices:
        position = s.measure + float(s.start_position / s.time_signature.barDuration.quarterLength)
        x.append(position)
        if s.ps is not None:
            ps_s.append(s.ps)
        else:
            ps_s.append(0)
    fig = matplotlib.pyplot.figure(figsize=size)
    ax = fig.add_subplot(111)
    ax.step(x, ps_s, color="#555555", linewidth=0.5, markersize=1)
    matplotlib.pyplot.title(title, fontsize=18)
    matplotlib.pyplot.xlabel("Measure No.")
    matplotlib.pyplot.ylabel("Pset Cardinality")
    if path is None:
        matplotlib.pyplot.show()
    else:
        matplotlib.pyplot.savefig(path)
        matplotlib.pyplot.close()


def chart_pitch_onset(results, title="Pitch Onset Graph", size=(8, 6), path=None):
    """
    Makes a pitch onset chart
    :param results: A Results object
    :param title: The title of the plot
    :param size: The size of the plot
    :param path: A path to save the chart
    :return: None
    """
    matplotlib.pyplot.clf()
    matplotlib.pyplot.rcParams["font.family"] = "Academico"
    pitches = [[] for i in range(results.max_p_count)]
    x = []
    for s in range(len(results.slices)):
        position = results.slices[s].measure
        position += float(results.slices[s].start_position / results.slices[s].time_signature.barDuration.quarterLength)
        x.append(position)
        for i in range(len(pitches)):
            if i < len(results.slices[s].pseg):
                if s - 1 >= 0:
                    if results.slices[s].pseg[i] not in results.slices[s - 1].pset:
                        pitches[i].append(results.slices[s].pseg[i].p)
                    else:
                        pitches[i].append(numpy.nan)
                else:
                    pitches[i].append(results.slices[s].pseg[i].p)
            else:
                pitches[i].append(numpy.nan)
    draw = matplotlib.pyplot.figure(figsize=size)
    axes = draw.add_subplot(111)
    for i in range(len(pitches)):
        axes.scatter(x, pitches[i], c='#222222', marker='.')
    ytick_tick = []
    ytick_labels = []
    for i in range(results.lower_bound, results.upper_bound + 1):
        if i % 12 == 0:
            ytick_tick.append(i)
            ytick_labels.append(f"C{i // 12 + 4}/{i}")
    matplotlib.pyplot.yticks(ytick_tick, ytick_labels)
    matplotlib.pyplot.title(title, fontsize=18)
    matplotlib.pyplot.xlabel("Measure No.")
    matplotlib.pyplot.ylabel("Pitch")

    if path is None:
        matplotlib.pyplot.show()
    else:
        matplotlib.pyplot.savefig(path)
        matplotlib.pyplot.close()


def chart_spaces(results, size=(8, 6), path=None):
    """
    Makes a pitch space stacked area chart
    :param results: A Results object
    :param size: The size of the plot
    :param path: A path to save the chart
    :return: None
    """
    matplotlib.pyplot.clf()
    x = []
    ins = []
    lns = []
    ns = []
    ps = []
    uns = []
    for s in results.slices:
        position = s.measure + float(s.start_position / s.time_signature.barDuration.quarterLength)
        x.append(position)
        if s.ins is not None:
            ins.append(s.ins)
        else:
            ins.append(0)
        if s.ps is not None:
            ps.append(s.ps)
        else:
            ps.append(0)
        if s.uns is None:
            lns.append(0)
            uns.append(0)
            ns.append(results.lps_card)
        else:
            lns.append(s.lns)
            uns.append(s.uns)
            ns.append(0)
    """
    matplotlib.pyplot.step(x, uns, fillstyle="full")
    matplotlib.pyplot.step(x, ps)
    """
    labels = ["NS", "LNS", "INS", "PS", "UNS"]
    colors = ["#000000", "#333333", "#555555", "#DDDDDD", "#333333"]
    fig, ax = matplotlib.pyplot.subplots()
    matplotlib.pyplot.figure(figsize=size)
    ax.stackplot(x, ns, lns, ins, ps, uns, labels=labels, colors=colors)
    ax.legend(loc="upper left")
    if path is None:
        matplotlib.pyplot.show()
    else:
        matplotlib.pyplot.savefig(path)
        matplotlib.pyplot.close()
