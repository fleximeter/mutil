"""
File: norgard.py
Author: Jeff Martin
Date: 11/13/21
"""

import mgen.xml_gen as xml_gen
from ..pctheory.util import util


if __name__ == "__main__":
    gmap = {0: 9, 1: 11, 2: 12, 3: 14, 4: 16, 5: 18, 6: 19}
    n100 = util.norgard(400)
    pseq = util.map_to_chromatic(gmap, n100)
    s = xml_gen.create_score()
    xml_gen.add_instrument(s, "Violin", "Vln.")
    xml_gen.add_measures(s, 100, 1, 1, "4/4")
    xml_gen.add_sequence(s[1], xml_gen.make_music21_list(pseq, [1 for i in range(len(pseq))]))
    xml_gen.export_to_xml(s, r"H:\My Drive\Composition\Dorico\draft10.xml")
