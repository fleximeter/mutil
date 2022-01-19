"""
Name: orchestra_piece.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 9/25/21

This file contains functions for creating drafts of an orchestra piece.
"""

import music21
import mgen.xml_gen as xml_gen
import pctheory.pitch as pitch


# The chords to use (in order)
pcsets = ({0, 1, 3, 5, 7, 9},
          {1, 5, 6, 7, 9, 10},
          {1, 2, 5, 7, 9, 11},
          {1, 3, 4, 5, 7, 9, 11},
          {0, 2, 3, 4, 8, 11},
          {0, 3, 4, 6, 7, 8, 10},
          {0, 2, 4, 6, 8, 11},
          {0, 2, 4, 5, 8, 10},
          {2, 4, 6, 7, 8, 10, 11},
          {3, 4, 5, 7, 8, 11},
          {2, 3, 5, 6, 7, 11},
          {1, 3, 4, 6, 7, 9, 11},
          {1, 2, 3, 5, 6, 9},
          {2, 5, 6, 8, 9, 10},
          {0, 3, 4, 6, 8, 10},
          {0, 1, 3, 5, 7, 9, 10},
          {1, 2, 5, 9, 10, 11},
          {1, 3, 4, 5, 7, 8, 11},
          {2, 4, 6, 8, 10, 11},
          {0, 1, 3, 4, 5, 9},
          {1, 3, 5, 6, 7, 9, 10},
          {1, 2, 4, 6, 8, 10},
          {0, 2, 3, 6, 8, 10},
          {0, 2, 3, 5, 7, 9, 11},
          {0, 2, 5, 6, 8, 10},
          {0, 3, 7, 8, 9, 11},
          {1, 2, 3, 7, 10, 11},
          {0, 1, 3, 5, 7, 8, 9, 11},
          {1, 3, 4, 7, 9, 11},
          {2, 6, 7, 8, 10, 11},
          {0, 1, 3, 5, 6, 7, 9, 10},
          {0, 2, 4, 7, 8, 10},
          {0, 1, 4, 6, 8, 10},
          {2, 3, 4, 6, 7, 9, 10, 11},
          {0, 1, 2, 6, 9, 10},
          {1, 3, 5, 6, 7, 8, 9, 11},
          {2, 3, 5, 7, 9, 11},
          {0, 1, 3, 4, 7, 11},
          {1, 2, 3, 5, 6, 7, 10, 11},
          {1, 3, 5, 7, 8, 11},
          {0, 3, 4, 6, 7, 8},
          {0, 2, 3, 4, 7, 8, 9, 11},
          {0, 1, 4, 8, 9, 10},
          {0, 2, 4, 6, 9, 10},
          {1, 2, 3, 5, 7, 9, 10, 11},
          {0, 1, 5, 8, 9, 11},
          {0, 3, 5, 7, 9, 11},
          {0, 3, 4, 6, 7, 8, 10, 11},
          {1, 3, 5, 8, 9, 11},
          {0, 2, 4, 6, 8, 9},
          {2, 3, 4, 6, 7, 10},
          {1, 2, 3, 4, 5, 6, 8, 9, 10},
          {0, 4, 7, 8, 10, 11},
          {1, 3, 6, 7, 9, 11},
          {0, 1, 2, 3, 4, 5, 9, 10, 11},
          {0, 2, 3, 6, 10, 11},
          {1, 2, 5, 6, 7, 8, 9, 10, 11},
          {1, 4, 5, 7, 8, 9},
          {0, 1, 2, 3, 7, 8, 9, 10, 11},
          {1, 3, 5, 7, 9, 10},
          {1, 2, 3, 5, 6, 7, 8, 10, 11},
          {1, 3, 5, 7, 10, 11},
          {0, 1, 2, 3, 4, 6, 7, 9, 10},
          {0, 1, 2, 4, 5, 8},
          {0, 2, 4, 6, 7, 8, 9, 10, 11},
          {1, 2, 4, 5, 6, 10},
          {0, 1, 3, 4, 5, 6, 7, 9, 10},
          {0, 2, 4, 6, 7, 10},
          {0, 4, 5, 6, 8, 9},
          {3, 6, 7, 9, 10, 11},
          {1, 4, 5, 7, 9, 11},
          {1, 3, 5, 6, 9, 11}
          )

