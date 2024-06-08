"""
File: test.py
"""

import mgen.algorithms as algorithms

z = algorithms.NoteEnvelope([(0, 12), (0, 24), (12, 36)], [0, 15, 30])
print(z(19))
