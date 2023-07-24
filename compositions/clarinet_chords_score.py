"""
Name: clarinet_chords_score.py
Author: Jeff Martin
Date: 12/23/22

Description:
This file generates a MusicXML score of chords and associated information for 
the clarinet piece. This is a generic implementation that could be used in later
pieces - the idea is that you establish a root set-class and extract all subset-
classes from it, remove set-classes with cardinality less than 3, and generate
pitch-sets from the prime forms. Then you generate a MusicXML score with set-class
prime form name and IC vector.
"""

from pctheory import pcset, pitch
from mgen import xml_gen
import music21

# The root set from which subsets are extracted
root_set = pcset.make_pcset24(0, 1, 5, 9, 10, 11, 15, 19)
root_sc = pcset.SetClass24(root_set)
root_subset_classes = root_sc.get_abstract_subset_classes()

# Eliminate all set-classes smaller than trichordal set-classes
items_to_remove = set()
for item in root_subset_classes:
    if len(item) < 3:
        items_to_remove.add(item)
for item in items_to_remove:
    root_subset_classes.remove(item)

def make_score():
    """
    Makes a MusicXML score with information about the set-classes
    """

    # We make two scores - one with all of the chords, and the other
    # with the microtonal chords removed.
    score1 = xml_gen.create_score("Clarinet Piece Draft 0.1.2.1", "Jeffrey Martin")
    xml_gen.add_instrument(score1, "Clarinet", "Cl.")
    score2 = xml_gen.create_score("Clarinet Piece Draft 0.1.2.2", "Jeffrey Martin")
    xml_gen.add_instrument(score2, "Clarinet", "Cl.")

    # Make the pitch sets
    pset_list = []
    root_subset_classes_list = list(root_subset_classes)
    root_subset_classes_list.sort()
    for subset_class in root_subset_classes_list:
        chord_pset = [pitch.Pitch24(pc.pc) for pc in subset_class.pcset]
        pset_list.append(chord_pset)
    
    # Make the lyrics and music21 chords
    lyrics1 = [[subset_class.name_prime, subset_class.ic_vector_str] for subset_class in root_subset_classes_list]
    for i, lyric in enumerate(lyrics1):
        odd = 0
        for pc in root_subset_classes_list[i].pcset:
            if pc.pc % 2:
                odd += 1
        lyric.append(f"{odd}/{len(root_subset_classes_list[i])}")

    chords1 = xml_gen.make_music21_list(pset_list, [4.0 for item in pset_list])
    chords2 = []
    lyrics2 = []
    for i in range(len(root_subset_classes_list)):
        if "0/" in lyrics1[i][2]:
            chords2.append(pset_list[i])
            sc1 = pcset.SetClass12(root_subset_classes_list[i].pcset)
            lyrics2.append([sc1.name_morris, sc1.ic_vector_str])
    chords2 = xml_gen.make_music21_list(chords2, [4.0 for item in chords2])
    
    # Generate a score
    xml_gen.add_measures(score1, len(pset_list), meter="4/4")
    xml_gen.add_item(score1[1], music21.clef.TrebleClef(), 1)
    xml_gen.add_sequence(score1[1], chords1, lyrics1)
    xml_gen.export_to_xml(score1, "D:\\Compositions\\clarinet_piece\\clarinet_0.1.2.1.xml")
    xml_gen.add_measures(score2, len(chords2), meter="4/4")
    xml_gen.add_item(score2[1], music21.clef.TrebleClef(), 1)
    xml_gen.add_sequence(score2[1], chords2, lyrics2)
    xml_gen.export_to_xml(score2, "D:\\Compositions\\clarinet_piece\\clarinet_0.1.2.2.xml")


if __name__ == "__main__":
    make_score()
