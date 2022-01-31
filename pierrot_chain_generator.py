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
# abcd
# cbad
# adcb
# cdab
core_sc = ["(3-3)[014]", "(3-4)[015]", "(3-8)[026]", "(3-11)[037]"]
sc_lists = [
    [
        ["(4-Z15)[0146]", "(4-19)[0148]", "(4-20)[0158]", "(4-Z29)[0137]"],
        ["(4-20)[0158]", "(4-19)[0148]", "(4-Z15)[0146]", "(4-Z29)[0137]"],
        ["(4-Z15)[0146]", "(4-Z29)[0137]", "(4-20)[0158]", "(4-19)[0148]"],
        ["(4-20)[0158]", "(4-Z29)[0137]", "(4-Z15)[0146]", "(4-19)[0148]"]
    ],
    [
        ["(5-20)[01568]", "(5-26)[02458]", "(5-30)[01468]", "(5-Z37)[03458]"],
        ["(5-30)[01468]", "(5-26)[02458]", "(5-20)[01568]", "(5-Z37)[03458]"],
        ["(5-20)[01568]", "(5-Z37)[03458]", "(5-30)[01468]", "(5-26)[02458]"],
        ["(5-30)[01468]", "(5-Z37)[03458]", "(5-20)[01568]", "(5-26)[02458]"],
    ],
    [
        ["(6-Z17)[012478]", "(6-31)[014579]", "(6-Z46)[012469]", "(6-Z48)[012579]"],
        ["(6-Z46)[012469]", "(6-31)[014579]", "(6-Z17)[012478]", "(6-Z48)[012579]"],
        ["(6-Z17)[012478]", "(6-Z48)[012579]", "(6-Z46)[012469]", "(6-31)[014579]"],
        ["(6-Z46)[012469]", "(6-Z48)[012579]", "(6-Z17)[012478]", "(6-31)[014579]"],
    ]
]
chains = poset.generate_chains_weak(pc[2], sc_lists[0][0], 0.3, 0.2, 0.8, 0, pc[10])
chains = poset.filter_poset_positions(chains,
                                      [None,
                                       None, # {pc[0], pc[1], pc[2], pc[5], pc[6], pc[9], pc[11]},
                                       {pc[1], pc[3], pc[5], pc[7]},
                                       None, # {pc[1], pc[3], pc[4], pc[5], pc[6], pc[7], pc[10]},
                                       {pc[6], pc[10], pc[11]},
                                       None, # {pc[0], pc[1], pc[4], pc[6], pc[7], pc[9], pc[11]},
                                       {pc[2], pc[7]},
                                       None, # {pc[0], pc[1], pc[5], pc[6], pc[8], pc[11]},
                                       None])

# Calculate the number of duplicates
chains2 = []
[chains2.append(c) for c in chains if c not in chains2]
print(f"{len(chains)} chains total")
print(f"{len(chains) - len(chains2)} duplicates")

# Print the chains
for chain in chains:
    print(chain)
