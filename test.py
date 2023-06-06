from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
from mgen import xml_gen

score1 = xml_gen.create_score("Randomness Testing", "Jeffrey Martin")
xml_gen.add_instrument(score1, "Cello", "Vlc.")

# Create the function for determining range
