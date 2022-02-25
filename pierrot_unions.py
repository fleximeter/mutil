"""
Name: pierrot_unions.py
Author: Jeff Martin
Description:
This file takes four trichords and generates all possible set-class unions of these chords. It creates a MusicXML file.
"""

from pctheory import group, pcseg, pcset, pitch, set_complex, tables, transformations
from mgen import xml_gen
import music21

google_drive = "H:\\My Drive"

sets = {
    "s": [pcset.make_pcset(0, 1, 4)],  # (3-3)[014]
    "t": [pcset.make_pcset(0, 1, 5)],  # (3-4)[015]
    "u": [pcset.make_pcset(0, 2, 6)],  # (3-8)[026]
    "v": [pcset.make_pcset(0, 3, 7)]  # (3-11)[037]
}

tn = transformations.get_ttos(transformations.OperatorType.Tn)
tni = transformations.get_ttos(transformations.OperatorType.TnI)
x = tables.create_tables()
sc = pcset.SetClass(x)

# Holds unions
unions = {
    "st": set(),
    "su": set(),
    "sv": set(),
    "tu": set(),
    "tv": set(),
    "uv": set(),
    "stu": set(),
    "stv": set(),
    "suv": set(),
    "tuv": set(),
    "stuv": set()
}

# Generate all transformations
for s in sets:
    for i in range(1, 12):
        sets[s].append(tn[i].transform(sets[s][0]))
    for i in range(0, 12):
        sets[s].append(tni[i].transform(sets[s][0]))

for u in unions:
    match(len(u)):
        case 2:
            for s in sets[u[0]]:
                for t in sets[u[1]]:
                    tempset = s.union(t)
                    sc1 = pcset.SetClass(x, tempset)
                    unions[u].add(sc1)
        case 3:
            for s in sets[u[0]]:
                for t in sets[u[1]]:
                    tempset = s.union(t)
                    for v in sets[u[2]]:
                        tempset2 = tempset.union(v)
                        sc1 = pcset.SetClass(x, tempset2)
                        unions[u].add(sc1)
        case 4:
            for s in sets[u[0]]:
                for t in sets[u[1]]:
                    tempset = s.union(t)
                    for v in sets[u[2]]:
                        tempset2 = tempset.union(v)
                        for w in sets[u[3]]:
                            tempset3 = tempset2.union(w)
                            sc1 = pcset.SetClass(x, tempset3)
                            unions[u].add(sc1)


def print_unions():
    for u in unions:
        print(u)
        s = list(unions[u])
        s.sort()
        for n in s:
            print(n.name_morris)
        print("*************************************")


def make_score():
    score = xml_gen.create_score("Pierrot 0.1.0", "Jeffrey Martin")
    xml_gen.add_instrument(score, "Clarinet", "Cl.")

    # Make chords
    s_list = []
    lyrics = [["(3-3)[014]", "s", "[3101100]"], ["(3-4)[015]", "t", "[3100110]"], ["(3-8)[026]", "u", "[3010101]"],
              ["(3-11)[037]", "v", "[3001110]"]]
    used_sc = set()
    for s in sets:
        ps = []
        for pc in sets[s][0]:
            ps.append(pitch.Pitch(pc.pc + 4))
        s_list.append(ps)
    for i in range(4, 13):
        for u in unions:
            for s in unions[u]:
                if len(s) == i:
                    ps = []
                    for pc in s.pcset:
                        ps.append(pitch.Pitch(pc.pc + 4))
                    if s.name_forte not in used_sc:
                        s_list.append(ps)
                        used_sc.add(s.name_forte)
                        lyrics.append([s.name_morris, u, s.ic_vector_string])
                    else:
                        j = s_list.index(ps)
                        lyrics[j][1] += "," + u

    chords = xml_gen.make_music21_list(s_list, [4.0 for item in s_list])
    xml_gen.add_measures(score, len(s_list), meter="4/4")
    xml_gen.add_item(score[1], music21.clef.TrebleClef(), 1)
    xml_gen.add_sequence(score[1], chords, lyrics)
    xml_gen.export_to_xml(score, google_drive + "\\Composition\\Dorico\\Pierrot Piece\\pierrot.xml")


if __name__ == "__main__":
    make_score()
