"""
File: pierrot_arrays.py
10uthor: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 2/4/22

This file contains functionality for working with arrays.
"""

from pctheory import array, pcset, pitch

m = [
    [
        [
            [pitch.PitchClass(4), pcset.make_pcset(1, 5), pitch.PitchClass(11), pcset.make_pcset(3, 7),
             pitch.PitchClass(6), pcset.make_pcset(1, 5), pitch.PitchClass(10), pcset.make_pcset(3, 7),
             pitch.PitchClass(9)],
            [pitch.PitchClass(1), pcset.make_pcset(0, 8), pitch.PitchClass(5), pcset.make_pcset(2, 6),
             pitch.PitchClass(10), pcset.make_pcset(3, 4), pitch.PitchClass(0), pcset.make_pcset(9, 11),
             pitch.PitchClass(5)],
            [pitch.PitchClass(0), pcset.make_pcset(1, 7), pitch.PitchClass(9), pcset.make_pcset(8, 11),
             pitch.PitchClass(3), pcset.make_pcset(10, 7), pitch.PitchClass(2), pcset.make_pcset(5, 9),
             pitch.PitchClass(1)],
            [pitch.PitchClass(8), pcset.make_pcset(11, 3), pitch.PitchClass(4), pcset.make_pcset(0, 10),
             pitch.PitchClass(9), pcset.make_pcset(11, 5), pitch.PitchClass(6), pcset.make_pcset(10, 2),
             pitch.PitchClass(7)],
            [pitch.PitchClass(4), pcset.make_pcset(9, 1), pitch.PitchClass(8), pcset.make_pcset(3, 7),
             pitch.PitchClass(11), pcset.make_pcset(1, 4), pitch.PitchClass(5), pcset.make_pcset(2, 3),
             pitch.PitchClass(9)],
            [pitch.PitchClass(7), pcset.make_pcset(8, 11), pitch.PitchClass(1), pcset.make_pcset(0, 6),
             pitch.PitchClass(10), pcset.make_pcset(2, 3), pitch.PitchClass(7), pcset.make_pcset(8, 4),
             pitch.PitchClass(0)],
            [pitch.PitchClass(2), pcset.make_pcset(10, 5), pitch.PitchClass(9), pcset.make_pcset(6, 7),
             pitch.PitchClass(1), pcset.make_pcset(11, 4), pitch.PitchClass(5), pcset.make_pcset(2, 10),
             pitch.PitchClass(6)]
        ],
        [
            [pitch.PitchClass(5), pcset.make_pcset(0, 9, 4), pitch.PitchClass(10), pcset.make_pcset(2, 3, 6),
             pitch.PitchClass(0), pcset.make_pcset(8, 10, 4), pitch.PitchClass(5), pcset.make_pcset(2, 6, 7),
             pitch.PitchClass(10)],
            [pitch.PitchClass(4), pcset.make_pcset(10, 11, 6), pitch.PitchClass(2), pcset.make_pcset(0, 8, 5),
             pitch.PitchClass(4), pcset.make_pcset(9, 3, 11), pitch.PitchClass(8), pcset.make_pcset(1, 5, 10),
             pitch.PitchClass(9)],
            [pitch.PitchClass(11), pcset.make_pcset(1, 2, 7), pitch.PitchClass(6), pcset.make_pcset(1, 4, 9),
             pitch.PitchClass(5), pcset.make_pcset(0, 2, 6), pitch.PitchClass(10), pcset.make_pcset(0, 1, 8),
             pitch.PitchClass(4)],
            [pitch.PitchClass(6), pcset.make_pcset(3, 10, 2), pitch.PitchClass(8), pcset.make_pcset(1, 10, 5),
             pitch.PitchClass(9), pcset.make_pcset(10, 2, 7), pitch.PitchClass(3), pcset.make_pcset(1, 4, 11),
             pitch.PitchClass(7)],
            [pitch.PitchClass(2), pcset.make_pcset(0, 8, 7), pitch.PitchClass(3), pcset.make_pcset(9, 11, 6),
             pitch.PitchClass(7), pcset.make_pcset(1, 5, 9), pitch.PitchClass(0), pcset.make_pcset(7, 10, 11),
             pitch.PitchClass(3)],
            [pitch.PitchClass(10), pcset.make_pcset(1, 5, 9), pitch.PitchClass(3), pcset.make_pcset(11, 6, 7),
             pitch.PitchClass(9), pcset.make_pcset(0, 11, 5), pitch.PitchClass(4), pcset.make_pcset(2, 3, 7),
             pitch.PitchClass(11)],
            [pitch.PitchClass(5), pcset.make_pcset(10, 3, 6), pitch.PitchClass(11), pcset.make_pcset(2, 4, 7),
             pitch.PitchClass(3), pcset.make_pcset(8, 10, 4), pitch.PitchClass(0), pcset.make_pcset(2, 6, 9),
             pitch.PitchClass(10)],
        ],
        [
            [pitch.PitchClass(11), pcset.make_pcset(0, 2, 10, 6), pitch.PitchClass(5), pcset.make_pcset(0, 8, 10, 4),
             pitch.PitchClass(1), pcset.make_pcset(0, 4, 7, 9), pitch.PitchClass(11), pcset.make_pcset(3, 6, 7, 8),
             pitch.PitchClass(1)],
            [pitch.PitchClass(8), pcset.make_pcset(1, 4, 5, 6), pitch.PitchClass(10), pcset.make_pcset(0, 2, 5, 6),
             pitch.PitchClass(9), pcset.make_pcset(1, 3, 4, 10), pitch.PitchClass(5), pcset.make_pcset(0, 1, 2, 7),
             pitch.PitchClass(9)],
            [pitch.PitchClass(5), pcset.make_pcset(8, 9, 2, 7), pitch.PitchClass(1), pcset.make_pcset(8, 11, 6, 7),
             pitch.PitchClass(3), pcset.make_pcset(5, 7, 8, 9), pitch.PitchClass(0), pcset.make_pcset(1, 4, 5, 8),
             pitch.PitchClass(10)],
            [pitch.PitchClass(0), pcset.make_pcset(11, 10, 3, 6), pitch.PitchClass(8), pcset.make_pcset(1, 3, 5, 9),
             pitch.PitchClass(10), pcset.make_pcset(3, 4, 9, 11), pitch.PitchClass(7), pcset.make_pcset(0, 3, 8, 11),
             pitch.PitchClass(5)],
            [pitch.PitchClass(10), pcset.make_pcset(1, 3, 5, 9), pitch.PitchClass(4), pcset.make_pcset(8, 1, 3, 7),
             pitch.PitchClass(11), pcset.make_pcset(0, 3, 6, 8), pitch.PitchClass(10), pcset.make_pcset(2, 6, 9, 11),
             pitch.PitchClass(4)],
            [pitch.PitchClass(4), pcset.make_pcset(11, 2, 10, 7), pitch.PitchClass(0), pcset.make_pcset(9, 2, 10, 5),
             pitch.PitchClass(6), pcset.make_pcset(0, 4, 5, 8), pitch.PitchClass(11), pcset.make_pcset(0, 5, 7, 10),
             pitch.PitchClass(3)],
            [pitch.PitchClass(0), pcset.make_pcset(11, 4, 5, 6), pitch.PitchClass(8), pcset.make_pcset(11, 3, 6, 7),
             pitch.PitchClass(1), pcset.make_pcset(2, 5, 7, 10), pitch.PitchClass(3), pcset.make_pcset(0, 1, 8, 9),
             pitch.PitchClass(5)]
        ]
    ],
    [
        [
                [pitch.PitchClass(10), pcset.make_pcset(1, 2), pitch.PitchClass(8), pcset.make_pcset(0, 4), 
                pitch.PitchClass(3), pcset.make_pcset(11, 6), pitch.PitchClass(10), pcset.make_pcset(4, 5), 
                pitch.PitchClass(2)],
                [pitch.PitchClass(6), pcset.make_pcset(11, 7), pitch.PitchClass(2), pcset.make_pcset(1, 5), 
                pitch.PitchClass(9), pcset.make_pcset(10, 4), pitch.PitchClass(6), pcset.make_pcset(0, 5), 
                pitch.PitchClass(8)],
                [pitch.PitchClass(3), pcset.make_pcset(9, 10), pitch.PitchClass(1), pcset.make_pcset(8, 7), 
                pitch.PitchClass(5), pcset.make_pcset(0, 9), pitch.PitchClass(4), pcset.make_pcset(11, 3), 
                pitch.PitchClass(7)],
                [pitch.PitchClass(2), pcset.make_pcset(1, 6), pitch.PitchClass(9), pcset.make_pcset(11, 3), 
                pitch.PitchClass(8), pcset.make_pcset(1, 10), pitch.PitchClass(2), pcset.make_pcset(11, 7), 
                pitch.PitchClass(3)],
                [pitch.PitchClass(9), pcset.make_pcset(10, 6), pitch.PitchClass(4), pcset.make_pcset(0, 8), 
                pitch.PitchClass(1), pcset.make_pcset(5, 6), pitch.PitchClass(10), pcset.make_pcset(8, 4), 
                pitch.PitchClass(11)],
                [pitch.PitchClass(4), pcset.make_pcset(11, 3), pitch.PitchClass(8), pcset.make_pcset(9, 1), 
                pitch.PitchClass(5), pcset.make_pcset(10, 11), pitch.PitchClass(7), pcset.make_pcset(1, 6), 
                pitch.PitchClass(9)]
        ],
        [
                [pitch.PitchClass(9), pcset.make_pcset(2, 4, 5), pitch.PitchClass(10), pcset.make_pcset(8, 11, 6), 
                pitch.PitchClass(2), pcset.make_pcset(0, 8, 4), pitch.PitchClass(9), pcset.make_pcset(4, 5, 6), 
                pitch.PitchClass(1)],
                [pitch.PitchClass(4), pcset.make_pcset(0, 8, 11), pitch.PitchClass(6), pcset.make_pcset(2, 10, 5), 
                pitch.PitchClass(8), pcset.make_pcset(1, 2, 9), pitch.PitchClass(4), pcset.make_pcset(0, 3, 8), 
                pitch.PitchClass(5)],
                [pitch.PitchClass(0), pcset.make_pcset(1, 3, 7), pitch.PitchClass(8), pcset.make_pcset(1, 5, 9), 
                pitch.PitchClass(10), pcset.make_pcset(11, 3, 7), pitch.PitchClass(5), pcset.make_pcset(1, 6, 9), 
                pitch.PitchClass(3)],
                [pitch.PitchClass(10), pcset.make_pcset(8, 3, 6), pitch.PitchClass(2), pcset.make_pcset(11, 4, 7), 
                pitch.PitchClass(3), pcset.make_pcset(8, 4, 9), pitch.PitchClass(1), pcset.make_pcset(2, 5, 11), 
                pitch.PitchClass(9)],
                [pitch.PitchClass(8), pcset.make_pcset(9, 2, 6), pitch.PitchClass(1), pcset.make_pcset(0, 8, 4), 
                pitch.PitchClass(10), pcset.make_pcset(0, 2, 6), pitch.PitchClass(7), pcset.make_pcset(3, 4, 11), 
                pitch.PitchClass(2)],
                [pitch.PitchClass(3), pcset.make_pcset(8, 11, 7), pitch.PitchClass(1), pcset.make_pcset(9, 4, 5), 
                pitch.PitchClass(7), pcset.make_pcset(10, 2, 3), pitch.PitchClass(9), pcset.make_pcset(1, 5, 10), 
                pitch.PitchClass(8)]
        ],
        [
                [pitch.PitchClass(0), pcset.make_pcset(8, 2, 4, 7), pitch.PitchClass(1), pcset.make_pcset(8, 9, 4, 5), 
                pitch.PitchClass(11), pcset.make_pcset(2, 4, 7, 8), pitch.PitchClass(6), pcset.make_pcset(1, 3, 8, 10), 
                pitch.PitchClass(2)],
                [pitch.PitchClass(9), pcset.make_pcset(11, 1, 10, 3), pitch.PitchClass(6), pcset.make_pcset(11, 2, 10, 7), 
                pitch.PitchClass(4), pcset.make_pcset(5, 9, 10, 11), pitch.PitchClass(1), pcset.make_pcset(0, 4, 6, 11), 
                pitch.PitchClass(8)],
                [pitch.PitchClass(4), pcset.make_pcset(1, 11, 5, 9), pitch.PitchClass(10), pcset.make_pcset(0, 11, 3, 7), 
                pitch.PitchClass(5), pcset.make_pcset(1, 3, 8, 11), pitch.PitchClass(4), pcset.make_pcset(0, 1, 7, 9), 
                pitch.PitchClass(5)],
                [pitch.PitchClass(2), pcset.make_pcset(8, 3, 4, 6), pitch.PitchClass(11), pcset.make_pcset(1, 4, 5, 6), 
                pitch.PitchClass(9), pcset.make_pcset(2, 3, 4, 6), pitch.PitchClass(10), pcset.make_pcset(2, 5, 7, 9), 
                pitch.PitchClass(1)],
                [pitch.PitchClass(8), pcset.make_pcset(0, 10, 11, 4), pitch.PitchClass(5), pcset.make_pcset(0, 8, 3, 9), 
                pitch.PitchClass(1), pcset.make_pcset(0, 4, 6, 9), pitch.PitchClass(2), pcset.make_pcset(3, 4, 7, 11), 
                pitch.PitchClass(9)],
                [pitch.PitchClass(3), pcset.make_pcset(10, 5, 6, 7), pitch.PitchClass(1), pcset.make_pcset(2, 11, 5, 6), 
                pitch.PitchClass(9), pcset.make_pcset(2, 3, 8, 10), pitch.PitchClass(6), pcset.make_pcset(1, 3, 8, 11), 
                pitch.PitchClass(7)]
        ]
    ],
    [
        [
                [pitch.PitchClass(4), pcset.make_pcset(0, 10), pitch.PitchClass(3), pcset.make_pcset(11, 7), 
                pitch.PitchClass(8), pcset.make_pcset(9, 1), pitch.PitchClass(4), pcset.make_pcset(10, 3), 
                pitch.PitchClass(6)],
                [pitch.PitchClass(1), pcset.make_pcset(8, 4), pitch.PitchClass(9), pcset.make_pcset(2, 6), 
                pitch.PitchClass(10), pcset.make_pcset(0, 4), pitch.PitchClass(3), pcset.make_pcset(11, 6), 
                pitch.PitchClass(5)],
                [pitch.PitchClass(0), pcset.make_pcset(9, 2), pitch.PitchClass(8), pcset.make_pcset(10, 11), 
                pitch.PitchClass(4), pcset.make_pcset(9, 5), pitch.PitchClass(0), pcset.make_pcset(3, 7), 
                pitch.PitchClass(11)],
                [pitch.PitchClass(8), pcset.make_pcset(0, 1), pitch.PitchClass(5), pcset.make_pcset(2, 4), 
                pitch.PitchClass(10), pcset.make_pcset(6, 7), pitch.PitchClass(0), pcset.make_pcset(1, 5), 
                pitch.PitchClass(9)],
                [pitch.PitchClass(6), pcset.make_pcset(10, 4), pitch.PitchClass(9), pcset.make_pcset(0, 5), 
                pitch.PitchClass(11), pcset.make_pcset(3, 4), pitch.PitchClass(8), pcset.make_pcset(9, 5), 
                pitch.PitchClass(1)]
        ],
        [
                [pitch.PitchClass(2), pcset.make_pcset(1, 9, 7), pitch.PitchClass(6), pcset.make_pcset(10, 2, 11), 
                pitch.PitchClass(8), pcset.make_pcset(0, 9, 2), pitch.PitchClass(4), pcset.make_pcset(2, 7, 11), 
                pitch.PitchClass(3)],
                [pitch.PitchClass(1), pcset.make_pcset(0, 8, 6), pitch.PitchClass(4), pcset.make_pcset(1, 9, 7), 
                pitch.PitchClass(5), pcset.make_pcset(1, 10, 6), pitch.PitchClass(0), pcset.make_pcset(1, 4, 8), 
                pitch.PitchClass(11)],
                [pitch.PitchClass(8), pcset.make_pcset(9, 2, 4), pitch.PitchClass(1), pcset.make_pcset(3, 10, 2), 
                pitch.PitchClass(6), pcset.make_pcset(0, 1, 4), pitch.PitchClass(8), pcset.make_pcset(2, 5, 10), 
                pitch.PitchClass(6)],
                [pitch.PitchClass(6), pcset.make_pcset(8, 2, 10), pitch.PitchClass(1), pcset.make_pcset(9, 2, 5), 
                pitch.PitchClass(0), pcset.make_pcset(2, 11, 6), pitch.PitchClass(7), pcset.make_pcset(3, 4, 11), 
                pitch.PitchClass(1)],
                [pitch.PitchClass(10), pcset.make_pcset(1, 5, 6), pitch.PitchClass(0), pcset.make_pcset(8, 3, 4), 
                pitch.PitchClass(6), pcset.make_pcset(2, 10, 5), pitch.PitchClass(0), pcset.make_pcset(3, 10, 11), 
                pitch.PitchClass(7)]
        ],
        [
                [pitch.PitchClass(10), pcset.make_pcset(8, 9, 3, 6), pitch.PitchClass(2), pcset.make_pcset(1, 10, 5, 7), 
                pitch.PitchClass(9), pcset.make_pcset(0, 5, 7, 8), pitch.PitchClass(3), pcset.make_pcset(6, 7, 8, 11), 
                pitch.PitchClass(1)],
                [pitch.PitchClass(8), pcset.make_pcset(1, 11, 4, 5), pitch.PitchClass(3), pcset.make_pcset(0, 9, 11, 4), 
                pitch.PitchClass(7), pcset.make_pcset(1, 2, 3, 11), pitch.PitchClass(8), pcset.make_pcset(1, 3, 5, 10), 
                pitch.PitchClass(9)],
                [pitch.PitchClass(4), pcset.make_pcset(10, 3, 5, 7), pitch.PitchClass(11), pcset.make_pcset(8, 3, 6, 7), 
                pitch.PitchClass(1), pcset.make_pcset(4, 7, 9, 11), pitch.PitchClass(0), pcset.make_pcset(1, 4, 8, 10), 
                pitch.PitchClass(5)],
                [pitch.PitchClass(0), pcset.make_pcset(1, 4, 6, 9), pitch.PitchClass(2), pcset.make_pcset(8, 1, 10, 3), 
                pitch.PitchClass(6), pcset.make_pcset(0, 1, 7, 8), pitch.PitchClass(4), pcset.make_pcset(1, 2, 6, 9), 
                pitch.PitchClass(10)],
                [pitch.PitchClass(5), pcset.make_pcset(0, 1, 6, 7), pitch.PitchClass(9), pcset.make_pcset(0, 11, 3, 4), 
                pitch.PitchClass(7), pcset.make_pcset(2, 4, 6, 11), pitch.PitchClass(8), pcset.make_pcset(1, 2, 6, 10), 
                pitch.PitchClass(3)]
        ]
    ],
    [
        [
                [pitch.PitchClass(6), pcset.make_pcset(9, 10), pitch.PitchClass(4), pcset.make_pcset(0, 8), 
                pitch.PitchClass(11), pcset.make_pcset(2, 6), pitch.PitchClass(7), pcset.make_pcset(1, 5), 
                pitch.PitchClass(8)],
                [pitch.PitchClass(3), pcset.make_pcset(11, 4), pitch.PitchClass(8), pcset.make_pcset(9, 1), 
                pitch.PitchClass(5), pcset.make_pcset(11, 3), pitch.PitchClass(0), pcset.make_pcset(10, 6), 
                pitch.PitchClass(1)],
                [pitch.PitchClass(2), pcset.make_pcset(8, 9), pitch.PitchClass(0), pcset.make_pcset(3, 7), 
                pitch.PitchClass(1), pcset.make_pcset(8, 9), pitch.PitchClass(4), pcset.make_pcset(3, 7), 
                pitch.PitchClass(11)],
                [pitch.PitchClass(8), pcset.make_pcset(0, 3), pitch.PitchClass(7), pcset.make_pcset(11, 5), 
                pitch.PitchClass(4), pcset.make_pcset(0, 1), pitch.PitchClass(6), pcset.make_pcset(10, 2), 
                pitch.PitchClass(7)]
        ],
        [
                [pitch.PitchClass(1), pcset.make_pcset(9, 2, 7), pitch.PitchClass(6), pcset.make_pcset(8, 10, 11), 
                pitch.PitchClass(2), pcset.make_pcset(0, 8, 4), pitch.PitchClass(9), pcset.make_pcset(1, 4, 5), 
                pitch.PitchClass(6)],
                [pitch.PitchClass(8), pcset.make_pcset(1, 3, 7), pitch.PitchClass(11), pcset.make_pcset(2, 10, 6), 
                pitch.PitchClass(8), pcset.make_pcset(1, 4, 9), pitch.PitchClass(2), pcset.make_pcset(3, 4, 11), 
                pitch.PitchClass(7)],
                [pitch.PitchClass(2), pcset.make_pcset(9, 3, 5), pitch.PitchClass(10), pcset.make_pcset(3, 11, 7), 
                pitch.PitchClass(0), pcset.make_pcset(2, 10, 6), pitch.PitchClass(5), pcset.make_pcset(0, 1, 9), 
                pitch.PitchClass(3)],
                [pitch.PitchClass(10), pcset.make_pcset(8, 1, 6), pitch.PitchClass(2), pcset.make_pcset(0, 1, 5), 
                pitch.PitchClass(9), pcset.make_pcset(10, 2, 7), pitch.PitchClass(3), pcset.make_pcset(5, 6, 9), 
                pitch.PitchClass(1)]
        ],
        [
                [pitch.PitchClass(9), pcset.make_pcset(1, 10, 11, 5), pitch.PitchClass(4), pcset.make_pcset(0, 9, 2, 5), 
                pitch.PitchClass(8), pcset.make_pcset(1, 4, 7, 11), pitch.PitchClass(9), pcset.make_pcset(2, 4, 6, 10),
                 pitch.PitchClass(11)],
                [pitch.PitchClass(5), pcset.make_pcset(0, 9, 3, 7), pitch.PitchClass(8), pcset.make_pcset(11, 3, 4, 7), 
                pitch.PitchClass(1), pcset.make_pcset(3, 5, 8, 9), pitch.PitchClass(2), pcset.make_pcset(0, 7, 8, 9), 
                pitch.PitchClass(4)],
                [pitch.PitchClass(11), pcset.make_pcset(8, 4, 5, 6), pitch.PitchClass(0), pcset.make_pcset(8, 9, 2, 4), 
                pitch.PitchClass(7), pcset.make_pcset(0, 3, 8, 10), pitch.PitchClass(6), pcset.make_pcset(2, 4, 7, 11), 
                pitch.PitchClass(10)],
                [pitch.PitchClass(6), pcset.make_pcset(10, 3, 5, 7), pitch.PitchClass(1), pcset.make_pcset(9, 4, 5, 6), 
                pitch.PitchClass(11), pcset.make_pcset(0, 4, 5, 10), pitch.PitchClass(8), pcset.make_pcset(3, 6, 10, 11), 
                pitch.PitchClass(2)]
        ]
    ],
    [
        [
                [pitch.PitchClass(1), pcset.make_pcset(2, 5), pitch.PitchClass(7), pcset.make_pcset(3, 11), 
                pitch.PitchClass(10), pcset.make_pcset(2, 5), pitch.PitchClass(9), pcset.make_pcset(8, 3), 
                pitch.PitchClass(11)],
                [pitch.PitchClass(6), pcset.make_pcset(10, 11), pitch.PitchClass(3), pcset.make_pcset(8, 4), 
                pitch.PitchClass(0), pcset.make_pcset(2, 6), pitch.PitchClass(5), pcset.make_pcset(11, 4), 
                pitch.PitchClass(7)],
                [pitch.PitchClass(2), pcset.make_pcset(1, 5), pitch.PitchClass(7), pcset.make_pcset(0, 6), 
                pitch.PitchClass(4), pcset.make_pcset(8, 1), pitch.PitchClass(9), pcset.make_pcset(10, 2), 
                pitch.PitchClass(6)]
        ],
        [
                [pitch.PitchClass(1), pcset.make_pcset(0, 8, 5), pitch.PitchClass(7), pcset.make_pcset(3, 1, 11), 
                pitch.PitchClass(4), pcset.make_pcset(0, 8, 10), pitch.PitchClass(3), pcset.make_pcset(1, 6, 10), 
                pitch.PitchClass(2)],
                [pitch.PitchClass(9), pcset.make_pcset(2, 10, 6), pitch.PitchClass(4), pcset.make_pcset(8, 2, 11), 
                pitch.PitchClass(0), pcset.make_pcset(9, 4, 5), pitch.PitchClass(10), pcset.make_pcset(2, 5, 6), 
                pitch.PitchClass(7)],
                [pitch.PitchClass(2), pcset.make_pcset(0, 8, 3), pitch.PitchClass(7), pcset.make_pcset(2, 5, 6), 
                pitch.PitchClass(10), pcset.make_pcset(1, 5, 9), pitch.PitchClass(3), pcset.make_pcset(0, 2, 10), 
                pitch.PitchClass(6)]
        ],
        [
                [pitch.PitchClass(8), pcset.make_pcset(0, 9, 8, 4), pitch.PitchClass(3), pcset.make_pcset(0, 2, 10, 7), 
                pitch.PitchClass(6), pcset.make_pcset(0, 2, 4, 9), pitch.PitchClass(5), pcset.make_pcset(3, 4, 8, 10), 
                pitch.PitchClass(0)],
                [pitch.PitchClass(0), pcset.make_pcset(2, 11, 4, 7), pitch.PitchClass(10), pcset.make_pcset(1, 5, 9, 7), 
                pitch.PitchClass(2), pcset.make_pcset(4, 6, 9, 10), pitch.PitchClass(3), pcset.make_pcset(5, 8, 9, 10), 
                pitch.PitchClass(1)],
                [pitch.PitchClass(7), pcset.make_pcset(0, 1, 11, 6), pitch.PitchClass(3), pcset.make_pcset(1, 2, 10, 6), 
                pitch.PitchClass(8), pcset.make_pcset(0, 1, 5, 11), pitch.PitchClass(3), pcset.make_pcset(1, 6, 9, 10), 
                pitch.PitchClass(5)]
        ]
    ],
    [
        [
                [pitch.PitchClass(2), pcset.make_pcset(1, 10), pitch.PitchClass(8), pcset.make_pcset(0, 4), 
                pitch.PitchClass(3), pcset.make_pcset(11, 6), pitch.PitchClass(10), pcset.make_pcset(2, 4), 
                pitch.PitchClass(5)],
                [pitch.PitchClass(0), pcset.make_pcset(11, 7), pitch.PitchClass(4), pcset.make_pcset(1, 9), 
                pitch.PitchClass(5), pcset.make_pcset(0, 2), pitch.PitchClass(6), pcset.make_pcset(9, 1), 
                pitch.PitchClass(7)]
        ],
        [
                [pitch.PitchClass(5), pcset.make_pcset(8, 1, 7), pitch.PitchClass(0), pcset.make_pcset(8, 3, 4), 
                pitch.PitchClass(6), pcset.make_pcset(8, 2, 10), pitch.PitchClass(1), pcset.make_pcset(4, 5, 9), 
                pitch.PitchClass(6)],
                [pitch.PitchClass(1), pcset.make_pcset(9, 4, 5), pitch.PitchClass(11), pcset.make_pcset(10, 3, 7), 
                pitch.PitchClass(1), pcset.make_pcset(8, 9, 4), pitch.PitchClass(3), pcset.make_pcset(1, 2, 6), 
                pitch.PitchClass(10)]
        ],
        [
                [pitch.PitchClass(8), pcset.make_pcset(9, 2, 3, 5), pitch.PitchClass(1), pcset.make_pcset(0, 9, 5, 7), 
                pitch.PitchClass(4), pcset.make_pcset(1, 5, 8, 11), pitch.PitchClass(3), pcset.make_pcset(1, 2, 6, 8), 
                pitch.PitchClass(10)],
                [pitch.PitchClass(5), pcset.make_pcset(8, 1, 11, 4), pitch.PitchClass(3), pcset.make_pcset(1, 10, 6, 7), 
                pitch.PitchClass(11), pcset.make_pcset(0, 5, 6, 10), pitch.PitchClass(2), pcset.make_pcset(0, 5, 7, 9), 
                pitch.PitchClass(1)]
        ]
    ]
]

m = array.make_array_chain(m, 3, False)
for i in range(len(m)):
    print(m[i])
