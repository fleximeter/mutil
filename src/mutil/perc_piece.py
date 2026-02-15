from mutil.algorithms import LindenmayerSystem, Rule, Range
import mutil.mgen.xml_gen as xml_gen
import music21
from music21.pitch import Pitch
from music21.scale import *

note_system = LindenmayerSystem()
note_system.add_rule(Rule(lambda x: type(x) == int and x % 2 == 0 and x % 3 < 2, lambda x: [x, x + 1]))
note_system.add_rule(Rule(lambda x: type(x) == int and x % 2 == 1, lambda x: [x - 3, x]))
note_system.add_rule(Rule(lambda x: type(x) == int and x % 2 == 0, lambda x: [x, x + 6]))
note_system.add_rule(Rule(lambda x: type(x) == int and x % 2 == 1 and x % 3 > 0, lambda x: [x - 6]))
note_system.add_rule(Rule(lambda x: type(x) == int and x % 3 == 1, lambda x: [x - 1, x]))
note_system.add_rule(Rule(lambda x: type(x) == int and x % 3 == 2, lambda x: [x - 1, x + 1]))
note_system.add_rule(Rule(lambda x: x is None, lambda x: [x]))
note_system.set_axiom(0)
note_system.grow(4)
print(f"Note tokens: {len(note_system.token_stream)}")

rhythm_system = LindenmayerSystem()
rhythm_system.add_rule(Rule(lambda x: x % 2 == 1, lambda x: [x, x, x + 1, x, x]))
rhythm_system.add_rule(Rule(lambda x: x % 2 == 0, lambda x: [x, x - 1]))
rhythm_system.set_axiom(1)
rhythm_system.grow(5)
print(f"Rhythm tokens: {len(rhythm_system.token_stream)}")

# need at least as many durations as notes
assert(len(note_system.token_stream) <= len(rhythm_system.token_stream))

score = xml_gen.create_score("LSystemScore", "Jeff Martin")
part = music21.stream.Part(partName="Xylophone", partAbbreviation="Xyl.")
part.insert(0, music21.instrument.Xylophone())
score.append(part)
xml_gen.add_measures(score, 400, meter="4/4")
xml_gen.add_item(part, music21.tempo.MetronomeMark("Presto", 180), 1)

# need to quantize to a scale
#scale = MajorScale(Pitch('C'))
#scale = ConcreteScale(pitches=['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B-5'])
scale = DorianScale(Pitch('D'))
pitches = scale.getPitches('C5', 'D7')
note_range = Range(0, len(pitches)-1)
tokens = []
for token in note_system.token_stream:
    if token is None:
        tokens.append(token)
    else:
        tokens.append(pitches[note_range.fold(token)])

rhythm_range = Range(1, 4)
#[0.5 for _ in range(len(note_system.token_stream))]
xml_gen.add_sequence(score[1], xml_gen.make_music21_list(tokens, [rhythm_range.wrap(val) * 0.5 for val in rhythm_system.token_stream]))
xml_gen.remove_empty_measures(score)
xml_gen.export_to_xml(score, "data/score.xml")
# score.show()