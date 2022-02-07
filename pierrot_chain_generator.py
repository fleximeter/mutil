"""
File: pierrot_chain_generator.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
Date: 1/27/22

This file contains functionality for generating chains.
"""

from pctheory import pcset, poset, pitch

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
chains = poset.generate_chains_weak(pc[4], sc_lists[2][1], 0.5, 0.5, 0.9, 0.5, pc[3])

# Filter exclusively
chains = poset.filter_poset_positions(chains,
                                      [None,
                                       pcset.make_pcset(3),
                                       None, # pcset.make_pcset(5, 10),
                                       pcset.make_pcset(1, 3),
                                       None, # pcset.make_pcset(1, 9),
                                       pcset.make_pcset(3),
                                       None, # pcset.make_pcset(11, 5),
                                       pcset.make_pcset(11),
                                       None],
                                       True)

# Filter inclusively
chains = poset.filter_poset_positions(chains,
                                      [None,
                                       None,
                                       pcset.make_pcset(0),
                                       None,
                                       pcset.make_pcset(1, 9, 3, 10, 11),
                                       None,
                                       pcset.make_pcset(3, 11, 5, 0, 7, 10),
                                       None,
                                       None])

# Print the chains
print(f"{len(chains)} chains total")
for chain in chains:
    print(chain)