# The pcset names corresponding to the chords
set_names = (
        "{013579}", "{15679A}", "{12579B}", "{134579B}", "{02348B}", "{034678A}", "{02468B}", "{02458A}",
        "{24678AB}", "{34578B}", "{23567B}", "{134679B}", "{123569}", "{25689A}", "{03468A}", "{013579A}",
        "{1259AB}", "{134578B}", "{2468AB}", "{013459}", "{135679A}", "{12468A}", "{02368A}", "{023579B}",
        "{02568A}", "{03789B}", "{1237AB}", "{0135789B}", "{13479B}", "{2678AB}", "{0135679A}", "{02478A}",
        "{01468A}", "{234679AB}", "{01269A}", "{1356789B}", "{23579B}", "{01347B}", "{123567AB}", "{13578B}",
        "{034678}", "{0234789B}", "{01489A}", "{02469A}", "{123579AB}", "{01589B}", "{03579B}", "{034678AB}",
        "{13589B}", "{024689}", "{23467A}", "{12345689A}", "{0478AB}", "{13679B}", "{0123459AB}", "{0236AB}",
        "{1256789AB}", "{145789}", "{0123459AB}", "{13579A}", "{1235678AB}", "{1357AB}", "{01234679A}", "{012458}",
        "{0246789AB}", "{12456A}", "{01345679A}", "{02467A}", "{045689}", "{3679AB}", "{14579B}", "{13569B}"
)

# Bass pattern indices
lower_names = (
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1",
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"
)

# Chord identifiers
chord_names = (
    "A", "B", "A", "AA", "B", "AB", "A", "A", "AB", "B", "B", "AA", "B", "B", "A", "AA", "B", "AB", "A", "B",
    "AB", "A", "A", "AA", "A", "B", "B", "AA", "A", "B", "AB", "A", "A", "BB", "B", "AA", "A", "B", "AB", "A",
    "B", "BB", "B", "A", "AA", "B", "A", "AB", "A", "A", "B", "AB", "B", "A", "BB", "B", "AB", "B", "BB", "A",
    "AB", "A", "BB", "B", "AB", "B", "BB", "A", "B", "B", "A", "A"
)

# Chord cardinalities
chord_cards = (
    "6", "6", "6", "7", "6", "7", "6", "6", "7", "6", "6", "7", "6", "6", "6", "7", "6", "7", "6", "6", "7",
    "6", "6", "7", "6", "6", "6", "8", "6", "6", "8", "6", "6", "8", "6", "8", "6", "6", "8", "6", "6", "8",
    "6", "6", "8", "6", "6", "8", "6", "6", "6", "9", "6", "6", "9", "6", "9", "6", "9", "6", "9", "6", "9",
    "6", "9", "6", "9", "6", "6", "6", "6", "6",
)

# The bass notes to use
bass = (1, 5, 2, 3, 0, 4, 8, 4, 2, 8, 3, 11, 3, 9, 0, 5, 2, 8, 10, 9, 7, 1, 8, 5, 8, 11, 7, 9, 7, 10, 3, 2, 0, 11, 1, 9,
        9, 1, 6, 11, 8, 0, 4, 0, 10, 9, 11, 8, 5, 8, 10, 1, 4, 7, 0, 10, 8, 5, 9, 3, 11, 3, 4, 8, 10, 2, 6, 6, 4, 3, 5,
        1)


