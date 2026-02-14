from mutil.algorithms import LindenmayerSystem, Rule
import mutil.mgen.xml_gen as xml_gen
import music21
from music21.pitch import Pitch
from music21.scale import MajorScale

system = LindenmayerSystem()
system.add_rule(Rule(lambda x: x % 2 == 0 and x % 3 < 2, lambda x: [x, x + 1]))
system.add_rule(Rule(lambda x: x % 2 == 1, lambda x: [x, x - 2]))
system.add_rule(Rule(lambda x: x % 2 == 0, lambda x: [x + 3]))
system.set_axiom(60)
system.grow(5)
print(system.token_stream)

score = xml_gen.create_score("LSystemScore", "Jeff Martin")
xml_gen.add_instrument(score, "Xylophone", "Xyl.")
xml_gen.add_measures(score, 100, meter="4/4")

# need to quantize to a scale
scale = MajorScale(Pitch('C'))
tokens = [scale.pitchFromDegree(degree) for degree in system.token_stream]

xml_gen.add_sequence(score[1], xml_gen.make_music21_list(tokens, [0.5 for _ in range(len(system.token_stream))]))
xml_gen.export_to_xml(score, "data/score.xml")