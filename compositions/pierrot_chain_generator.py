"""
File: pierrot_chain_generator.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 1/27/22

This file contains functionality for generating chains.
"""

from pctheory import poset, pitch

# Create all pcs
pc = [pitch.PitchClass(i) for i in range(12)]

# Set-class name lists for use in chain generation
sc_lists = [
    ["(3-3)[014]", "(3-4)[015]", "(3-8)[026]", "(3-11)[037]"],
    ["(4-19)[0148]", "(4-Z15)[0146]", "(4-Z29)[0137]"],
    ["(5-30)[01468]", "(5-Z37)[03458]"],
    ["(6-31)[014579]", "(6-31)[014579]"]
]
chains = poset.generate_chains_weak(pc[0], sc_lists[3], 0.4, 0.2, 1, 0, pc[4])

# Calculate the number of duplicates
chains2 = []
[chains2.append(c) for c in chains if c not in chains2]
print(f"{len(chains)} chains total")
print(f"{len(chains) - len(chains2)} duplicates")

# Print the chains
for chain in chains:
    print(chain)
