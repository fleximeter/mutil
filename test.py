from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources
import mgen.xml_parse_sc_pbind as sc

scf = sc.read_file("D:\\Documents\\Scores\\Choral\\Above all praise and majesty (Mendelssohn).xml")
pp = sc.parse_parts(scf)
sc.dump_sc_to_file("D:\\Desktop\\test.scd", pp)
