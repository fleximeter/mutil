from pctheory import array, group, pcseg, pcset, pseg, pset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

ro = transformations.get_otos12()
pc = [pitch.PitchClass12(i) for i in range(12)]


def print_babbitt_all_partition_arr(arr):
    """
    Formats and prints a Babbitt all-partition array
    :param arr: A 4D all-partition array
    Dimension 1: Block
    Dimension 2: Row
    Dimension 3: Column
    Dimension 4: pcs in column
    """
    for block in arr:
        str_block = ""
        total_width = 1
        col_widths = [0 for i in range(len(block[0]))]
        padding = [1, 1]  # left and right padding
        # get the column widths
        for i in range(len(col_widths)):
            for j in range(len(block)):
                if len(block[j][i]) > col_widths[i]:
                    col_widths[i] = len(block[j][i])
        # add the padding and space for borders
        for i in range(len(col_widths)):
            col_widths[i] += padding[1]
            total_width += col_widths[i] + 1 + padding[0]

        # print the top border
        for i in range(total_width):
            str_block += "-"
        str_block += "\n"

        for row in block:
            str_block += "|"
            for i in range(len(row)):
                format_str = "{0:<" + f"{col_widths[i]}" + "}"
                chunk = ""
                for j in range(padding[0]):
                    str_block += " "
                for pc1 in row[i]:
                    chunk += str(pc1)
                str_block += format_str.format(chunk)
                str_block += "|"
            str_block += "\n"

        # print the bottom border
        for i in range(total_width):
            str_block += "-"
        str_block += "\n"

        print(str_block)


