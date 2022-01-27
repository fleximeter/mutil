"""
File: pierrot_chain_generator.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 1/27/22

This file contains functionality for generating chains.
"""

from pctheory import pcseg, pitch

pc = pitch.PitchClass(9)
chains = pcseg.make_chain_weak(pc, ["[015]", "[014]", "[026]", "[037]"], 0.4, 0.4)
chains = pcseg.make_chain_weak(pc, ["[0148]", "[0146]", "[0137]"], 0.4, 0.2)

chains2 = []
[chains2.append(c) for c in chains if c not in chains2]
print(f"{len(chains)} chains total")
print(f"{len(chains) - len(chains2)} duplicates")

for chain in chains:
    print(chain)
