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
    score = xml_gen.create_score("Clarinet Piece Draft 0.1.2", "Jeffrey Martin")
    xml_gen.add_instrument(score, "Clarinet", "Cl.")

    # Make the pitch sets
    pset_list = []
    root_subset_classes_list = list(root_subset_classes)
    root_subset_classes_list.sort()
    for subset_class in root_subset_classes_list:
        chord_pset = [pitch.Pitch24(pc.pc) for pc in subset_class.pcset]
        pset_list.append(chord_pset)
    
    # Make the lyrics and music21 chords
    lyrics = [[subset_class.name_prime, subset_class.ic_vector_str] for subset_class in root_subset_classes_list]
    chords = xml_gen.make_music21_list(pset_list, [4.0 for item in pset_list])
    
    # Generate a score
    xml_gen.add_measures(score, len(pset_list), meter="4/4")
    xml_gen.add_item(score[1], music21.clef.TrebleClef(), 1)
    xml_gen.add_sequence(score[1], chords, lyrics)
    xml_gen.export_to_xml(score, "D:\\Compositions\\clarinet_piece\\clarinet_0.1.2.xml")


if __name__ == "__main__":
    make_score()
