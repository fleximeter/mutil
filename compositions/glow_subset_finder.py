"""
Name: glow_subset_finder.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 11/13/21

This file contains functionality for working with subsets.
"""

import pctheory.pcset as pcset
import pctheory.pitch as pitch

pcsets = [
    [
        [0, 1, 3, 5, 7, 9],
        [1, 5, 6, 7, 9, 10],
        [1, 2, 5, 7, 9, 11],
        [1, 3, 4, 5, 7, 9, 11],
        [0, 2, 3, 4, 8, 11],
        [0, 3, 4, 6, 7, 8, 10],
        [0, 2, 4, 6, 8, 11],
        [0, 2, 4, 5, 8, 10],
        [2, 4, 6, 7, 8, 10, 11],
        [3, 4, 5, 7, 8, 11],
        [2, 3, 5, 6, 7, 11],
        [1, 3, 4, 6, 7, 9, 11],
        [1, 2, 3, 5, 6, 9],
        [2, 5, 6, 8, 9, 10],
        [0, 3, 4, 6, 8, 10]
    ],
    [
        [0, 1, 3, 5, 7, 9, 10],
        [1, 2, 5, 9, 10, 11],
        [1, 3, 4, 5, 7, 8, 11],
        [2, 4, 6, 8, 10, 11],
        [0, 1, 3, 4, 5, 9],
        [1, 3, 5, 6, 7, 9, 10],
        [1, 2, 4, 6, 8, 10],
        [0, 2, 3, 6, 8, 10],
        [0, 2, 3, 5, 7, 9, 11],
        [0, 2, 5, 6, 8, 10],
        [0, 3, 7, 8, 9, 11]
    ],
    [
        [1, 2, 3, 7, 10, 11],
        [0, 1, 3, 5, 7, 8, 9, 11],
        [1, 3, 4, 7, 9, 11],
        [2, 6, 7, 8, 10, 11],
        [0, 1, 3, 5, 6, 7, 9, 10],
        [0, 2, 4, 7, 8, 10],
        [0, 1, 4, 6, 8, 10],
        [2, 3, 4, 6, 7, 9, 10, 11],
        [0, 1, 2, 6, 9, 10],
        [1, 3, 5, 6, 7, 8, 9, 11],
        [2, 3, 5, 7, 9, 11],
        [0, 1, 3, 4, 7, 11],
        [1, 2, 3, 5, 6, 7, 10, 11],
        [1, 3, 5, 7, 8, 11],
        [0, 3, 4, 6, 7, 8],
        [0, 2, 3, 4, 7, 8, 9, 11],
        [0, 1, 4, 8, 9, 10],
        [0, 2, 4, 6, 9, 10],
        [1, 2, 3, 5, 7, 9, 10, 11],
        [0, 1, 5, 8, 9, 11],
        [0, 3, 5, 7, 9, 11],
        [0, 3, 4, 6, 7, 8, 10, 11],
        [1, 3, 5, 8, 9, 11],
        [0, 2, 4, 6, 8, 9],
        [2, 3, 4, 6, 7, 10]
    ],
    [
        [1, 2, 3, 4, 5, 6, 8, 9, 10],
        [0, 4, 7, 8, 10, 11],
        [1, 3, 6, 7, 9, 11],
        [0, 1, 2, 3, 4, 5, 9, 10, 11],
        [0, 2, 3, 6, 10, 11],
        [1, 2, 5, 6, 7, 8, 9, 10, 11],
        [1, 4, 5, 7, 8, 9],
        [0, 1, 2, 3, 7, 8, 9, 10, 11],
        [1, 3, 5, 7, 9, 10]
    ], 
    [
        [1, 2, 3, 5, 6, 7, 8, 10, 11],
        [1, 3, 5, 7, 10, 11],
        [0, 1, 2, 3, 4, 6, 7, 9, 10],
        [0, 1, 2, 4, 5, 8],
        [0, 2, 4, 6, 7, 8, 9, 10, 11],
        [1, 2, 4, 5, 6, 10],
        [0, 1, 3, 4, 5, 6, 7, 9, 10],
        [0, 2, 4, 6, 7, 10],
        [0, 4, 5, 6, 8, 9],
        [3, 6, 7, 9, 10, 11],
        [1, 4, 5, 7, 9, 11],
        [1, 3, 5, 6, 9, 11]
    ]
]

# current section
k = 0


pcsets2 = []
for pc in pcsets[k]:
    pcsets2.append([pitch.PitchClass12(p) for p in pc])
#s = pcset.make_pcset(1, 2, 5, 9, 10, 11)
#s = pcset.make_pcset(1, 3, 4, 5, 7, 8, 11)

for i in range(len(pcsets2)):
    sub = pcset.subsets(set(pcsets2[i]))

    print(pcsets[k][i], "\n")
    filter = pcset.set_class_filter12("[026]", sub)
    print("[026]")
    for i in filter:
        print(i)

    filter = pcset.set_class_filter12("[015]", sub)
    print("\n[015]")
    for i in filter:
        print(i)

    print("\n********************************\n")
