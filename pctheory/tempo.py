"""
File: tempo.py
Author: Jeff Martin
Date: 6/6/2021

Copyright © 2022 by Jeffrey Martin. All rights reserved.
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

from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def make_metric_modulation_chain(initial_tempo, ratios: list):
    """
    Calculates a succession of tempos based on the provided metric modulation ratios
    :param initial_tempo: The initial tempo
    :param ratios: A list of ratios
    :return: A list of tempos
    """
    tempos = [Fraction(initial_tempo)]
    for i in range(len(ratios)):
        tempos.append(tempos[i] * ratios[i])
    return tempos


def plot_tempo_table(quarter_note_tempos: list):
    """
    Makes a table of tempos based on a list of quarter-note tempos
    :param quarter_note_tempos: A list of quarter-note tempos
    :return: None
    """
    # A list of fractional durations (whole note, half note, half triplet, etc.)
    DURATIONS = [Fraction(4, 1), Fraction(2, 1), Fraction(4, 3), Fraction(1, 1), Fraction(4, 5), Fraction(2, 3),
                 Fraction(4, 7), Fraction(1, 2), Fraction(2, 5), Fraction(1, 3), Fraction(2, 7), Fraction(1, 4),
                 Fraction(1, 5), Fraction(1, 6), Fraction(1, 7), Fraction(1, 8)]
    N = 3  # index of quarter note duration in DURATIONS
    columns = []
    rows = [f"Tempo {i+1}" for i in range(len(quarter_note_tempos))]
    for f in DURATIONS:
        if f.denominator == 1:
            columns.append(f"{f.numerator}")
        else:
            columns.append(f"{f.numerator}/{f.denominator}")

    # Convert the tempo list to Fractions
    tempos = [Fraction(t) for t in quarter_note_tempos]

    # Build the tempo table
    tempo_table = np.zeros((len(tempos), len(DURATIONS)))
    for i in range(len(tempos)):
        tempo_table[i][N] = DURATIONS[N] * tempos[i]
        for j in range(N):
            tempo_table[i][j] = tempos[i] / DURATIONS[j]
        for j in range(N + 1, len(DURATIONS)):
            tempo_table[i][j] = tempos[i] / DURATIONS[j]

    # Display the table
    df = pd.DataFrame(tempo_table, columns=columns)
    plt.rcParams["font.family"] = "Segoe UI"
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    fig.canvas.set_window_title("Tempo Table")
    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")
    t = ax.table(cellText=df.values, colLabels=columns, colColours=["#DDDDDD" for i in range(len(DURATIONS))], loc="center")
    t.auto_set_font_size(False)
    t.set_fontsize(11)
    p = t.properties()
    for c in p["celld"]:
        p["celld"][c].set(linewidth=0.5, width=0.09, height=0.08)
    fig.tight_layout()
    plt.show()
