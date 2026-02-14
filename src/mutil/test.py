from mutil.algorithms import LindenmayerSystem, Rule
from pctheory.pitch import Pitch
import mutil.mgen.xml_gen as xml_gen
import music21

system = LindenmayerSystem()
system.add_rule(Rule(lambda x: x.pc % 2 == 0 and x.p % 3 < 2, lambda x: [x, x + 1]))
system.add_rule(Rule(lambda x: x.pc % 2 == 1, lambda x: [x, x - 2]))
system.add_rule(Rule(lambda x: x.pc % 2 == 0, lambda x: [x + 3]))
system.set_axiom(Pitch(60))
system.grow(5)
print(system.token_stream)

score = xml_gen.create_score("LSystemScore", "Jeff Martin")
xml_gen.add_instrument(score, "Xylophone", "Xyl.")
xml_gen.add_measures(score, 100, meter="4/4")
xml_gen.add_sequence(score[1], xml_gen.make_music21_list(system.token_stream, [0.5 for _ in range(len(system.token_stream))]))
xml_gen.export_to_xml(score, "data/score.xml")