def make_draft():
    """
    Makes an initial draft
    :return:
    """
    s = xml_gen.create_score()
    xml_gen.add_instrument_multi(s, "Piano", "Pno.", 2, "brace", True)
    xml_gen.add_measures(s, 72, 1, 0, "2/4")

    # Add the chords to voice 1
    for i in range(72):
        c = music21.chord.Chord([pc + 60 for pc in pcsets[i]], offset=0, quarterLength=2)
        c.semiClosedPosition(inPlace=True)
        s[1][i].append(c)

    # Add the bass notes to voice 2
    for i in range(72):
        n = music21.note.Note(offset=0, quarterLength=2)
        n.pitches[0].midi = bass[i] + 36
        s[2][i].append(n)

    # s.show()
    xml_gen.export_to_xml(s, r"H:\My Drive\Composition\Dorico\draft.xml")


def make_draft_2():
    """
    Makes a second draft
    :return:
    """
    s = xml_gen.create_score()
    xml_gen.add_instrument_multi(s, "Piano", "Pno.", 2, "brace", True)

    # Add measures for each section
    xml_gen.add_measures(s, 25, 1, None, "4/4")
    xml_gen.add_measures(s, 1, 26, None, "5/4")
    s[1][len(s[1]) - 1].rightBarline = "double"
    s[2][len(s[1]) - 1].rightBarline = "double"
    xml_gen.add_measures(s, 13, 27, None, "4/4")
    xml_gen.add_measures(s, 1, 40, None, "3/4")
    s[1][len(s[1]) - 1].rightBarline = "double"
    s[2][len(s[1]) - 1].rightBarline = "double"
    xml_gen.add_measures(s, 37, 41, None, "4/4")
    xml_gen.add_measures(s, 1, 78, None, "2/4")
    s[1][len(s[1]) - 1].rightBarline = "double"
    s[2][len(s[1]) - 1].rightBarline = "double"
    xml_gen.add_measures(s, 10, 79, None, "4/4")
    xml_gen.add_measures(s, 1, 89, None, "5/4")
    s[1][len(s[1]) - 1].rightBarline = "double"
    s[2][len(s[1]) - 1].rightBarline = "double"
    xml_gen.add_measures(s, 21, 90, None, "4/4")

    # Add tempo markings
    xml_gen.add_item(s[1], music21.tempo.MetronomeMark(None, 60, music21.note.Note(type="quarter")), 1)
    xml_gen.add_item(s[1], music21.tempo.MetronomeMark(None, 120, music21.note.Note(type="quarter")), 41)
    xml_gen.add_item(s[1], music21.tempo.MetronomeMark(None, 60, music21.note.Note(type="quarter")), 79)

    # Add note durations
    durations = []
    for i in range(15):
        durations.append(7)
    for i in range(11):
        durations.append(5)
    for i in range(25):
        durations.append(6)
    for i in range(9):
        durations.append(5)
    for i in range(17):
        durations.append(7)

    # Create the top lyrics
    lyrics_top = [[set_names[i], chord_names[i], chord_cards[i]] for i in range(len(pcsets))]
    pcsets2 = xml_gen.make_music21_list(pcsets, durations)
    for chord in pcsets2:
        xml_gen.make_semi_closed(chord)
    bass2 = [music21.note.Note(p + 24, quarterDuration=durations[i]) for p in bass]
    
    # Add notes
    xml_gen.add_sequence(s[1], pcsets2, lyrics_top, 1, 4, 0)
    xml_gen.add_sequence(s[2], bass2, lower_names, 1, 4, 0)

    # Render the score in MusicXML
    # s.show()
    xml_gen.export_to_xml(s, r"H:\My Drive\Composition\Dorico\draft9.xml")


def make_common_tones():
    """
    Make a list of common tones
    :return:
    """
    intersect = [pcsets[i].intersection(pcsets[i + 1]) for i in range(len(pcsets) - 1)]
    for i in range(len(intersect)):
        print(f"{i+1}. {intersect[i]}")


if __name__ == "__main__":
    make_draft_2()
