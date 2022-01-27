"""
File: pierrot_subset_finder.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 1/26/22

This file contains functionality for working with subsets.
Testing to see if this comment pushes.
"""

import pctheory.pcset as pcset
import pctheory.pitch as pitch
import pctheory.tables as tables

t = tables.create_tables()
sc = pcset.SetClass(t)
pcsets = []

# Get a pcset from the user
user_input = str(input("Enter a pcset: "))
user_input = user_input.split("{")
if len(user_input) > 1:
    user_input[1] = user_input[1].strip(" }")
    pcset1 = set()
    for char in user_input[1]:
        pcset1.add(pitch.PitchClass(t["hexToInt"][char]))
    pcsets.append(pcset1)

# Print the filtered results
for i in range(len(pcsets)):
    sub = pcset.subsets(pcsets[i])
    sc.pcset = pcsets[i]
    filters = ["(3-3)[014]", "(3-4)[015]", "(3-8)[026]", "(3-11)[037]"]
    print(f"{sc.name_morris}: {pcsets[i]}\n")
    for j in range(len(filters)):
        filtered = pcset.set_class_filter(filters[j], sub)
        print(filters[j])
        for ps in filtered:
            print(ps)
        print()
    print("********************************\n")
