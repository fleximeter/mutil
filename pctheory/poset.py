"""
File: poset.py
Author: Jeff Martin
Date: 11/7/2021

Copyright © 2021 by Jeffrey Martin. All rights reserved.
Email: jmartin@jeffreymartincomposer.com
Website: https://jeffreymartincomposer.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pctheory import pitch, pcset, pcseg, tables, transformations


def generate_chains_weak(p0: pitch.PitchClass, sc_list: list, max_2_similarity: float = 0.4,
                         max_3_similarity: float = 1):
    """
    Generates all possible "weak" chains of pcsets that match the specified input criteria. The result is a list of
    posets of the form
    <pc_0 {...} pc_1 {...} pc_2 {...}>
    where a member of each set-class in the list appears in order. The unordered set is unioned with the immediately
    adjacent free pcs to form the actual set corresponding to the set-class in the list.
    This is a weaker form of the "strong" chains in Morris 1987, where there must be complete overlap between adjacent
    pcsets. In these chains, only one pc overlaps between adjacent pcsets.
    :param p0: The starting pitch
    :param sc_list: The list of set-class names
    :param max_2_similarity: The maximum adjacent similarity percentage (expressed as a decimal). Specifies
    the maximum percentage of a set that can be duplicated in an adjacent set. For example, 0.4 means that 2 out of 5
    pcs in a pentachord may be duplicated in each adjacent set. A value of 1 means that no similarity restrictions
    are imposed (since we are allowing up to 100% similarity). A value that is too low to allow at least 1 duplicate
    pc will prevent the algorithm from generating any chains at all (since we need at least one duplicate between
    each pair of adjacent pcsets).
    :param max_3_similarity: Like max_2_similarity, except this covers three adjacent pcsets. The default value is 1,
    which imposes no similarity restrictions.
    :return: A list of weak chains. The list will be empty if it was impossible to generate any chains matching the
    provided specifications.
    """
    chain_build = [[p0]]   # The chains will be stored here
    chain_build2 = []      # (a temporary storage place for chains)
    sc = pcset.SetClass()  # The set-class object for pcset generation

    # Consider the first pcset and initialize the chains
    sc.load_from_name(sc_list[0])
    corpus = pcset.get_corpus(sc.pcset)

    # If a pcset in the corpus matches the starting pc, we can use that pcset to start a chain.
    for pcset1 in corpus:
        pcset2 = set(pcset1)
        if p0 in pcset1:
            new_chain = list(chain_build[0])
            new_chain.append(pcset2)
            new_chain[1].remove(p0)
            chain_build2.append(new_chain)

    # Clear out the last generation of chains
    chain_build = chain_build2
    chain_build2 = []

    # Continue building chains in the same manner as before
    for i in range(1, len(sc_list)):
        sc.load_from_name(sc_list[i])
        corpus = pcset.get_corpus(sc.pcset)
        for pcset1 in corpus:
            pcset2 = set(pcset1)
            for chain in chain_build:
                # Temporarily reconstruct the previous set
                tempset = set(chain[len(chain) - 1])
                tempset.add(chain[len(chain) - 2])

                # Calculate the similarity of the last set with the current one (sim2)
                intersect = tempset.intersection(pcset2)
                sim2 = len(intersect) / len(pcset2)

                # Calculate the similarity of the last two sets with the current one (sim3)
                sim3 = 0
                if len(chain) >= 4:
                    tempset2 = set(chain[len(chain) - 3])
                    tempset2.add(chain[len(chain) - 4])
                    tempset2.add(chain[len(chain) - 2])
                    union1 = tempset.union(tempset2)
                    union2 = union1.union(pcset2)
                    total_len = len(tempset) + len(tempset2) + len(pcset2)
                    sim3 = (total_len - len(union2)) / total_len

                # If the similarity conditions are satisfied, we can continue building the chains
                if sim2 <= max_2_similarity and sim3 <= max_3_similarity:
                    for pc in intersect:
                        # We cannot use the same pc as an intersection point twice in a row.
                        if pc != chain[len(chain) - 2]:
                            chain1 = []
                            # Unfortunately we need to manually copy the data structures to avoid disaster
                            for item in chain:
                                if type(item) == set:
                                    chain1.append(set(item))
                                else:
                                    chain1.append(item)
                            chain1.append(pc)
                            chain1[len(chain1) - 2].remove(pc)
                            chain1.append(set(pcset2))
                            chain1[len(chain1) - 1].remove(pc)
                            chain_build2.append(chain1)
        chain_build = chain_build2
        chain_build2 = []

    return chain_build
