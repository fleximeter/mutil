from mutil.algorithms import LindenmayerSystem, Rule, Range
import mutil.mgen.xml_gen as xml_gen
import music21
from music21.pitch import Pitch
from music21.scale import *

system = LindenmayerSystem()
system.add_rule(Rule(lambda x: x % 2 == 0 and x % 3 < 2, lambda x: [x, x + 1]))
system.add_rule(Rule(lambda x: x % 2 == 1, lambda x: [x, x - 2]))
system.add_rule(Rule(lambda x: x % 2 == 0, lambda x: [x + 6]))
system.add_rule(Rule(lambda x: x % 2 == 1 and x % 3 > 0, lambda x: [x - 6]))
system.add_rule(Rule(lambda x: x % 3 == 1, lambda x: [x - 1, x]))
system.add_rule(Rule(lambda x: x % 3 == 2, lambda x: [x + 1, x]))
system.set_axiom(0)
system.grow(5)
print(system.token_stream)

score = xml_gen.create_score("LSystemScore", "Jeff Martin")
xml_gen.add_instrument(score, "Xylophone", "Xyl.")
xml_gen.add_measures(score, 200, meter="4/4")

# need to quantize to a scale
#scale = MajorScale(Pitch('C'))
#scale = ConcreteScale(pitches=['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B-5'])
scale = DorianScale(Pitch('D'))
pitches = scale.getPitches('F4', 'D7')
r = Range(0, len(pitches)-1)
tokens = [pitches[r.fold(degree+14)] for degree in system.token_stream]

xml_gen.add_sequence(score[1], xml_gen.make_music21_list(tokens, [0.5 for _ in range(len(system.token_stream))]))
xml_gen.remove_empty_measures(score)
xml_gen.export_to_xml(score, "data/score.xml")
score.show()