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
chains = poset.generate_chains_weak(pc[0], sc_lists[2][0], 0.4, 0.2, 1, 0, pc[2])

"""
chains = poset.filter_poset_positions(chains,
                                      [None,
                                       None,
                                       pcset.make_pcset(1, 3, 5, 7),
                                       None,
                                       pcset.make_pcset(6, 10, 11),
                                       None,
                                       pcset.make_pcset(2, 7),
                                       None,
                                       None])
"""

# Calculate the number of duplicates
chains2 = []
[chains2.append(c) for c in chains if c not in chains2]
print(f"{len(chains)} chains total")
print(f"{len(chains) - len(chains2)} duplicates")

# Print the chains
for chain in chains:
    print(chain)