joy_of_more_sextets_arr_part = [
        [  # block pc[1]
            [[pc[2], pc[9]], [], [pc[9], pc[10], pc[8], pc[4], pc[3], pc[0]], [pc[0], pc[5]], [], [pc[11]], [pc[11], pc[1]]],
            [[pc[1]], [], [pc[1], pc[6], pc[5], pc[7]], [pc[7]], [pc[7], pc[11], pc[0]], [], [pc[3], pc[10], pc[4], pc[2], pc[9], pc[8]]],
            [[pc[3], pc[10], pc[11]], [pc[9], pc[5], pc[4]], [], [pc[4]], [], [pc[4], pc[1], pc[6], pc[0], pc[2], pc[7], pc[8]], []],
            [[pc[6]], [pc[7], pc[0], pc[2]], [], [pc[8], pc[1]], [pc[10]], [pc[10], pc[9], pc[5], pc[3]], []],
            [[pc[7], pc[8]], [pc[8], pc[1], pc[3]], [], [pc[3], pc[9], pc[2], pc[11], pc[10], pc[6]], [pc[6], pc[4], pc[5]], [], [pc[5], pc[0]]],
            [[pc[0], pc[5], pc[4]], [pc[6], pc[10], pc[11]], [pc[11], pc[2]], [], [pc[2], pc[9], pc[3], pc[1], pc[8]], [], [pc[7], pc[6]]]
        ],
        [  # block pc[2]
            [[pc[6], pc[7]], [pc[4], pc[3], pc[10]], [pc[10], pc[8], pc[2], pc[9], pc[0]], [pc[1], pc[5]], [], [], [pc[7], pc[6], pc[11]]],
            [[], [pc[5], pc[6], pc[11], pc[1], pc[7], pc[0]], [], [], [], [pc[9], pc[8]], [pc[4], pc[2], pc[3], pc[10], pc[5], pc[0]]],
            [[pc[8], pc[5], pc[10], pc[9]], [], [pc[11], pc[3], pc[4], pc[7]], [], [pc[2], pc[8], pc[6], pc[1], pc[0]], [], []],
            [[pc[3], pc[4], pc[11], pc[2]], [pc[2]], [pc[1]], [pc[8], pc[6], pc[0]], [pc[7], pc[10], pc[11], pc[3], pc[5], pc[4], pc[9]], [pc[6], pc[1]], []],
            [[pc[0], pc[1]], [pc[8], pc[9]], [], [pc[9], pc[7], pc[3], pc[2], pc[11], pc[4], pc[10]], [], [], []],
            [[], [], [pc[6], pc[5]], [], [], [pc[5], pc[0], pc[10], pc[4], pc[11], pc[2], pc[3], pc[7]], [pc[9], pc[8], pc[1]]]
        ],
        [  # block pc[3]
            [[], [], [pc[10]], [pc[3]], [pc[2], pc[4], pc[8], pc[9], pc[0], pc[7], pc[1], pc[11]], [pc[11], pc[6]], [pc[6], pc[5]]],
            [[], [], [pc[1], pc[11], pc[7], pc[6], pc[3], pc[8], pc[2]], [pc[4]], [], [], [pc[4], pc[9], pc[10], pc[7]]],
            [[], [pc[3], pc[4], pc[9], pc[11], pc[5], pc[10]], [], [pc[7]], [pc[6]], [pc[2], pc[0]], [pc[0], pc[1]]],
            [[], [pc[1], pc[2], pc[0], pc[8], pc[7]], [pc[4], pc[9]], [pc[9]], [pc[3], pc[5], pc[10]], [], [pc[11], pc[8]]],
            [[pc[0], pc[5], pc[6], pc[9], pc[2], pc[1], pc[3], pc[7], pc[8]], [], [], [pc[8], pc[11], pc[6], pc[0], pc[10]], [], [pc[10], pc[5], pc[4]], [pc[3], pc[2]]],
            [[pc[10], pc[11], pc[4]], [pc[6]], [pc[0], pc[5]], [pc[5], pc[2], pc[1]], [], [pc[1], pc[9], pc[7], pc[8], pc[3]], []]
        ],
        [  # block pc[4]
            [[pc[5]], [], [pc[2]], [pc[3]], [pc[8], pc[10], pc[4], pc[9], pc[6], pc[5]], [pc[5], pc[1], pc[11]], [pc[0]], [pc[0], pc[7]]],
            [[pc[7], pc[6]], [], [pc[6], pc[1], pc[11], pc[5], pc[0], pc[3], pc[4]], [pc[4]], [], [pc[8], pc[10], pc[9]], [pc[2]], [pc[2], pc[11]]],
            [[pc[1]], [pc[11], pc[10], pc[5], pc[3], pc[9], pc[4], pc[7], pc[8]], [pc[8]], [pc[0]], [pc[0]], [pc[2]], [pc[1]], [pc[1], pc[6]]],
            [[pc[8]], [pc[1], pc[0], pc[2], pc[6]], [pc[7]], [], [], [pc[7]], [pc[7], pc[10], pc[5], pc[11], pc[9], pc[4]], [pc[4], pc[3]]],
            [[pc[2], pc[9]], [], [pc[9]], [pc[9], pc[7], pc[1], pc[8], pc[11]], [pc[11]], [pc[0], pc[4], pc[6]], [pc[6]], [pc[5], pc[10]]],
            [[pc[3], pc[4], pc[11], pc[0], pc[10]], [], [pc[10]], [pc[10], pc[6], pc[5], pc[2]], [pc[2], pc[7], pc[1], pc[3]], [pc[3]], [pc[3], pc[8]], [pc[8], pc[9]]]
        ],
        [  # block pc[5]
            [[], [pc[4]], [pc[9], pc[8], pc[10]], [], [pc[2], pc[3]], [], [pc[3], pc[6], pc[1], pc[7], pc[5], pc[0], pc[11], pc[10]]],
            [[], [pc[11]], [pc[11], pc[6]], [pc[6], pc[7], pc[5], pc[1], pc[0], pc[9], pc[2], pc[8], pc[10], pc[3], pc[4]], [], [], [pc[4]]],
            [[], [pc[9], pc[10]], [pc[3], pc[5]], [], [pc[5], pc[11], pc[4], pc[1], pc[0]], [pc[0], pc[8]], [pc[8]]],
            [[], [], [pc[0], pc[7]], [], [pc[8], pc[6]], [pc[6], pc[2], pc[1], pc[10], pc[3], pc[9], pc[11], pc[4], pc[5]], []],
            [[pc[3], pc[8], pc[7], pc[9], pc[1], pc[2]], [pc[2], pc[5], pc[0], pc[6]], [pc[4]], [pc[11]], [pc[10], pc[7]], [pc[7]], [pc[2]]],
            [[pc[4], pc[5], pc[10], pc[0], pc[6], pc[11]], [pc[7], pc[3], pc[1]], [pc[1], pc[2]], [], [pc[9]], [], [pc[9]]]
        ],
        [  # block pc[6]
            [[pc[10]], [], [pc[10], pc[9], pc[4], pc[2], pc[8], pc[3], pc[6], pc[7], pc[11], pc[1], pc[0], pc[5]], [], [], [], [pc[5]]],
            [[pc[4], pc[11], pc[0], pc[5]], [pc[7], pc[1], pc[6]], [], [pc[3]], [], [pc[3]], [pc[3], pc[2], pc[10], pc[8], pc[9], pc[4], pc[7], pc[0], pc[11], pc[1]]],
            [[pc[6], pc[7], pc[2]], [pc[2], pc[11], pc[4], pc[3], pc[5], pc[9], pc[10]], [], [pc[1]], [pc[8]], [pc[8], pc[2]], []],
            [[], [pc[8]], [], [pc[7], pc[2]], [pc[0]], [pc[6], pc[1], pc[4], pc[5], pc[9], pc[11], pc[10]], []],
            [[pc[3], pc[1], pc[9], pc[8]], [], [], [], [pc[5], pc[10], pc[4], pc[6], pc[11]], [pc[0]], []],
            [[], [pc[0]], [], [pc[0], pc[11], pc[6], pc[4], pc[10], pc[5], pc[8], pc[9]], [pc[9], pc[1], pc[3], pc[2], pc[7]], [pc[7]], [pc[6]]]
        ],
        [  # block pc[7]
            [[pc[8]], [pc[8], pc[3], pc[4], pc[2]], [], [pc[10], pc[9], pc[6], pc[11], pc[5], pc[7]], [], [pc[7], pc[0]], [pc[0], pc[1]]],
            [[], [pc[1], pc[5], pc[6], pc[9]], [], [pc[4]], [], [pc[4], pc[10], pc[8], pc[3], pc[2]], []],
            [[pc[2], pc[0], pc[7], pc[6], pc[9], pc[5], pc[4], pc[3], pc[11]], [pc[11], pc[10], pc[7], pc[0]], [pc[6], pc[8], pc[1]], [pc[2]], [], [pc[5]], []],
            [[pc[10]], [], [], [pc[3], pc[0], pc[1]], [pc[1], pc[6]], [], [pc[6], pc[8], pc[2], pc[7], pc[4], pc[3], pc[11], pc[9], pc[10], pc[5]]],
            [[pc[1]], [], [pc[2], pc[7], pc[9], pc[3]], [pc[8]], [pc[5], pc[4], pc[0], pc[10], pc[11]], [pc[11], pc[6], pc[9]], []],
            [[], [], [pc[11], pc[10], pc[0], pc[4], pc[5]], [], [pc[8], pc[3], pc[9], pc[7], pc[2]], [pc[1]], []]
        ],
        [  # block pc[8]
            [[], [pc[8], pc[9], pc[2]], [pc[2], pc[4]], [pc[4], pc[10], pc[3]], [pc[3], pc[0], pc[11], pc[7]], [pc[7]], [pc[5]], [pc[5], pc[6], pc[1]]],
            [[pc[1], pc[0]], [pc[0]], [pc[7], pc[5]], [pc[5], pc[11], pc[6], pc[9]], [pc[9]], [pc[9], pc[10]], [pc[2], pc[4], pc[3], pc[8]], []],
            [[pc[5], pc[4], pc[11]], [pc[11]], [pc[9], pc[3], pc[10], pc[1]], [], [pc[1]], [pc[2], pc[6]], [pc[6]], [pc[8], pc[7], pc[0]]],
            [[pc[2], pc[7], pc[6]], [], [pc[6]], [pc[8], pc[0], pc[1]], [pc[4]], [pc[4], pc[11], pc[5], pc[3]], [pc[10]], [pc[10], pc[9]]],
            [[pc[9], pc[8], pc[3]], [pc[3], pc[1], pc[7]], [], [pc[7], pc[2]], [pc[2], pc[5], pc[6], pc[10]], [pc[0]], [pc[0], pc[11]], [pc[11], pc[4]]],
            [[pc[10]], [pc[10], pc[5], pc[6], pc[4]], [pc[0], pc[11], pc[8]], [], [pc[8]], [pc[8], pc[1]], [pc[1], pc[7], pc[9]], [pc[2], pc[3]]]
        ]
    ]


arr2 = ro["T0R"].transform(joy_of_more_sextets_arr_part)
for i in range(len(arr2)):
    arr2[i].reverse()

print_babbitt_all_partition_arr(joy_of_more_sextets_arr_part)
print_babbitt_all_partition_arr(arr2)
