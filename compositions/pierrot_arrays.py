"""
File: pierrot_arrays.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 2/4/22

This file contains functionality for working with arrays.
"""

from pctheory import array, pcset, pitch, transformations

arrays = [
    [
        [
            [pitch.PitchClass12(4), pcset.make_pcset12(1, 5), pitch.PitchClass12(11), pcset.make_pcset12(3, 7),
             pitch.PitchClass12(6), pcset.make_pcset12(1, 5), pitch.PitchClass12(10), pcset.make_pcset12(3, 7),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(1), pcset.make_pcset12(0, 8), pitch.PitchClass12(5), pcset.make_pcset12(2, 6),
             pitch.PitchClass12(10), pcset.make_pcset12(3, 4), pitch.PitchClass12(0), pcset.make_pcset12(9, 11),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(0), pcset.make_pcset12(1, 7), pitch.PitchClass12(9), pcset.make_pcset12(8, 11),
             pitch.PitchClass12(3), pcset.make_pcset12(10, 7), pitch.PitchClass12(2), pcset.make_pcset12(5, 9),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(8), pcset.make_pcset12(11, 3), pitch.PitchClass12(4), pcset.make_pcset12(0, 10),
             pitch.PitchClass12(9), pcset.make_pcset12(11, 5), pitch.PitchClass12(6), pcset.make_pcset12(10, 2),
             pitch.PitchClass12(7)],
            [pitch.PitchClass12(4), pcset.make_pcset12(9, 1), pitch.PitchClass12(8), pcset.make_pcset12(3, 7),
             pitch.PitchClass12(11), pcset.make_pcset12(1, 4), pitch.PitchClass12(5), pcset.make_pcset12(2, 3),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(7), pcset.make_pcset12(8, 11), pitch.PitchClass12(1), pcset.make_pcset12(0, 6),
             pitch.PitchClass12(10), pcset.make_pcset12(2, 3), pitch.PitchClass12(7), pcset.make_pcset12(8, 4),
             pitch.PitchClass12(0)],
            [pitch.PitchClass12(2), pcset.make_pcset12(10, 5), pitch.PitchClass12(9), pcset.make_pcset12(6, 7),
             pitch.PitchClass12(1), pcset.make_pcset12(11, 4), pitch.PitchClass12(5), pcset.make_pcset12(2, 10),
             pitch.PitchClass12(6)]
        ],
        [
            [pitch.PitchClass12(5), pcset.make_pcset12(0, 9, 4), pitch.PitchClass12(10), pcset.make_pcset12(2, 3, 6),
             pitch.PitchClass12(0), pcset.make_pcset12(8, 10, 4), pitch.PitchClass12(5), pcset.make_pcset12(2, 6, 7),
             pitch.PitchClass12(10)],
            [pitch.PitchClass12(4), pcset.make_pcset12(10, 11, 6), pitch.PitchClass12(2), pcset.make_pcset12(0, 8, 5),
             pitch.PitchClass12(4), pcset.make_pcset12(9, 3, 11), pitch.PitchClass12(8), pcset.make_pcset12(1, 5, 10),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(11), pcset.make_pcset12(1, 2, 7), pitch.PitchClass12(6), pcset.make_pcset12(1, 4, 9),
             pitch.PitchClass12(5), pcset.make_pcset12(0, 2, 6), pitch.PitchClass12(10), pcset.make_pcset12(0, 1, 8),
             pitch.PitchClass12(4)],
            [pitch.PitchClass12(6), pcset.make_pcset12(3, 10, 2), pitch.PitchClass12(8), pcset.make_pcset12(1, 10, 5),
             pitch.PitchClass12(9), pcset.make_pcset12(10, 2, 7), pitch.PitchClass12(3), pcset.make_pcset12(1, 4, 11),
             pitch.PitchClass12(7)],
            [pitch.PitchClass12(2), pcset.make_pcset12(0, 8, 7), pitch.PitchClass12(3), pcset.make_pcset12(9, 11, 6),
             pitch.PitchClass12(7), pcset.make_pcset12(1, 5, 9), pitch.PitchClass12(0), pcset.make_pcset12(7, 10, 11),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(10), pcset.make_pcset12(1, 5, 9), pitch.PitchClass12(3), pcset.make_pcset12(11, 6, 7),
             pitch.PitchClass12(9), pcset.make_pcset12(0, 11, 5), pitch.PitchClass12(4), pcset.make_pcset12(2, 3, 7),
             pitch.PitchClass12(11)],
            [pitch.PitchClass12(5), pcset.make_pcset12(10, 3, 6), pitch.PitchClass12(11), pcset.make_pcset12(2, 4, 7),
             pitch.PitchClass12(3), pcset.make_pcset12(8, 10, 4), pitch.PitchClass12(0), pcset.make_pcset12(2, 6, 9),
             pitch.PitchClass12(10)],
        ],
        [
            [pitch.PitchClass12(11), pcset.make_pcset12(0, 2, 10, 6), pitch.PitchClass12(5), pcset.make_pcset12(0, 8, 10, 4),
             pitch.PitchClass12(1), pcset.make_pcset12(0, 4, 7, 9), pitch.PitchClass12(11), pcset.make_pcset12(3, 6, 7, 8),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(8), pcset.make_pcset12(1, 4, 5, 6), pitch.PitchClass12(10), pcset.make_pcset12(0, 2, 5, 6),
             pitch.PitchClass12(9), pcset.make_pcset12(1, 3, 4, 10), pitch.PitchClass12(5), pcset.make_pcset12(0, 1, 2, 7),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(5), pcset.make_pcset12(8, 9, 2, 7), pitch.PitchClass12(1), pcset.make_pcset12(8, 11, 6, 7),
             pitch.PitchClass12(3), pcset.make_pcset12(5, 7, 8, 9), pitch.PitchClass12(0), pcset.make_pcset12(1, 4, 5, 8),
             pitch.PitchClass12(10)],
            [pitch.PitchClass12(0), pcset.make_pcset12(11, 10, 3, 6), pitch.PitchClass12(8), pcset.make_pcset12(1, 3, 5, 9),
             pitch.PitchClass12(10), pcset.make_pcset12(3, 4, 9, 11), pitch.PitchClass12(7), pcset.make_pcset12(0, 3, 8, 11),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(10), pcset.make_pcset12(1, 3, 5, 9), pitch.PitchClass12(4), pcset.make_pcset12(8, 1, 3, 7),
             pitch.PitchClass12(11), pcset.make_pcset12(0, 3, 6, 8), pitch.PitchClass12(10), pcset.make_pcset12(2, 6, 9, 11),
             pitch.PitchClass12(4)],
            [pitch.PitchClass12(4), pcset.make_pcset12(11, 2, 10, 7), pitch.PitchClass12(0), pcset.make_pcset12(9, 2, 10, 5),
             pitch.PitchClass12(6), pcset.make_pcset12(0, 4, 5, 8), pitch.PitchClass12(11), pcset.make_pcset12(0, 5, 7, 10),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(0), pcset.make_pcset12(11, 4, 5, 6), pitch.PitchClass12(8), pcset.make_pcset12(11, 3, 6, 7),
             pitch.PitchClass12(1), pcset.make_pcset12(2, 5, 7, 10), pitch.PitchClass12(3), pcset.make_pcset12(0, 1, 8, 9),
             pitch.PitchClass12(5)]
        ]
    ],
    [
        [
            [pitch.PitchClass12(10), pcset.make_pcset12(1, 2), pitch.PitchClass12(8), pcset.make_pcset12(0, 4),
             pitch.PitchClass12(3), pcset.make_pcset12(11, 6), pitch.PitchClass12(10), pcset.make_pcset12(4, 5),
             pitch.PitchClass12(2)],
            [pitch.PitchClass12(6), pcset.make_pcset12(11, 7), pitch.PitchClass12(2), pcset.make_pcset12(1, 5),
             pitch.PitchClass12(9), pcset.make_pcset12(10, 4), pitch.PitchClass12(6), pcset.make_pcset12(0, 5),
             pitch.PitchClass12(8)],
            [pitch.PitchClass12(3), pcset.make_pcset12(9, 10), pitch.PitchClass12(1), pcset.make_pcset12(8, 7),
             pitch.PitchClass12(5), pcset.make_pcset12(0, 9), pitch.PitchClass12(4), pcset.make_pcset12(11, 3),
             pitch.PitchClass12(7)],
            [pitch.PitchClass12(2), pcset.make_pcset12(1, 6), pitch.PitchClass12(9), pcset.make_pcset12(11, 3),
             pitch.PitchClass12(8), pcset.make_pcset12(1, 10), pitch.PitchClass12(2), pcset.make_pcset12(11, 7),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(9), pcset.make_pcset12(10, 6), pitch.PitchClass12(4), pcset.make_pcset12(0, 8),
             pitch.PitchClass12(1), pcset.make_pcset12(5, 6), pitch.PitchClass12(10), pcset.make_pcset12(8, 4),
             pitch.PitchClass12(11)],
            [pitch.PitchClass12(4), pcset.make_pcset12(11, 3), pitch.PitchClass12(8), pcset.make_pcset12(9, 1),
             pitch.PitchClass12(5), pcset.make_pcset12(10, 11), pitch.PitchClass12(7), pcset.make_pcset12(1, 6),
             pitch.PitchClass12(9)]
        ],
        [
            [pitch.PitchClass12(9), pcset.make_pcset12(2, 4, 5), pitch.PitchClass12(10), pcset.make_pcset12(8, 11, 6),
             pitch.PitchClass12(2), pcset.make_pcset12(0, 8, 4), pitch.PitchClass12(9), pcset.make_pcset12(4, 5, 6),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(4), pcset.make_pcset12(0, 8, 11), pitch.PitchClass12(6), pcset.make_pcset12(2, 10, 5),
             pitch.PitchClass12(8), pcset.make_pcset12(1, 2, 9), pitch.PitchClass12(4), pcset.make_pcset12(0, 3, 8),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(0), pcset.make_pcset12(1, 3, 7), pitch.PitchClass12(8), pcset.make_pcset12(1, 5, 9),
             pitch.PitchClass12(10), pcset.make_pcset12(11, 3, 7), pitch.PitchClass12(5), pcset.make_pcset12(1, 6, 9),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(10), pcset.make_pcset12(8, 3, 6), pitch.PitchClass12(2), pcset.make_pcset12(11, 4, 7),
             pitch.PitchClass12(3), pcset.make_pcset12(8, 4, 9), pitch.PitchClass12(1), pcset.make_pcset12(2, 5, 11),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(8), pcset.make_pcset12(9, 2, 6), pitch.PitchClass12(1), pcset.make_pcset12(0, 8, 4),
             pitch.PitchClass12(10), pcset.make_pcset12(0, 2, 6), pitch.PitchClass12(7), pcset.make_pcset12(3, 4, 11),
             pitch.PitchClass12(2)],
            [pitch.PitchClass12(3), pcset.make_pcset12(8, 11, 7), pitch.PitchClass12(1), pcset.make_pcset12(9, 4, 5),
             pitch.PitchClass12(7), pcset.make_pcset12(10, 2, 3), pitch.PitchClass12(9), pcset.make_pcset12(1, 5, 10),
             pitch.PitchClass12(8)]
        ],
        [
            [pitch.PitchClass12(0), pcset.make_pcset12(8, 2, 4, 7), pitch.PitchClass12(1), pcset.make_pcset12(8, 9, 4, 5),
             pitch.PitchClass12(11), pcset.make_pcset12(2, 4, 7, 8), pitch.PitchClass12(6), pcset.make_pcset12(1, 3, 8, 10),
             pitch.PitchClass12(2)],
            [pitch.PitchClass12(9), pcset.make_pcset12(11, 1, 10, 3), pitch.PitchClass12(6), pcset.make_pcset12(11, 2, 10, 7),
             pitch.PitchClass12(4), pcset.make_pcset12(5, 9, 10, 11), pitch.PitchClass12(1), pcset.make_pcset12(0, 4, 6, 11),
             pitch.PitchClass12(8)],
            [pitch.PitchClass12(4), pcset.make_pcset12(1, 11, 5, 9), pitch.PitchClass12(10), pcset.make_pcset12(0, 11, 3, 7),
             pitch.PitchClass12(5), pcset.make_pcset12(1, 3, 8, 11), pitch.PitchClass12(4), pcset.make_pcset12(0, 1, 7, 9),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(2), pcset.make_pcset12(8, 3, 4, 6), pitch.PitchClass12(11), pcset.make_pcset12(1, 4, 5, 6),
             pitch.PitchClass12(9), pcset.make_pcset12(2, 3, 4, 6), pitch.PitchClass12(10), pcset.make_pcset12(2, 5, 7, 9),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(8), pcset.make_pcset12(0, 10, 11, 4), pitch.PitchClass12(5), pcset.make_pcset12(0, 8, 3, 9),
             pitch.PitchClass12(1), pcset.make_pcset12(0, 4, 6, 9), pitch.PitchClass12(2), pcset.make_pcset12(3, 4, 7, 11),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(3), pcset.make_pcset12(10, 5, 6, 7), pitch.PitchClass12(1), pcset.make_pcset12(2, 11, 5, 6),
             pitch.PitchClass12(9), pcset.make_pcset12(2, 3, 8, 10), pitch.PitchClass12(6), pcset.make_pcset12(1, 3, 8, 11),
             pitch.PitchClass12(7)]
        ]
    ],
    [
        [
            [pitch.PitchClass12(4), pcset.make_pcset12(0, 10), pitch.PitchClass12(3), pcset.make_pcset12(11, 7),
             pitch.PitchClass12(8), pcset.make_pcset12(9, 1), pitch.PitchClass12(4), pcset.make_pcset12(10, 3),
             pitch.PitchClass12(6)],
            [pitch.PitchClass12(1), pcset.make_pcset12(8, 4), pitch.PitchClass12(9), pcset.make_pcset12(2, 6),
             pitch.PitchClass12(10), pcset.make_pcset12(0, 4), pitch.PitchClass12(3), pcset.make_pcset12(11, 6),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(0), pcset.make_pcset12(9, 2), pitch.PitchClass12(8), pcset.make_pcset12(10, 11),
             pitch.PitchClass12(4), pcset.make_pcset12(9, 5), pitch.PitchClass12(0), pcset.make_pcset12(3, 7),
             pitch.PitchClass12(11)],
            [pitch.PitchClass12(8), pcset.make_pcset12(0, 1), pitch.PitchClass12(5), pcset.make_pcset12(2, 4),
             pitch.PitchClass12(10), pcset.make_pcset12(6, 7), pitch.PitchClass12(0), pcset.make_pcset12(1, 5),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(6), pcset.make_pcset12(10, 4), pitch.PitchClass12(9), pcset.make_pcset12(0, 5),
             pitch.PitchClass12(11), pcset.make_pcset12(3, 4), pitch.PitchClass12(8), pcset.make_pcset12(9, 5),
             pitch.PitchClass12(1)]
        ],
        [
            [pitch.PitchClass12(2), pcset.make_pcset12(1, 9, 7), pitch.PitchClass12(6), pcset.make_pcset12(10, 2, 11),
             pitch.PitchClass12(8), pcset.make_pcset12(0, 9, 2), pitch.PitchClass12(4), pcset.make_pcset12(2, 7, 11),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(1), pcset.make_pcset12(0, 8, 6), pitch.PitchClass12(4), pcset.make_pcset12(1, 9, 7),
             pitch.PitchClass12(5), pcset.make_pcset12(1, 10, 6), pitch.PitchClass12(0), pcset.make_pcset12(1, 4, 8),
             pitch.PitchClass12(11)],
            [pitch.PitchClass12(8), pcset.make_pcset12(9, 2, 4), pitch.PitchClass12(1), pcset.make_pcset12(3, 10, 2),
             pitch.PitchClass12(6), pcset.make_pcset12(0, 1, 4), pitch.PitchClass12(8), pcset.make_pcset12(2, 5, 10),
             pitch.PitchClass12(6)],
            [pitch.PitchClass12(6), pcset.make_pcset12(8, 2, 10), pitch.PitchClass12(1), pcset.make_pcset12(9, 2, 5),
             pitch.PitchClass12(0), pcset.make_pcset12(2, 11, 6), pitch.PitchClass12(7), pcset.make_pcset12(3, 4, 11),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(10), pcset.make_pcset12(1, 5, 6), pitch.PitchClass12(0), pcset.make_pcset12(8, 3, 4),
             pitch.PitchClass12(6), pcset.make_pcset12(2, 10, 5), pitch.PitchClass12(0), pcset.make_pcset12(3, 10, 11),
             pitch.PitchClass12(7)]
        ],
        [
            [pitch.PitchClass12(10), pcset.make_pcset12(8, 9, 3, 6), pitch.PitchClass12(2), pcset.make_pcset12(1, 10, 5, 7),
             pitch.PitchClass12(9), pcset.make_pcset12(0, 5, 7, 8), pitch.PitchClass12(3), pcset.make_pcset12(6, 7, 8, 11),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(8), pcset.make_pcset12(1, 11, 4, 5), pitch.PitchClass12(3), pcset.make_pcset12(0, 9, 11, 4),
             pitch.PitchClass12(7), pcset.make_pcset12(1, 2, 3, 11), pitch.PitchClass12(8), pcset.make_pcset12(1, 3, 5, 10),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(4), pcset.make_pcset12(10, 3, 5, 7), pitch.PitchClass12(11), pcset.make_pcset12(8, 3, 6, 7),
             pitch.PitchClass12(1), pcset.make_pcset12(4, 7, 9, 11), pitch.PitchClass12(0), pcset.make_pcset12(1, 4, 8, 10),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(0), pcset.make_pcset12(1, 4, 6, 9), pitch.PitchClass12(2), pcset.make_pcset12(8, 1, 10, 3),
             pitch.PitchClass12(6), pcset.make_pcset12(0, 1, 7, 8), pitch.PitchClass12(4), pcset.make_pcset12(1, 2, 6, 9),
             pitch.PitchClass12(10)],
            [pitch.PitchClass12(5), pcset.make_pcset12(0, 1, 6, 7), pitch.PitchClass12(9), pcset.make_pcset12(0, 11, 3, 4),
             pitch.PitchClass12(7), pcset.make_pcset12(2, 4, 6, 11), pitch.PitchClass12(8), pcset.make_pcset12(1, 2, 6, 10),
             pitch.PitchClass12(3)]
        ]
    ],
    [
        [
            [pitch.PitchClass12(6), pcset.make_pcset12(9, 10), pitch.PitchClass12(4), pcset.make_pcset12(0, 8),
             pitch.PitchClass12(11), pcset.make_pcset12(2, 6), pitch.PitchClass12(7), pcset.make_pcset12(1, 5),
             pitch.PitchClass12(8)],
            [pitch.PitchClass12(3), pcset.make_pcset12(11, 4), pitch.PitchClass12(8), pcset.make_pcset12(9, 1),
             pitch.PitchClass12(5), pcset.make_pcset12(11, 3), pitch.PitchClass12(0), pcset.make_pcset12(10, 6),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(2), pcset.make_pcset12(8, 9), pitch.PitchClass12(0), pcset.make_pcset12(3, 7),
             pitch.PitchClass12(1), pcset.make_pcset12(8, 9), pitch.PitchClass12(4), pcset.make_pcset12(3, 7),
             pitch.PitchClass12(11)],
            [pitch.PitchClass12(8), pcset.make_pcset12(0, 3), pitch.PitchClass12(7), pcset.make_pcset12(11, 5),
             pitch.PitchClass12(4), pcset.make_pcset12(0, 1), pitch.PitchClass12(6), pcset.make_pcset12(10, 2),
             pitch.PitchClass12(7)]
        ],
        [
            [pitch.PitchClass12(1), pcset.make_pcset12(9, 2, 7), pitch.PitchClass12(6), pcset.make_pcset12(8, 10, 11),
             pitch.PitchClass12(2), pcset.make_pcset12(0, 8, 4), pitch.PitchClass12(9), pcset.make_pcset12(1, 4, 5),
             pitch.PitchClass12(6)],
            [pitch.PitchClass12(8), pcset.make_pcset12(1, 3, 7), pitch.PitchClass12(11), pcset.make_pcset12(2, 10, 6),
             pitch.PitchClass12(8), pcset.make_pcset12(1, 4, 9), pitch.PitchClass12(2), pcset.make_pcset12(3, 4, 11),
             pitch.PitchClass12(7)],
            [pitch.PitchClass12(2), pcset.make_pcset12(9, 3, 5), pitch.PitchClass12(10), pcset.make_pcset12(3, 11, 7),
             pitch.PitchClass12(0), pcset.make_pcset12(2, 10, 6), pitch.PitchClass12(5), pcset.make_pcset12(0, 1, 9),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(10), pcset.make_pcset12(8, 1, 6), pitch.PitchClass12(2), pcset.make_pcset12(0, 1, 5),
             pitch.PitchClass12(9), pcset.make_pcset12(10, 2, 7), pitch.PitchClass12(3), pcset.make_pcset12(5, 6, 9),
             pitch.PitchClass12(1)]
        ],
        [
            [pitch.PitchClass12(9), pcset.make_pcset12(1, 10, 11, 5), pitch.PitchClass12(4), pcset.make_pcset12(0, 9, 2, 5),
             pitch.PitchClass12(8), pcset.make_pcset12(1, 4, 7, 11), pitch.PitchClass12(9), pcset.make_pcset12(2, 4, 6, 10),
             pitch.PitchClass12(11)],
            [pitch.PitchClass12(5), pcset.make_pcset12(0, 9, 3, 7), pitch.PitchClass12(8), pcset.make_pcset12(11, 3, 4, 7),
             pitch.PitchClass12(1), pcset.make_pcset12(3, 5, 8, 9), pitch.PitchClass12(2), pcset.make_pcset12(0, 7, 8, 9),
             pitch.PitchClass12(4)],
            [pitch.PitchClass12(11), pcset.make_pcset12(8, 4, 5, 6), pitch.PitchClass12(0), pcset.make_pcset12(8, 9, 2, 4),
             pitch.PitchClass12(7), pcset.make_pcset12(0, 3, 8, 10), pitch.PitchClass12(6), pcset.make_pcset12(2, 4, 7, 11),
             pitch.PitchClass12(10)],
            [pitch.PitchClass12(6), pcset.make_pcset12(10, 3, 5, 7), pitch.PitchClass12(1), pcset.make_pcset12(9, 4, 5, 6),
             pitch.PitchClass12(11), pcset.make_pcset12(0, 4, 5, 10), pitch.PitchClass12(8), pcset.make_pcset12(3, 6, 10, 11),
             pitch.PitchClass12(2)]
        ]
    ],
    [
        [
            [pitch.PitchClass12(4), pcset.make_pcset12(8, 7), pitch.PitchClass12(2), pcset.make_pcset12(10, 6),
             pitch.PitchClass12(9), pcset.make_pcset12(8, 1), pitch.PitchClass12(4), pcset.make_pcset12(2, 10),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(1), pcset.make_pcset12(10, 5), pitch.PitchClass12(6), pcset.make_pcset12(11, 7),
             pitch.PitchClass12(3), pcset.make_pcset12(10, 4), pitch.PitchClass12(0), pcset.make_pcset12(11, 5),
             pitch.PitchClass12(9)],
            [pitch.PitchClass12(0), pcset.make_pcset12(4, 6), pitch.PitchClass12(1), pcset.make_pcset12(10, 11),
             pitch.PitchClass12(5), pcset.make_pcset12(0, 4), pitch.PitchClass12(9), pcset.make_pcset12(10, 2),
             pitch.PitchClass12(6)]
        ],
        [
            [pitch.PitchClass12(2), pcset.make_pcset12(0, 3, 7), pitch.PitchClass12(8), pcset.make_pcset12(2, 5, 6),
             pitch.PitchClass12(10), pcset.make_pcset12(0, 8, 3), pitch.PitchClass12(4), pcset.make_pcset12(2, 7, 11),
             pitch.PitchClass12(3)],
            [pitch.PitchClass12(10), pcset.make_pcset12(2, 11, 6), pitch.PitchClass12(4), pcset.make_pcset12(0, 1, 10),
             pitch.PitchClass12(8), pcset.make_pcset12(1, 2, 6), pitch.PitchClass12(9), pcset.make_pcset12(0, 4, 8),
             pitch.PitchClass12(7)],
            [pitch.PitchClass12(1), pcset.make_pcset12(8, 2, 4), pitch.PitchClass12(9), pcset.make_pcset12(10, 11, 6),
             pitch.PitchClass12(2), pcset.make_pcset12(8, 4, 9), pitch.PitchClass12(0), pcset.make_pcset12(2, 3, 10),
             pitch.PitchClass12(6)]
        ],
        [
            [pitch.PitchClass12(7), pcset.make_pcset12(11, 9, 10, 3), pitch.PitchClass12(4), pcset.make_pcset12(8, 11, 3, 6),
             pitch.PitchClass12(0), pcset.make_pcset12(3, 4, 5, 7), pitch.PitchClass12(9), pcset.make_pcset12(4, 5, 6, 11),
             pitch.PitchClass12(1)],
            [pitch.PitchClass12(11), pcset.make_pcset12(0, 1, 5, 8), pitch.PitchClass12(3), pcset.make_pcset12(1, 10, 5, 9),
             pitch.PitchClass12(6), pcset.make_pcset12(0, 2, 10, 11), pitch.PitchClass12(5), pcset.make_pcset12(1, 2, 7, 9),
             pitch.PitchClass12(0)],
            [pitch.PitchClass12(8), pcset.make_pcset12(1, 2, 3, 7), pitch.PitchClass12(11), pcset.make_pcset12(0, 1, 6, 8),
             pitch.PitchClass12(4), pcset.make_pcset12(0, 5, 6, 9), pitch.PitchClass12(2), pcset.make_pcset12(0, 7, 8, 11),
             pitch.PitchClass12(4)]
        ]
    ],
    [
        [
            [pitch.PitchClass12(1), pcset.make_pcset12(11, 5), pitch.PitchClass12(4), pcset.make_pcset12(0, 8),
             pitch.PitchClass12(3), pcset.make_pcset12(11, 6), pitch.PitchClass12(10), pcset.make_pcset12(2, 4),
             pitch.PitchClass12(5)],
            [pitch.PitchClass12(0), pcset.make_pcset12(4, 7), pitch.PitchClass12(11), pcset.make_pcset12(10, 6),
             pitch.PitchClass12(2), pcset.make_pcset12(5, 7), pitch.PitchClass12(1), pcset.make_pcset12(0, 10),
             pitch.PitchClass12(6)]
        ],
        [
            [pitch.PitchClass12(2), pcset.make_pcset12(1, 9, 7), pitch.PitchClass12(6), pcset.make_pcset12(10, 2, 11),
             pitch.PitchClass12(8), pcset.make_pcset12(0, 9, 2), pitch.PitchClass12(4), pcset.make_pcset12(1, 5, 9),
             pitch.PitchClass12(6)],
            [pitch.PitchClass12(1), pcset.make_pcset12(8, 11, 7), pitch.PitchClass12(3), pcset.make_pcset12(0, 8, 6),
             pitch.PitchClass12(4), pcset.make_pcset12(8, 1, 9), pitch.PitchClass12(2), pcset.make_pcset12(3, 4, 11),
             pitch.PitchClass12(7)]
        ],
        [
            [pitch.PitchClass12(6), pcset.make_pcset12(9, 2, 3, 4), pitch.PitchClass12(10), pcset.make_pcset12(8, 1, 5, 6),
             pitch.PitchClass12(2), pcset.make_pcset12(4, 7, 8, 11), pitch.PitchClass12(6), pcset.make_pcset12(0, 2, 5, 7),
             pitch.PitchClass12(10)],
            [pitch.PitchClass12(5), pcset.make_pcset12(0, 8, 2, 10), pitch.PitchClass12(1), pcset.make_pcset12(9, 4, 5, 7),
             pitch.PitchClass12(0), pcset.make_pcset12(1, 6, 7, 10), pitch.PitchClass12(2), pcset.make_pcset12(4, 6, 9, 10),
             pitch.PitchClass12(11)]
        ]
    ]
]

t = array.transform_row_content(arrays[5][2], transformations.OTO(1, 0, 11))
m = array.make_array_chain(t, 1, False)
for i in range(len(m)):
    print(m[i])
