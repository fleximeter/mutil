from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

pc = pcseg.make_pcseg12(4,8,2,1,9,5,6)
dc = pcseg.make_pcseg12(5,3,1,6,0,8,9)
mx = pcseg.InvarianceMatrix("T", pc, dc)
mx.print([pitch.PitchClass12(6)])
