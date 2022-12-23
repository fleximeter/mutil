"""
Name: clarinet_chords_score.py
Author: Jeff Martin
Date: 12/23/22

Description:
This file generates a MusicXML score of chords and associated information for 
the clarinet piece.
"""

from pctheory import group, pcseg, pcset, pitch, set_complex, tables, transformations
from mgen import xml_gen
import music21

google_drive = "H:\\My Drive"

# The root set from which subsets are extracted
root_set = pcset.make_pcset24(0, 1, 5, 9, 10, 11, 15, 19)
sc = pcset.SetClass24(root_set)
sub = sc.get_abstract_subset_classes()

# Make the Tn/TnI group that maps U_e and U_o to themselves
"""
utos_clarinet = {}
utos_clarinet_list = []
for i in range(0, 24, 2):
    utos_clarinet[f"T{i}"] = transformations.UTO(i)
    utos_clarinet[f"T{i}I"] = transformations.UTO(i, 23)
for u in utos_clarinet:
    utos_clarinet_list.append(utos_clarinet[u])
grp = group.OperatorGroup(utos_clarinet_list, 24)
"""

# Eliminate all set-classes smaller than trichordal set-classes
items_to_remove = set()
for item in sub:
    if len(item) < 3:
        items_to_remove.add(item)
for item in items_to_remove:
    sub.remove(item)

def make_score():
    score = xml_gen.create_score("Clarinet Piece Draft 0.1.2", "Jeffrey Martin")
    xml_gen.add_instrument(score, "Clarinet", "Cl.")

    # Make chords
    chord_list = []
    # lyrics = [["(3-3)[014]", "s", "[3101100]"], ["(3-4)[015]", "t", "[3100110]"], ["(3-8)[026]", "u", "[3010101]"],
    #           ["(3-11)[037]", "v", "[3001110]"]]
    sub_list = list(sub)
    sub_list.sort()
    for s in sub_list:
        ps = [pitch.Pitch12(pc.pc) for pc in s.pcset]
        chord_list.append(ps)
    
    chords = xml_gen.make_music21_list(chord_list, [4.0 for item in chord_list])
    xml_gen.add_measures(score, len(chord_list), meter="4/4")
    xml_gen.add_item(score[1], music21.clef.TrebleClef(), 1)
    xml_gen.add_sequence(score[1], chords)
    xml_gen.export_to_xml(score, "D:\\Compositions\\clarinet_piece\\clarinet_0.1.2.xml")


if __name__ == "__main__":
    make_score()
