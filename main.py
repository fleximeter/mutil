from mgen import xml_parse_sc_pbind
import os

DIR = "G:\\My Drive\\Dorico Scores\\Songs\\XML"
FILE = "Maamme - Full score - 01 Flow 1.musicxml"
with open(os.path.join(DIR, "ji.scd"), 'w') as outfile:
    outfile.write(xml_parse_sc_pbind.dump_sc_with_tuning(
            xml_parse_sc_pbind.parse_parts(xml_parse_sc_pbind.read_file(os.path.join(DIR, FILE))),
            69
        )
    )
with open(os.path.join(DIR, "et.scd"), 'w') as outfile:
    outfile.write(xml_parse_sc_pbind.dump_sc(
            xml_parse_sc_pbind.parse_parts(xml_parse_sc_pbind.read_file(os.path.join(DIR, FILE))),
        )
    )