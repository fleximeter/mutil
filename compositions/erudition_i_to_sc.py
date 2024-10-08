"""
File: trombone_to_sc.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for converting MusicXML data into SuperCollider friendly format.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""

from mgen import xml_parse_sc, sc_data_gen
from mgen.xml_parse_sc import Dynamic, Note, Sound, Pan
import random
import time

# File names and locations
OUTPUT_DESKTOP = "D:\\SuperCollider\\erudition_i"
OUTPUT_LAPTOP = "C:\\Users\\Jeff Martin\\Source\\erudition_i"
OUTPUT = OUTPUT_DESKTOP
FILE1 = "Trombone Piece 0.2.4.1a - Full score - 01 erudition I.xml"
FILE2 = "Trombone Piece 0.2.4.1b - Full score - 01 erudition I.xml"
FILE1_debug = "Trombone Piece 0.2.4.1a_debug - Full score - 01 erudition I.xml"

# Constants
NUM_BUFFERS = 24
NUM_BUSES = 80
CHANGE_BUS_CONSTANT = 20
random.seed(time.time())

# this represents dynamic levels from 0-9. it allows easy adjusting project-wide.
d = [0, 1, 2, 5, 7, 9, 13, 17, 22, 28]


def add_sc_data(new_parts):
    """
    Adds buffer indices to a list of new parts for SuperCollider
    :param new_parts: A list of new parts
    :return:
    """
    # The current voice
    i = 0
    for part in new_parts:
        for voice in part:
            for j in range(len(voice)):
                # Convert the times to floats
                voice[j].duration = float(voice[j].duration)
                voice[j].start_time = float(voice[j].start_time)
                voice[j].end_time = float(voice[j].end_time)

                # Adjust volume and add buffers and envelopes
                if type(voice[j]) == Note:
                    voice[j].mul = xml_parse_sc.equal_loudness(voice[j])
                    voice[j].legato = 4
                    add_buf(voice[j])
                    add_env(voice[j])
                elif type(voice[j]) == Sound:
                    voice[j].mul = 0.15
                    add_env_sound(voice[j])

                # The bus allocation formula. Adjacent notes alternate buses to allow legato.
                voice[j].bus_out = NUM_BUSES - CHANGE_BUS_CONSTANT + (2 * i) + (j % 2)

                # Set the wait time until the next note in the current voice
                if j < len(voice) - 1:
                    voice[j].wait = float(voice[j + 1].start_time - voice[j].start_time)
                else:
                    voice[j].wait = 0
            i += 1


def add_buf(note):
    """
    Adds a buffer to a Note
    :param note: A Note
    :return:
    """
    # A map that lists the pitch integer for each buffer. This is microtonal pitch with pcs from 0-23.
    buf_map = [-48, -44, -40, -38, -34, -30, -26, -24, -20, -16, -14, -10, -6, -2, 0, 4, 8, 10, 14, 18, 22, 24, 28, 32]

    # Choose a sensible buffer for long notes
    if note.pitch.p < buf_map[0]:
        note.buffer = 0
    elif note.pitch.p > buf_map[len(buf_map) - 1]:
        note.buffer = len(buf_map) - 1
    else:
        for i in range(len(buf_map)):
            if abs(note.pitch.p - buf_map[i]) <= 2:
                note.buffer = i

    # For short notes, choose a random buffer, but don't go too low. Otherwise we'll have too much snazz.
    if note.duration < 0.5:
        lower_limit = max(0, note.buffer - 3)
        note.buffer = random.randrange(lower_limit, NUM_BUFFERS - 1, 1)


def add_effects(new_parts, effect_parts):
    """
    Adds dynamics to a list of parsed parts. Updates buses.
    :param new_parts: A list of parsed parts
    :param effect_parts: A list of dynamic parts
    :return:
    """
    NOTE_END_TIME_PADDING = 0.05

    # Iterate through each effect entry for the current voice
    for effect in effect_parts:
        # Identify the starting note
        start_note = new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]
        if type(start_note) == list:
            for item in start_note:
                if type(item) == Note or type(item) == Sound:
                    start_note = item
                    break

        # Pan effects are easy to add
        if type(effect) == Pan:
            effect.bus_in = start_note.bus_out
            effect.duration = start_note.duration
            effect.measure = start_note.measure
            effect.start_time = start_note.start_time

        # For normal effects, we need to update buses, etc.
        else:
            # Identify the ending note
            end_note = new_parts[effect.end_note[0]][effect.end_note[1]][effect.end_note[2]]
            if type(end_note) == list:
                for item in end_note:
                    if type(item) == Note or type(item) == Sound:
                        end_note = item
                        break

            # Set times and duration
            effect.start_time = start_note.start_time
            effect.end_time = end_note.start_time + end_note.duration + NOTE_END_TIME_PADDING
            effect.measure = start_note.measure
            effect.duration = effect.end_time - effect.start_time

            bus = -1  # The bus for the effect
            first_idx = 0  # The index of the first note affected by the effect

            # Get the appropriate bus to use for the effect, and record the index of the first note affected
            for i in range(len(new_parts[effect.voice_index[0]][effect.voice_index[1]])):
                done = False
                # If we've encountered separate chaining, look inside the list
                if type(new_parts[effect.voice_index[0]][effect.voice_index[1]][i]) == list:
                    for item in new_parts[effect.voice_index[0]][effect.voice_index[1]][i]:
                        if (type(item) == Note or type(item) == Sound) and item.start_time >= effect.start_time and \
                                item.end_time <= effect.end_time:
                            bus = item.bus_out
                            first_idx = i
                            done = True
                            break
                elif new_parts[effect.voice_index[0]][effect.voice_index[1]][i].start_time >= effect.start_time and \
                        new_parts[effect.voice_index[0]][effect.voice_index[1]][i].end_time <= effect.end_time:
                    bus = new_parts[effect.voice_index[0]][effect.voice_index[1]][i].bus_out
                    first_idx = i
                    done = True
                if done:
                    break

            # Update the buses of the effect
            effect.bus_out = bus
            effect.bus_in = effect.bus_out - CHANGE_BUS_CONSTANT

            # Update the buses of affected notes
            for i in range(first_idx, len(new_parts[effect.voice_index[0]][effect.voice_index[1]])):
                done = False

                # If we're doing separate chaining
                if type(new_parts[effect.voice_index[0]][effect.voice_index[1]][i]) == list:
                    for item in new_parts[effect.voice_index[0]][effect.voice_index[1]][i]:
                        if done:
                            break
                        if type(item) == Note or type(item) == Sound:
                            if item.start_time > effect.end_time:
                                done = True
                            elif item.end_time > effect.end_time + NOTE_END_TIME_PADDING:
                                done = True
                            else:
                                item.bus_out -= CHANGE_BUS_CONSTANT
                elif new_parts[effect.voice_index[0]][effect.voice_index[1]][i].start_time > effect.end_time:
                    done = True
                elif new_parts[effect.voice_index[0]][effect.voice_index[1]][i].end_time > \
                        effect.end_time + NOTE_END_TIME_PADDING:
                    done = True
                else:
                    new_parts[effect.voice_index[0]][effect.voice_index[1]][i].bus_out -= CHANGE_BUS_CONSTANT
                if done:
                    break

        # Now we need to duplicate the effect to deal with the alternating buses in adjacent notes,
        # a feature we implemented to allow legato. At this point, only dynamics are implemented, because
        # Effect objects are not used in this piece
        effect2 = None
        if type(effect) == Dynamic:
            effect2 = Dynamic(synth=effect.synth, start_note=effect.start_note, end_note=effect.end_note,
                              voice_index=effect.voice_index, levels=effect.levels, times=effect.times,
                              curves=effect.curves, duration=effect.duration, start_time=effect.start_time,
                              end_time=effect.end_time, measure=effect.measure)
            if effect.bus_in % 2 == 0:
                effect2.bus_in = effect.bus_in + 1
                effect2.bus_out = effect.bus_out + 1
            else:
                effect2.bus_in = effect.bus_in - 1
                effect2.bus_out = effect.bus_out - 1

        # When adding effects, we use separate chaining. That is, we create a list containing the effect
        # and starting note, and put that list into the voice where the starting note used to be.
        # We will go through the voice and flatten it out later, after all dynamics and effects are added.
        # This allows us to easily add dynamics and effects by index.
        if effect2 is not None:
            if type(new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]) != list:
                item_list = [effect, effect2, new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]]
                new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]] = item_list
            else:
                new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]].insert(0, effect2)
                new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]].insert(0, effect)
        else:
            if type(new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]) != list:
                item_list = [effect, new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]]]
                new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]] = item_list
            else:
                new_parts[effect.start_note[0]][effect.start_note[1]][effect.start_note[2]].insert(0, effect)


def add_env(note):
    """
    Adds an envelope to a Note
    :param note: A Note
    :return:
    """
    if note.duration > 1:
        note.env = sc_data_gen.env6_strong_atk(note.duration)
        note.envlen = 6
    elif note.duration >= 0.25:
        note.env = sc_data_gen.env5_strong_atk(note.duration)
        note.envlen = 5
    else:
        note.env = sc_data_gen.env4_strong_atk(note.duration)
        note.envlen = 4


def add_env_sound(sound):
    """
    Adds an envelope to a Sound
    :param sound: A Sound
    :return:
    """
    sound.env = [[1, 1, 0], [sound.duration - 0.1, 0.1], [0, -2]]
    sound.envlen = 3


def add_legato(notes, legato_dur):
    """
    Adds legato to a list of notes. Legato is added by lengthening the duration of the note.
    :param notes: A list of notes
    :param legato_dur: The duration of the legato in seconds (this will be a small number like 0.02)
    :return:
    """
    for note in notes:
        note.duration += legato_dur
        if note.duration > 1:
            note.env = sc_data_gen.env6_weak_atk(note.duration)
            note.envlen = 6
        elif note.duration >= 0.25:
            note.env = sc_data_gen.env5_weak_atk(note.duration)
            note.envlen = 5
        else:
            note.env = sc_data_gen.env4_weak_atk(note.duration)
            note.envlen = 4


def batch_fm_synth_update(new_parts, updates):
    """
    Performs a batch update of synth indices
    :param new_parts: A list of parts
    :param updates: A tuple (or list). Index 1 is a tuple/list containing the index of the node to update.
    Index 2 is the new synth index.
    :return:
    """
    for item in updates:
        dur = new_parts[item[0][0]][item[0][1]][item[0][2]].duration
        new_parts[item[0][0]][item[0][1]][item[0][2]].synth = item[1] + len(item[2])
        new_parts[item[0][0]][item[0][1]][item[0][2]].mod_levels = item[2]
        new_parts[item[0][0]][item[0][1]][item[0][2]].mod_curves = item[4]
        new_parts[item[0][0]][item[0][1]][item[0][2]].mod_times = [float(dur * n) for n in item[3]]


def batch_dynamic_synth_update(new_parts):
    """
    Performs a batch update of dynamic synths
    :param new_parts: A list of parts
    :return:
    """
    for part in new_parts:
        for voice in part:
            for item in voice:
                if type(item) == list:
                    for item2 in item:
                        if type(item2) == Dynamic:
                            item2.times = [float(n * item2.duration) for n in item2.times]


def build_score():
    """
    Builds the SuperCollider score
    :return:
    """
    parsed_parts1 = xml_parse_sc.analyze_xml(FILE1)
    parsed_parts2 = xml_parse_sc.analyze_xml(FILE2)

    # Add data
    add_sc_data(parsed_parts1)
    add_sc_data(parsed_parts2)

    # Output the score for manual edit planning
    xml_parse_sc.dump_parts(parsed_parts1)

    # Add legato
    legato = [
        parsed_parts1[0][0][5],
        parsed_parts1[0][0][6],
        parsed_parts1[0][0][7],
        parsed_parts1[0][0][8],
        parsed_parts1[0][0][9],
        parsed_parts1[0][0][10],
        parsed_parts1[0][0][11],
        parsed_parts1[0][0][12],
        parsed_parts1[0][0][13],
        parsed_parts1[0][0][14],
        parsed_parts1[0][0][15],
        parsed_parts1[0][0][16],
        parsed_parts1[0][0][17],
        parsed_parts1[0][0][18],
        parsed_parts1[0][5][6],
        parsed_parts1[0][5][10],
        parsed_parts1[0][0][28],
        parsed_parts1[0][0][33],
        parsed_parts1[0][0][42],
        parsed_parts1[0][0][43],
        parsed_parts1[0][0][45],
        parsed_parts1[0][0][47],
        parsed_parts1[0][0][48],
        parsed_parts1[0][0][49],
        parsed_parts1[0][0][50],
        parsed_parts1[0][0][53],
        parsed_parts1[0][0][56],
        parsed_parts1[0][0][58],
        parsed_parts1[0][0][60],
        parsed_parts1[0][0][61],
        parsed_parts1[0][0][63],
        parsed_parts1[0][0][64],
        parsed_parts1[0][0][65],
        parsed_parts1[0][0][69],
        parsed_parts1[0][0][71],
        parsed_parts1[0][0][73],
        parsed_parts1[0][0][74],
        parsed_parts1[0][0][79],
        parsed_parts1[0][0][82],
        parsed_parts1[0][0][87],
        parsed_parts1[0][0][90],
        parsed_parts1[0][0][91],
        parsed_parts1[0][0][93],
        parsed_parts1[0][0][95],
        parsed_parts1[0][0][97],
        parsed_parts1[0][5][25],
        parsed_parts1[0][5][26],
        parsed_parts1[0][5][27],
        parsed_parts1[0][5][30],
        parsed_parts1[0][5][31],
        parsed_parts1[0][0][99],
        parsed_parts1[0][0][100],
        parsed_parts1[0][0][101],
        parsed_parts1[0][0][103],
        parsed_parts1[0][0][104],
        parsed_parts1[0][0][105],
        parsed_parts1[0][0][107],
        parsed_parts1[0][0][108],
        parsed_parts1[0][0][109],
        parsed_parts1[0][0][110],
        parsed_parts1[0][0][112],
        parsed_parts1[0][3][5],
        parsed_parts1[0][0][114],
        parsed_parts1[0][5][35],
        parsed_parts1[0][5][36],
        parsed_parts1[0][5][38],
        parsed_parts1[0][5][40],
        parsed_parts1[0][0][118],
        parsed_parts1[0][0][123],
        parsed_parts1[0][1][0],
        parsed_parts1[0][5][45],
        parsed_parts1[0][5][46],
        parsed_parts1[0][0][127],
        parsed_parts1[0][0][131],
        parsed_parts1[0][0][136],
        parsed_parts1[0][5][52],
        parsed_parts1[0][0][143],
        parsed_parts1[0][0][144],
        parsed_parts1[0][0][65],
        parsed_parts1[0][0][66],
        parsed_parts1[0][0][71],
        parsed_parts1[0][0][74],
        parsed_parts1[0][0][154],
        parsed_parts1[0][0][155],
        parsed_parts1[0][0][162],
        parsed_parts1[0][0][163],
        parsed_parts1[0][0][164],
        parsed_parts1[0][0][174],
        parsed_parts1[0][0][175],
        parsed_parts1[0][0][177],
        parsed_parts1[0][0][179],
        parsed_parts1[0][0][182],
        parsed_parts1[0][0][184],
        parsed_parts1[0][0][185],
        parsed_parts1[0][0][187],
        parsed_parts1[0][0][188],
        parsed_parts1[0][0][190],
        parsed_parts1[0][0][191],
        parsed_parts1[0][1][10],
        parsed_parts1[0][0][197],
        parsed_parts1[0][0][198],
        parsed_parts1[0][0][200],
        parsed_parts1[0][0][201],
        parsed_parts1[0][0][202],
        parsed_parts1[0][0][210],
        parsed_parts1[0][1][19],
        parsed_parts1[0][0][214],
        parsed_parts1[0][0][215],
        parsed_parts1[0][0][216],
        parsed_parts1[0][0][217],
        parsed_parts1[0][5][108],
        parsed_parts1[0][6][10],
        parsed_parts1[0][5][112],
        parsed_parts1[0][5][114],
        parsed_parts1[0][6][14],
        parsed_parts1[0][6][16],
        parsed_parts1[0][5][119],
        parsed_parts1[0][0][225],
        parsed_parts1[0][0][226],
        parsed_parts1[0][0][227],
        parsed_parts1[0][5][128],
        parsed_parts1[0][5][129],
        parsed_parts1[0][5][136],
        parsed_parts1[0][0][232],
        parsed_parts1[0][0][238],
        parsed_parts1[0][0][241],
        parsed_parts1[0][0][242],
        parsed_parts1[0][5][142],
        parsed_parts1[0][5][143],
        parsed_parts1[0][0][249],
        parsed_parts1[0][0][250],
        parsed_parts1[0][0][251],
        parsed_parts1[0][0][252],
        parsed_parts1[0][5][143],
        parsed_parts1[0][5][155],
        parsed_parts1[0][5][156],
        parsed_parts1[0][5][159],
        parsed_parts1[0][5][160],
        parsed_parts1[0][5][165],
        parsed_parts1[0][5][166],
        parsed_parts1[0][5][172],
        parsed_parts1[0][5][176],
        parsed_parts1[0][5][177],
        parsed_parts1[0][5][180],
        parsed_parts1[0][5][181],
        parsed_parts1[0][5][182],
        parsed_parts1[0][5][187],
        parsed_parts1[0][5][188],
        parsed_parts1[0][0][254],
        parsed_parts1[0][0][255],
        parsed_parts1[0][0][257],
        parsed_parts1[0][0][258],
        parsed_parts1[0][0][260],
        parsed_parts1[0][0][261],
        parsed_parts1[0][0][265],
        parsed_parts1[0][0][266],
        parsed_parts1[0][0][270],
        parsed_parts1[0][0][271],
        parsed_parts1[0][0][272],
        parsed_parts1[0][0][273],
        parsed_parts1[0][0][279],
        parsed_parts1[0][5][206],
        parsed_parts1[0][5][208],
        parsed_parts1[0][5][211],
        parsed_parts1[0][5][215],
        parsed_parts1[0][5][216],
        parsed_parts1[0][5][227],
        parsed_parts1[0][5][232],
        parsed_parts1[0][5][240],
        parsed_parts1[0][5][241],
        parsed_parts1[0][5][245],
        parsed_parts1[0][5][247],
        parsed_parts1[0][5][248],
        parsed_parts1[0][6][45],
        parsed_parts1[0][6][46],
        parsed_parts1[0][6][50],
        parsed_parts1[0][5][257],
        parsed_parts1[0][5][258],
        parsed_parts2[0][0][0],
        parsed_parts2[0][1][0],
        parsed_parts2[0][1][2],
        parsed_parts2[0][1][6],
        parsed_parts2[0][1][19],
        parsed_parts2[0][1][21],
        parsed_parts2[0][7][2],
        parsed_parts2[0][7][3],
        parsed_parts2[0][7][4]
    ]
    add_legato(legato, 0.04)

    # Data structures that hold score updates for panning
    pan1 = {
        # m1
        "0,0,0": Pan(start_note=(0, 0, 0), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,0": Pan(start_note=(0, 5, 0), pan2=0.6, panx=0.6, panw=2.0),
        # m3
        "0,0,1": Pan(start_note=(0, 0, 1), pan2=0.4, panx=2.6, panw=2.0),
        "0,5,1": Pan(start_note=(0, 5, 1), pan2=0.6, panx=2.4, panw=2.0),
        # m5
        "0,0,2": Pan(start_note=(0, 0, 2), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,2": Pan(start_note=(0, 5, 2), pan2=0.6, panx=0.6, panw=2.0),
        # m7
        "0,0,3": Pan(start_note=(0, 0, 3), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,3": Pan(start_note=(0, 5, 3), pan2=0.65, panx=0.65, panw=2.0),
        # m9
        "0,0,4": Pan(start_note=(0, 0, 4), pan2=0.4, panx=2.6, panw=2.0),
        "0,5,4": Pan(start_note=(0, 5, 4), pan2=0.6, panx=2.4, panw=2.0),
        # m10
        "0,0,5": Pan(start_note=(0, 0, 5), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,6": Pan(start_note=(0, 0, 6), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,7": Pan(start_note=(0, 0, 7), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,8": Pan(start_note=(0, 0, 8), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,9": Pan(start_note=(0, 0, 9), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,10": Pan(start_note=(0, 0, 10), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,11": Pan(start_note=(0, 0, 11), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,12": Pan(start_note=(0, 0, 12), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,13": Pan(start_note=(0, 0, 13), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,14": Pan(start_note=(0, 0, 14), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,15": Pan(start_note=(0, 0, 15), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,16": Pan(start_note=(0, 0, 16), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,17": Pan(start_note=(0, 0, 17), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,18": Pan(start_note=(0, 0, 18), pan2=0.5, panx=0.5, panw=2.0),
        # m13
        "0,0,19": Pan(start_note=(0, 0, 19), pan2=0.45, panx=2.6, panw=2.0),
        "0,5,5": Pan(start_note=(0, 5, 5), pan2=0.55, panx=2.45, panw=2.0),
        # m15
        "0,0,20": Pan(start_note=(0, 0, 20), pan2=0.4, panx=0.45, panw=2.0),
        "0,5,6": Pan(start_note=(0, 5, 6), pan2=0.55, panx=0.55, panw=2.0),
        # m16
        "0,5,7": Pan(start_note=(0, 5, 7), pan2=0.6, panx=0.55, panw=2.0),
        # m20
        "0,5,8": Pan(start_note=(0, 5, 8), pan2=0.4, panx=3, panw=2.0),
        "0,5,9": Pan(start_note=(0, 5, 9), pan2=0.5, panx=2, panw=2.0),
        "0,5,10": Pan(start_note=(0, 5, 10), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,11": Pan(start_note=(0, 5, 11), pan2=0.6, panx=0.6, panw=2.0),
        # mm 21-24
        "0,0,21": Pan(start_note=(0, 0, 21), pan2=0.35, panx=2.65, panw=2.0),
        "0,0,22": Pan(start_note=(0, 0, 22), pan2=0.35, panx=2.65, panw=2.0),
        "0,3,0": Pan(start_note=(0, 3, 0), pan2=0.45, panx=2.55, panw=2.0),
        "0,3,1": Pan(start_note=(0, 3, 1), pan2=0.45, panx=2.55, panw=2.0),
        "0,4,0": Pan(start_note=(0, 4, 0), pan2=0.55, panx=2.45, panw=2.0),
        "0,4,1": Pan(start_note=(0, 4, 1), pan2=0.55, panx=2.45, panw=2.0),
        "0,5,12": Pan(start_note=(0, 5, 12), pan2=0.65, panx=2.35, panw=2.0),
        "0,5,13": Pan(start_note=(0, 5, 13), pan2=0.65, panx=2.35, panw=2.0),
        # m25
        "0,0,23": Pan(start_note=(0, 0, 23), pan2=0.5, panx=3, panw=2.0),
        "0,0,24": Pan(start_note=(0, 0, 24), pan2=0.4, panx=0.5, panw=2.0),
        "0,0,25": Pan(start_note=(0, 0, 25), pan2=0.5, panx=2, panw=2.0),
        # m27
        "0,0,26": Pan(start_note=(0, 0, 26), pan2=0.7, panx=3, panw=2.0),
        "0,0,27": Pan(start_note=(0, 0, 27), pan2=0.5, panx=2, panw=2.0),
        "0,0,28": Pan(start_note=(0, 0, 28), pan2=0.5, panx=2, panw=2.0),
        "0,0,29": Pan(start_note=(0, 0, 29), pan2=0.6, panx=3, panw=2.0),
        "0,0,30": Pan(start_note=(0, 0, 30), pan2=0.5, panx=1, panw=2.0),
        "0,0,31": Pan(start_note=(0, 0, 31), pan2=0.6, panx=3, panw=2.0),
        "0,0,32": Pan(start_note=(0, 0, 32), pan2=0.7, panx=0, panw=2.0),
        "0,0,33": Pan(start_note=(0, 0, 33), pan2=0.6, panx=2, panw=2.0),
        "0,0,34": Pan(start_note=(0, 0, 34), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,35": Pan(start_note=(0, 0, 35), pan2=0.5, panx=2.5, panw=2.0),
        # m29
        "0,0,36": Pan(start_note=(0, 0, 36), pan2=0.5, panx=2.45, panw=2.0),
        "0,0,37": Pan(start_note=(0, 0, 37), pan2=0.5, panx=2.55, panw=2.0),
        "0,5,14": Pan(start_note=(0, 5, 14), pan2=0.7, panx=0.4, panw=2.0),
        "0,5,15": Pan(start_note=(0, 5, 15), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,16": Pan(start_note=(0, 5, 16), pan2=0.7, panx=0.5, panw=2.0),
        # m30
        "0,0,38": Pan(start_note=(0, 0, 38), pan2=0.45, panx=2.45, panw=2.0),
        "0,0,39": Pan(start_note=(0, 0, 39), pan2=0.45, panx=2.55, panw=2.0),
        "0,5,17": Pan(start_note=(0, 5, 17), pan2=0.7, panx=0.45, panw=2.0),
        "0,5,18": Pan(start_note=(0, 5, 18), pan2=0.7, panx=0.55, panw=2.0),
        # m32
        "0,0,40": Pan(start_note=(0, 0, 40), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,41": Pan(start_note=(0, 0, 41), pan2=0.5, panx=1.5, panw=2.0),
        "0,0,42": Pan(start_note=(0, 0, 42), pan2=0.45, panx=3.5, panw=2.0),
        "0,0,43": Pan(start_note=(0, 0, 43), pan2=0.7, panx=1.5, panw=2.0),
        "0,0,44": Pan(start_note=(0, 0, 44), pan2=0.45, panx=0.5, panw=2.0),
        "0,0,45": Pan(start_note=(0, 0, 45), pan2=0.7, panx=2.35, panw=2.0),
        "0,0,46": Pan(start_note=(0, 0, 46), pan2=0.7, panx=2.4, panw=2.0),
        # m33
        "0,5,19": Pan(start_note=(0, 5, 19), pan2=0.7, panx=2.45, panw=2.0),
        "0,0,47": Pan(start_note=(0, 0, 47), pan2=0.5, panx=2.55, panw=2.0),
        "0,0,48": Pan(start_note=(0, 0, 48), pan2=0.5, panx=2.55, panw=2.0),
        "0,0,49": Pan(start_note=(0, 0, 49), pan2=0.5, panx=2.55, panw=2.0),
        "0,0,50": Pan(start_note=(0, 0, 50), pan2=0.45, panx=2.5, panw=2.0),
        "0,0,51": Pan(start_note=(0, 0, 51), pan2=0.45, panx=2.55, panw=2.0),
        # m34
        "0,3,2": Pan(start_note=(0, 3, 2), pan2=0.5, panx=0.6, panw=2.0),
        "0,3,3": Pan(start_note=(0, 3, 3), pan2=0.5, panx=0.6, panw=2.0),
        "0,5,20": Pan(start_note=(0, 5, 20), pan2=0.65, panx=2.35, panw=2.0),
        "0,5,21": Pan(start_note=(0, 5, 21), pan2=0.65, panx=2.35, panw=2.0),
        "0,5,22": Pan(start_note=(0, 5, 22), pan2=0.65, panx=2.35, panw=2.0),
        # m35
        "0,0,52": Pan(start_note=(0, 0, 52), pan2=0.3, panx=0.4, panw=2.0),
        "0,0,53": Pan(start_note=(0, 0, 53), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,54": Pan(start_note=(0, 0, 54), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,55": Pan(start_note=(0, 0, 55), pan2=0.4, panx=2.6, panw=2.0),
        "0,3,4": Pan(start_note=(0, 3, 4), pan2=0.5, panx=0.6, panw=2.0),
        # m36
        "0,0,56": Pan(start_note=(0, 0, 56), pan2=0.5, panx=2.55, panw=2.0),
        "0,0,57": Pan(start_note=(0, 0, 57), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,58": Pan(start_note=(0, 0, 58), pan2=0.6, panx=2.45, panw=2.0),
        "0,0,59": Pan(start_note=(0, 0, 59), pan2=0.6, panx=2.5, panw=2.0),
        "0,0,60": Pan(start_note=(0, 0, 60), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,61": Pan(start_note=(0, 0, 61), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,62": Pan(start_note=(0, 0, 62), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,63": Pan(start_note=(0, 0, 63), pan2=0.5, panx=0.55, panw=2.0),
        "0,0,64": Pan(start_note=(0, 0, 64), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,65": Pan(start_note=(0, 0, 65), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,66": Pan(start_note=(0, 0, 66), pan2=0.6, panx=0.45, panw=2.0),
        # m37
        "0,0,67": Pan(start_note=(0, 0, 67), pan2=0.55, panx=0.5, panw=2.0),
        "0,0,68": Pan(start_note=(0, 0, 68), pan2=0.55, panx=0.55, panw=2.0),
        "0,0,69": Pan(start_note=(0, 0, 69), pan2=0.65, panx=2.45, panw=2.0),
        "0,0,70": Pan(start_note=(0, 0, 70), pan2=0.65, panx=2.55, panw=2.0),
        # m38
        "0,0,71": Pan(start_note=(0, 0, 71), pan2=0.55, panx=2.55, panw=2.0),
        "0,0,72": Pan(start_note=(0, 0, 72), pan2=0.55, panx=2.5, panw=2.0),
        "0,0,73": Pan(start_note=(0, 0, 73), pan2=0.5, panx=0.45, panw=2.0),
        "0,0,74": Pan(start_note=(0, 0, 74), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,75": Pan(start_note=(0, 0, 75), pan2=0.5, panx=0.55, panw=2.0),
        "0,5,23": Pan(start_note=(0, 5, 23), pan2=0.7, panx=2.35, panw=2.0),
        # m39
        "0,0,76": Pan(start_note=(0, 0, 76), pan2=0.5, panx=0, panw=2.0),
        "0,0,77": Pan(start_note=(0, 0, 77), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,78": Pan(start_note=(0, 0, 78), pan2=0.4, panx=1, panw=2.0),
        "0,0,79": Pan(start_note=(0, 0, 79), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,80": Pan(start_note=(0, 0, 80), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,81": Pan(start_note=(0, 0, 81), pan2=0.4, panx=1, panw=2.0),
        "0,0,82": Pan(start_note=(0, 0, 82), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,83": Pan(start_note=(0, 0, 83), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,84": Pan(start_note=(0, 0, 84), pan2=0.3, panx=0, panw=2.0),
        "0,5,24": Pan(start_note=(0, 5, 24), pan2=0.5, panx=2.4, panw=2.0),
        # m40
        "0,0,85": Pan(start_note=(0, 0, 85), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,86": Pan(start_note=(0, 0, 86), pan2=0.45, panx=2.65, panw=2.0),
        "0,0,87": Pan(start_note=(0, 0, 87), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,88": Pan(start_note=(0, 0, 88), pan2=0.5, panx=0.45, panw=2.0),
        "0,0,89": Pan(start_note=(0, 0, 89), pan2=0.55, panx=2.45, panw=2.0),
        # m41
        "0,0,90": Pan(start_note=(0, 0, 90), pan2=0.3, panx=2.35, panw=2.0),
        "0,0,91": Pan(start_note=(0, 0, 91), pan2=0.3, panx=2.4, panw=2.0),
        "0,5,25": Pan(start_note=(0, 5, 25), pan2=0.7, panx=2.65, panw=2.0),
        "0,5,26": Pan(start_note=(0, 5, 26), pan2=0.7, panx=2.65, panw=2.0),
        # m42
        "0,0,92": Pan(start_note=(0, 0, 92), pan2=0.3, panx=2.4, panw=2.0),
        "0,0,93": Pan(start_note=(0, 0, 93), pan2=0.3, panx=2.35, panw=2.0),
        "0,5,27": Pan(start_note=(0, 5, 27), pan2=0.7, panx=2.6, panw=2.0),
        "0,5,28": Pan(start_note=(0, 5, 28), pan2=0.7, panx=2.55, panw=2.0),
        # m43
        "0,0,94": Pan(start_note=(0, 0, 94), pan2=0.3, panx=2.35, panw=2.0),
        "0,5,29": Pan(start_note=(0, 5, 29), pan2=0.5, panx=0.5, panw=2.0),
        # m44
        "0,0,95": Pan(start_note=(0, 0, 95), pan2=0.3, panx=2.4, panw=2.0),
        "0,5,30": Pan(start_note=(0, 5, 30), pan2=0.7, panx=2.6, panw=2.0),
        # m45
        "0,0,96": Pan(start_note=(0, 0, 96), pan2=0.3, panx=2.35, panw=2.0),
        "0,5,31": Pan(start_note=(0, 5, 31), pan2=0.7, panx=2.7, panw=2.0),
        "0,5,32": Pan(start_note=(0, 5, 32), pan2=0.7, panx=2.75, panw=2.0),
        # m46
        "0,0,97": Pan(start_note=(0, 0, 97), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,98": Pan(start_note=(0, 0, 98), pan2=0.5, panx=2.5, panw=2.0),
        # m47
        "0,0,99": Pan(start_note=(0, 0, 99), pan2=0.6, panx=0.6, panw=2.0),
        "0,0,100": Pan(start_note=(0, 0, 100), pan2=0.5, panx=0.55, panw=2.0),
        "0,0,101": Pan(start_note=(0, 0, 101), pan2=0.4, panx=0.5, panw=2.0),
        "0,0,102": Pan(start_note=(0, 0, 102), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,103": Pan(start_note=(0, 0, 103), pan2=0.5, panx=0, panw=2.0),
        "0,0,104": Pan(start_note=(0, 0, 104), pan2=0.6, panx=2, panw=2.0),
        "0,5,33": Pan(start_note=(0, 5, 33), pan2=0.5, panx=2.45, panw=2.0),
        "0,7,0": Pan(start_note=(0, 7, 0), pan2=0.5, panx=2.55, panw=2.0),
        # m48
        "0,0,105": Pan(start_note=(0, 0, 105), pan2=0.7, panx=1, panw=2.0),
        "0,0,106": Pan(start_note=(0, 0, 106), pan2=0.6, panx=3, panw=2.0),
        "0,0,107": Pan(start_note=(0, 0, 107), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,108": Pan(start_note=(0, 0, 108), pan2=0.6, panx=0.55, panw=2.0),
        "0,0,109": Pan(start_note=(0, 0, 109), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,110": Pan(start_note=(0, 0, 110), pan2=0.4, panx=0.45, panw=2.0),
        "0,0,111": Pan(start_note=(0, 0, 111), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,34": Pan(start_note=(0, 5, 34), pan2=0.5, panx=2.45, panw=2.0),
        "0,7,1": Pan(start_note=(0, 7, 1), pan2=0.5, panx=2.55, panw=2.0),
        # m49
        "0,0,112": Pan(start_note=(0, 0, 112), pan2=0.5, panx=0.45, panw=2.0),
        "0,3,5": Pan(start_note=(0, 3, 5), pan2=0.5, panx=0.55, panw=2.0),
        # m50
        "0,0,113": Pan(start_note=(0, 0, 113), pan2=0.5, panx=2.5, panw=2.0),
        "0,3,6": Pan(start_note=(0, 3, 6), pan2=0.5, panx=0.5, panw=2.0),
        # m51
        "0,0,114": Pan(start_note=(0, 0, 114), pan2=0.3, panx=2.65, panw=2.0),
        # m52
        "0,0,115": Pan(start_note=(0, 0, 115), pan2=0.3, panx=2.6, panw=2.0),
        "0,5,35": Pan(start_note=(0, 5, 35), pan2=0.7, panx=2.4, panw=2.0),
        "0,5,36": Pan(start_note=(0, 5, 36), pan2=0.7, panx=2.35, panw=2.0),
        "0,5,37": Pan(start_note=(0, 5, 37), pan2=0.7, panx=2.4, panw=2.0),
        # m53
        "0,0,116": Pan(start_note=(0, 0, 116), pan2=0.3, panx=2.55, panw=2.0),
        # m54
        "0,0,117": Pan(start_note=(0, 0, 117), pan2=0.3, panx=2.5, panw=2.0),
        "0,5,38": Pan(start_note=(0, 5, 38), pan2=0.7, panx=2.45, panw=2.0),
        "0,5,39": Pan(start_note=(0, 5, 39), pan2=0.7, panx=2.4, panw=2.0),
        "0,5,40": Pan(start_note=(0, 5, 40), pan2=0.7, panx=2.45, panw=2.0),
        # m55
        "0,5,41": Pan(start_note=(0, 5, 41), pan2=0.7, panx=0.5, panw=2.0),
        # m56
        "0,0,118": Pan(start_note=(0, 0, 118), pan2=0.3, panx=2.45, panw=2.0),
        "0,0,119": Pan(start_note=(0, 0, 119), pan2=0.3, panx=2.45, panw=2.0),
        "0,0,120": Pan(start_note=(0, 0, 120), pan2=0.3, panx=2.4, panw=2.0),
        "0,0,121": Pan(start_note=(0, 0, 121), pan2=0.3, panx=2.4, panw=2.0),
        "0,0,122": Pan(start_note=(0, 0, 122), pan2=0.3, panx=2.45, panw=2.0),
        "0,0,123": Pan(start_note=(0, 0, 123), pan2=0.3, panx=2.5, panw=2.0),
        "0,0,124": Pan(start_note=(0, 0, 124), pan2=0.3, panx=2.5, panw=2.0),
        "0,1,0": Pan(start_note=(0, 1, 0), pan2=0.5, panx=2.55, panw=2.0),
        "0,1,1": Pan(start_note=(0, 1, 1), pan2=0.5, panx=2.55, panw=2.0),
        "0,1,2": Pan(start_note=(0, 1, 2), pan2=0.5, panx=2.6, panw=2.0),
        "0,5,42": Pan(start_note=(0, 5, 42), pan2=0.7, panx=0.65, panw=2.0),
        "0,5,43": Pan(start_note=(0, 5, 43), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,44": Pan(start_note=(0, 5, 44), pan2=0.7, panx=0.55, panw=2.0),
        "0,5,45": Pan(start_note=(0, 5, 45), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,46": Pan(start_note=(0, 5, 46), pan2=0.7, panx=0.55, panw=2.0),
        "0,5,47": Pan(start_note=(0, 5, 47), pan2=0.7, panx=0.5, panw=2.0),
        # m57
        "0,0,125": Pan(start_note=(0, 0, 125), pan2=0.3, panx=2.55, panw=2.0),
        "0,0,126": Pan(start_note=(0, 0, 126), pan2=0.3, panx=2.5, panw=2.0),
        "0,0,127": Pan(start_note=(0, 0, 127), pan2=0.3, panx=2.45, panw=2.0),
        "0,0,128": Pan(start_note=(0, 0, 128), pan2=0.3, panx=2.5, panw=2.0),
        "0,0,129": Pan(start_note=(0, 0, 129), pan2=0.3, panx=2.65, panw=2.0),
        "0,1,3": Pan(start_note=(0, 1, 3), pan2=0.45, panx=2.5, panw=2.0),
        "0,2,0": Pan(start_note=(0, 2, 0), pan2=0.55, panx=2.35, panw=2.0),
        "0,5,48": Pan(start_note=(0, 5, 48), pan2=0.7, panx=0.55, panw=2.0),
        "0,5,49": Pan(start_note=(0, 5, 49), pan2=0.7, panx=0.5, panw=2.0),
        "0,5,50": Pan(start_note=(0, 5, 50), pan2=0.7, panx=0.6, panw=2.0),
        "0,6,0": Pan(start_note=(0, 6, 0), pan2=0.8, panx=0.4, panw=2.0),
        # m58
        "0,0,130": Pan(start_note=(0, 0, 130), pan2=0.5, panx=2.6, panw=2.0),
        "0,0,131": Pan(start_note=(0, 0, 131), pan2=0.5, panx=2.65, panw=2.0),
        "0,0,132": Pan(start_note=(0, 0, 132), pan2=0.5, panx=2.6, panw=2.0),
        "0,0,133": Pan(start_note=(0, 0, 133), pan2=0.5, panx=2.55, panw=2.0),
        "0,0,134": Pan(start_note=(0, 0, 134), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,135": Pan(start_note=(0, 0, 135), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,51": Pan(start_note=(0, 5, 51), pan2=0.5, panx=0.5, panw=2.0),
        # m60
        "0,0,136": Pan(start_note=(0, 0, 136), pan2=0.3, panx=0.4, panw=2.0),
        "0,0,137": Pan(start_note=(0, 0, 137), pan2=0.3, panx=2.55, panw=2.0),
        "0,0,138": Pan(start_note=(0, 0, 138), pan2=0.3, panx=0.4, panw=2.0),
        "0,0,139": Pan(start_note=(0, 0, 139), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,140": Pan(start_note=(0, 0, 140), pan2=0.3, panx=2.6, panw=2.0),
        "0,1,4": Pan(start_note=(0, 1, 4), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,52": Pan(start_note=(0, 5, 52), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,53": Pan(start_note=(0, 5, 53), pan2=0.7, panx=2.45, panw=2.0),
        "0,5,54": Pan(start_note=(0, 5, 54), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,55": Pan(start_note=(0, 5, 55), pan2=0.7, panx=2.4, panw=2.0),
        # m61
        "0,0,141": Pan(start_note=(0, 0, 141), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,142": Pan(start_note=(0, 0, 142), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,143": Pan(start_note=(0, 0, 143), pan2=0.3, panx=2.55, panw=2.0),
        "0,0,144": Pan(start_note=(0, 0, 144), pan2=0.3, panx=2.55, panw=2.0),
        "0,0,145": Pan(start_note=(0, 0, 145), pan2=0.3, panx=2.55, panw=2.0),
        "0,0,146": Pan(start_note=(0, 0, 146), pan2=0.3, panx=0.3, panw=2.0),
        "0,5,56": Pan(start_note=(0, 5, 56), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,57": Pan(start_note=(0, 5, 57), pan2=0.7, panx=2.45, panw=2.0),
        "0,5,58": Pan(start_note=(0, 5, 58), pan2=0.7, panx=2.45, panw=2.0),
        "0,5,59": Pan(start_note=(0, 5, 59), pan2=0.7, panx=0.7, panw=2.0),
        # m63
        "0,5,60": Pan(start_note=(0, 5, 60), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,61": Pan(start_note=(0, 5, 61), pan2=0.5, panx=2.5, panw=2.0),

        # m65
        "0,5,62": Pan(start_note=(0, 5, 62), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,63": Pan(start_note=(0, 5, 63), pan2=0.5, panx=2.5, panw=2.0),
        # m66
        "0,5,64": Pan(start_note=(0, 5, 64), pan2=0.3, panx=0, panw=3.0),
        "0,5,65": Pan(start_note=(0, 5, 65), pan2=0.4, panx=0, panw=3.0),
        "0,5,66": Pan(start_note=(0, 5, 66), pan2=0.5, panx=0, panw=3.0),
        "0,5,67": Pan(start_note=(0, 5, 67), pan2=0.6, panx=1, panw=3.0),
        "0,5,68": Pan(start_note=(0, 5, 68), pan2=0.5, panx=1, panw=3.0),
        "0,5,69": Pan(start_note=(0, 5, 69), pan2=0.6, panx=1, panw=3.0),
        # m67
        "0,5,70": Pan(start_note=(0, 5, 70), pan2=0.7, panx=3, panw=3.0),
        "0,5,71": Pan(start_note=(0, 5, 71), pan2=0.6, panx=3, panw=3.0),
        "0,5,72": Pan(start_note=(0, 5, 72), pan2=0.5, panx=3, panw=3.0),
        "0,5,73": Pan(start_note=(0, 5, 73), pan2=0.4, panx=2, panw=3.0),
        "0,5,74": Pan(start_note=(0, 5, 74), pan2=0.5, panx=2, panw=3.0),
        "0,5,75": Pan(start_note=(0, 5, 75), pan2=0.4, panx=2, panw=3.0),
        "0,5,76": Pan(start_note=(0, 5, 76), pan2=0.3, panx=2, panw=3.0),
        # m68
        "0,5,77": Pan(start_note=(0, 5, 77), pan2=0.3, panx=0.3, panw=2.0),
        "0,6,1": Pan(start_note=(0, 6, 1), pan2=0.7, panx=0.7, panw=2.0),
        # m69
        "0,0,147": Pan(start_note=(0, 0, 147), pan2=0.3, panx=0.3, panw=2.0),
        "0,5,78": Pan(start_note=(0, 5, 78), pan2=0.7, panx=0.7, panw=2.0),
        # m70
        "0,0,148": Pan(start_note=(0, 0, 148), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,149": Pan(start_note=(0, 0, 149), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,150": Pan(start_note=(0, 0, 150), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,79": Pan(start_note=(0, 5, 79), pan2=0.5, panx=2.5, panw=2.0),
        # m71
        "0,5,80": Pan(start_note=(0, 5, 80), pan2=0.5, panx=2.45, panw=2.0),
        "0,5,81": Pan(start_note=(0, 5, 81), pan2=0.5, panx=2.4, panw=2.0),
        # m72
        "0,0,151": Pan(start_note=(0, 0, 151), pan2=0.5, panx=0.45, panw=2.0),
        "0,5,82": Pan(start_note=(0, 5, 82), pan2=0.5, panx=2.3, panw=2.0),
        "0,5,83": Pan(start_note=(0, 5, 83), pan2=0.3, panx=2.25, panw=2.0),
        "0,5,84": Pan(start_note=(0, 5, 84), pan2=0.7, panx=0.55, panw=2.0),
        # m73
        "0,0,152": Pan(start_note=(0, 0, 152), pan2=0.3, panx=0, panw=3.0),
        "0,0,153": Pan(start_note=(0, 0, 153), pan2=0.3, panx=0, panw=3.0),
        "0,5,85": Pan(start_note=(0, 5, 85), pan2=0.7, panx=1, panw=3.0),
        "0,5,86": Pan(start_note=(0, 5, 86), pan2=0.7, panx=1, panw=3.0),
        # m75
        "0,0,154": Pan(start_note=(0, 0, 154), pan2=0.3, panx=0.3, panw=3.0),
        "0,0,155": Pan(start_note=(0, 0, 155), pan2=0.3, panx=0.3, panw=3.0),
        "0,0,156": Pan(start_note=(0, 0, 156), pan2=0.3, panx=0.3, panw=3.0),
        "0,5,87": Pan(start_note=(0, 5, 87), pan2=0.7, panx=0.7, panw=3.0),
        # m76
        "0,0,157": Pan(start_note=(0, 0, 157), pan2=0.3, panx=2.3, panw=2.0),
        "0,0,158": Pan(start_note=(0, 0, 158), pan2=0.3, panx=2.25, panw=2.0),
        "0,0,159": Pan(start_note=(0, 0, 159), pan2=0.3, panx=2.3, panw=2.0),
        "0,0,160": Pan(start_note=(0, 0, 160), pan2=0.3, panx=2.35, panw=2.0),
        "0,0,161": Pan(start_note=(0, 0, 161), pan2=0.3, panx=2.4, panw=2.0),
        "0,1,5": Pan(start_note=(0, 1, 5), pan2=0.45, panx=2.45, panw=2.0),
        "0,1,6": Pan(start_note=(0, 1, 6), pan2=0.45, panx=2.5, panw=2.0),
        "0,1,7": Pan(start_note=(0, 1, 7), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,88": Pan(start_note=(0, 5, 88), pan2=0.55, panx=0.5, panw=2.0),
        "0,7,2": Pan(start_note=(0, 7, 2), pan2=0.7, panx=2.5, panw=2.0),
        "0,7,3": Pan(start_note=(0, 7, 3), pan2=0.7, panx=2.5, panw=2.0),
        "0,7,4": Pan(start_note=(0, 7, 4), pan2=0.7, panx=2.5, panw=2.0),
        # m77
        "0,0,162": Pan(start_note=(0, 0, 162), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,163": Pan(start_note=(0, 0, 163), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,164": Pan(start_note=(0, 0, 164), pan2=0.6, panx=0.6, panw=2.0),
        "0,0,165": Pan(start_note=(0, 0, 165), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,89": Pan(start_note=(0, 5, 89), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,90": Pan(start_note=(0, 5, 90), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,91": Pan(start_note=(0, 5, 91), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,92": Pan(start_note=(0, 5, 92), pan2=0.6, panx=0.6, panw=2.0),
        "0,7,5": Pan(start_note=(0, 7, 5), pan2=0.7, panx=2.55, panw=2.0),
        # m79
        "0,0,166": Pan(start_note=(0, 0, 166), pan2=0.3, panx=0, panw=3.0),
        "0,0,167": Pan(start_note=(0, 0, 167), pan2=0.3, panx=1, panw=3.0),
        "0,0,168": Pan(start_note=(0, 0, 168), pan2=0.3, panx=0.3, panw=2.0),
        "0,0,169": Pan(start_note=(0, 0, 169), pan2=0.3, panx=0.35, panw=2.0),
        "0,5,93": Pan(start_note=(0, 5, 93), pan2=0.7, panx=0.55, panw=2.0),
        "0,5,94": Pan(start_note=(0, 5, 94), pan2=0.7, panx=0.6, panw=2.0),
        "0,5,95": Pan(start_note=(0, 5, 95), pan2=0.7, panx=0.55, panw=2.0),
        "0,5,96": Pan(start_note=(0, 5, 96), pan2=0.7, panx=0.5, panw=2.0),
        # m80
        "0,0,170": Pan(start_note=(0, 0, 170), pan2=0.3, panx=0, panw=3.0),
        "0,0,171": Pan(start_note=(0, 0, 171), pan2=0.3, panx=1, panw=3.0),
        "0,0,172": Pan(start_note=(0, 0, 172), pan2=0.3, panx=1, panw=3.0),
        "0,0,173": Pan(start_note=(0, 0, 173), pan2=0.3, panx=1, panw=3.0),
        "0,0,174": Pan(start_note=(0, 0, 174), pan2=0.3, panx=0, panw=3.0),
        "0,5,97": Pan(start_note=(0, 5, 97), pan2=0.7, panx=0.55, panw=2.0),
        "0,5,98": Pan(start_note=(0, 5, 98), pan2=0.7, panx=0.6, panw=2.0),
        # m81
        "0,0,175": Pan(start_note=(0, 0, 175), pan2=0.3, panx=0.1, panw=3.0),
        "0,0,176": Pan(start_note=(0, 0, 176), pan2=0.3, panx=0.2, panw=3.0),
        "0,0,177": Pan(start_note=(0, 0, 177), pan2=0.3, panx=0.3, panw=2.0),
        "0,0,178": Pan(start_note=(0, 0, 178), pan2=0.3, panx=0.3, panw=2.0),
        "0,0,179": Pan(start_note=(0, 0, 179), pan2=0.3, panx=0.35, panw=2.0),
        # m82
        "0,0,180": Pan(start_note=(0, 0, 180), pan2=0.3, panx=0.35, panw=2.0),
        "0,0,181": Pan(start_note=(0, 0, 181), pan2=0.6, panx=0.55, panw=2.0),
        "0,1,8": Pan(start_note=(0, 1, 8), pan2=0.6, panx=0.7, panw=2.0),
        # m83
        "0,0,182": Pan(start_note=(0, 0, 182), pan2=0.3, panx=0.45, panw=2.0),
        "0,0,183": Pan(start_note=(0, 0, 183), pan2=0.7, panx=0.5, panw=2.0),
        "0,0,184": Pan(start_note=(0, 0, 184), pan2=0.3, panx=2.55, panw=2.0),
        "0,0,185": Pan(start_note=(0, 0, 185), pan2=0.4, panx=2.6, panw=2.0),
        "0,0,186": Pan(start_note=(0, 0, 186), pan2=0.6, panx=2.65, panw=2.0),
        "0,0,187": Pan(start_note=(0, 0, 187), pan2=0.7, panx=0.65, panw=2.0),
        "0,0,188": Pan(start_note=(0, 0, 188), pan2=0.3, panx=0.6, panw=2.0),
        "0,1,9": Pan(start_note=(0, 1, 9), pan2=0.6, panx=2.35, panw=2.0),
        # m84
        "0,0,189": Pan(start_note=(0, 0, 189), pan2=0.4, panx=0.55, panw=2.0),
        "0,0,190": Pan(start_note=(0, 0, 190), pan2=0.5, panx=0.45, panw=2.0),
        "0,0,191": Pan(start_note=(0, 0, 191), pan2=0.6, panx=0.5, panw=2.0),
        "0,0,192": Pan(start_note=(0, 0, 192), pan2=0.5, panx=0.45, panw=2.0),
        "0,1,10": Pan(start_note=(0, 1, 10), pan2=0.5, panx=0.55, panw=2.0),
        "0,1,11": Pan(start_note=(0, 1, 11), pan2=0.5, panx=0.6, panw=2.0),
        # m85
        "0,0,193": Pan(start_note=(0, 0, 193), pan2=0.5, panx=2.5, panw=3.0),
        "0,0,194": Pan(start_note=(0, 0, 194), pan2=0.6, panx=2.6, panw=3.0),
        "0,0,195": Pan(start_note=(0, 0, 195), pan2=0.7, panx=2.7, panw=3.0),
        "0,0,196": Pan(start_note=(0, 0, 196), pan2=0.5, panx=0.4, panw=3.0),
        "0,1,12": Pan(start_note=(0, 1, 12), pan2=0.5, panx=2.7, panw=3.0),
        "0,1,13": Pan(start_note=(0, 1, 13), pan2=0.5, panx=0.5, panw=3.0),
        # m86
        "0,0,197": Pan(start_note=(0, 0, 197), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,198": Pan(start_note=(0, 0, 198), pan2=0.3, panx=0.3, panw=2.0),
        "0,0,199": Pan(start_note=(0, 0, 199), pan2=0.2, panx=0.2, panw=2.0),
        "0,0,200": Pan(start_note=(0, 0, 200), pan2=0.3, panx=2.3, panw=2.0),
        "0,0,201": Pan(start_note=(0, 0, 201), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,202": Pan(start_note=(0, 0, 202), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,203": Pan(start_note=(0, 0, 203), pan2=0.6, panx=2.6, panw=2.0),
        "0,0,204": Pan(start_note=(0, 0, 204), pan2=0.5, panx=2.6, panw=2.0),
        "0,1,14": Pan(start_note=(0, 1, 14), pan2=0.6, panx=2.4, panw=2.0),
        "0,1,15": Pan(start_note=(0, 1, 15), pan2=0.5, panx=2.4, panw=2.0),
        # m87
        "0,0,205": Pan(start_note=(0, 0, 205), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,206": Pan(start_note=(0, 0, 206), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,207": Pan(start_note=(0, 0, 207), pan2=0.5, panx=2.3, panw=2.0),
        "0,1,16": Pan(start_note=(0, 1, 16), pan2=0.5, panx=2.45, panw=2.0),
        "0,5,99": Pan(start_note=(0, 5, 99), pan2=0.5, panx=2.55, panw=2.0),
        "0,6,2": Pan(start_note=(0, 6, 2), pan2=0.5, panx=2.7, panw=2.0),
        # m89
        "0,0,208": Pan(start_note=(0, 0, 208), pan2=0.5, panx=2.3, panw=2.0),
        "0,0,209": Pan(start_note=(0, 0, 209), pan2=0.5, panx=2.3, panw=2.0),
        "0,1,17": Pan(start_note=(0, 1, 17), pan2=0.5, panx=2.45, panw=2.0),
        "0,1,18": Pan(start_note=(0, 1, 18), pan2=0.5, panx=2.45, panw=2.0),
        "0,5,100": Pan(start_note=(0, 5, 100), pan2=0.5, panx=2.55, panw=2.0),
        "0,5,101": Pan(start_note=(0, 5, 101), pan2=0.4, panx=0.45, panw=2.0),
        "0,5,102": Pan(start_note=(0, 5, 102), pan2=0.4, panx=0.45, panw=2.0),
        "0,5,103": Pan(start_note=(0, 5, 103), pan2=0.4, panx=0.5, panw=2.0),
        "0,6,3": Pan(start_note=(0, 6, 3), pan2=0.5, panx=2.7, panw=2.0),
        "0,6,4": Pan(start_note=(0, 6, 4), pan2=0.7, panx=0.65, panw=2.0),
        "0,6,5": Pan(start_note=(0, 6, 5), pan2=0.7, panx=0.6, panw=2.0),
        # m90
        "0,0,210": Pan(start_note=(0, 0, 210), pan2=0.2, panx=2.2, panw=2.0),
        "0,0,211": Pan(start_note=(0, 0, 211), pan2=0.2, panx=2.3, panw=2.0),
        "0,0,212": Pan(start_note=(0, 0, 212), pan2=0.2, panx=2.4, panw=2.0),
        "0,1,19": Pan(start_note=(0, 1, 19), pan2=0.5, panx=2.5, panw=2.0),
        "0,1,20": Pan(start_note=(0, 1, 20), pan2=0.5, panx=2.6, panw=2.0),
        "0,1,21": Pan(start_note=(0, 1, 21), pan2=0.5, panx=2.55, panw=2.0),
        "0,5,104": Pan(start_note=(0, 5, 104), pan2=0.4, panx=0.45, panw=2.0),
        "0,5,105": Pan(start_note=(0, 5, 105), pan2=0.4, panx=0.4, panw=2.0),
        "0,6,6": Pan(start_note=(0, 6, 6), pan2=0.7, panx=0.65, panw=2.0),
        "0,6,7": Pan(start_note=(0, 6, 7), pan2=0.7, panx=0.6, panw=2.0),
        # m91
        "0,0,213": Pan(start_note=(0, 0, 213), pan2=0.5, panx=0.5, panw=3.0),
        "0,0,214": Pan(start_note=(0, 0, 214), pan2=0.4, panx=0.4, panw=3.0),
        "0,0,215": Pan(start_note=(0, 0, 215), pan2=0.5, panx=0.5, panw=3.0),
        "0,0,216": Pan(start_note=(0, 0, 216), pan2=0.6, panx=0.6, panw=3.0),
        "0,0,217": Pan(start_note=(0, 0, 217), pan2=0.5, panx=0.5, panw=3.0),
        # m92
        "0,5,106": Pan(start_note=(0, 5, 106), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,107": Pan(start_note=(0, 5, 107), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,108": Pan(start_note=(0, 5, 108), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,109": Pan(start_note=(0, 5, 109), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,110": Pan(start_note=(0, 5, 110), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,111": Pan(start_note=(0, 5, 111), pan2=0.55, panx=0.55, panw=2.0),
        "0,6,8": Pan(start_note=(0, 6, 8), pan2=0.6, panx=0.6, panw=2.0),
        "0,6,9": Pan(start_note=(0, 6, 9), pan2=0.65, panx=0.65, panw=2.0),
        "0,6,10": Pan(start_note=(0, 6, 10), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,11": Pan(start_note=(0, 6, 11), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,12": Pan(start_note=(0, 6, 12), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,13": Pan(start_note=(0, 6, 13), pan2=0.7, panx=0.7, panw=2.0),
        # m93
        "0,5,112": Pan(start_note=(0, 5, 112), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,113": Pan(start_note=(0, 5, 113), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,114": Pan(start_note=(0, 5, 114), pan2=0.4, panx=2.4, panw=2.0),
        "0,5,115": Pan(start_note=(0, 5, 115), pan2=0.4, panx=2.4, panw=2.0),
        "0,5,116": Pan(start_note=(0, 5, 116), pan2=0.35, panx=2.35, panw=3.0),
        "0,5,117": Pan(start_note=(0, 5, 117), pan2=0.35, panx=2.35, panw=3.0),
        "0,5,118": Pan(start_note=(0, 5, 118), pan2=0.3, panx=2.3, panw=3.0),
        "0,6,14": Pan(start_note=(0, 6, 14), pan2=0.6, panx=2.6, panw=2.0),
        "0,6,15": Pan(start_note=(0, 6, 15), pan2=0.6, panx=2.6, panw=2.0),
        "0,6,16": Pan(start_note=(0, 6, 16), pan2=0.55, panx=2.55, panw=3.0),
        "0,6,17": Pan(start_note=(0, 6, 17), pan2=0.55, panx=2.55, panw=3.0),
        "0,6,18": Pan(start_note=(0, 6, 18), pan2=0.5, panx=2.5, panw=3.0),
        # m94
        "0,0,218": Pan(start_note=(0, 0, 218), pan2=0.55, panx=1, panw=3.0),
        "0,0,219": Pan(start_note=(0, 0, 219), pan2=0.5, panx=2.9, panw=3.0),
        "0,0,220": Pan(start_note=(0, 0, 220), pan2=0.45, panx=0.8, panw=3.0),
        "0,0,221": Pan(start_note=(0, 0, 221), pan2=0.4, panx=2.6, panw=3.0),
        "0,0,222": Pan(start_note=(0, 0, 222), pan2=0.45, panx=0.7, panw=3.0),
        "0,0,223": Pan(start_note=(0, 0, 223), pan2=0.5, panx=0.5, panw=3.0),
        "0,0,224": Pan(start_note=(0, 0, 224), pan2=0.55, panx=2.5, panw=3.0),
        "0,0,225": Pan(start_note=(0, 0, 225), pan2=0.5, panx=0.45, panw=3.0),
        "0,0,226": Pan(start_note=(0, 0, 226), pan2=0.45, panx=0.4, panw=3.0),
        "0,0,227": Pan(start_note=(0, 0, 227), pan2=0.5, panx=0.35, panw=3.0),
        "0,0,228": Pan(start_note=(0, 0, 228), pan2=0.5, panx=0.4, panw=3.0),
        "0,5,119": Pan(start_note=(0, 5, 119), pan2=0.7, panx=0, panw=3.0),
        "0,5,120": Pan(start_note=(0, 5, 120), pan2=0.65, panx=0.5, panw=3.0),
        # m96
        "0,5,121": Pan(start_note=(0, 5, 121), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,122": Pan(start_note=(0, 5, 122), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,123": Pan(start_note=(0, 5, 123), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,124": Pan(start_note=(0, 5, 124), pan2=0.45, panx=0.45, panw=2.0),
        "0,7,6": Pan(start_note=(0, 7, 6), pan2=0.7, panx=0.7, panw=2.0),
        "0,7,7": Pan(start_note=(0, 7, 7), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,19": Pan(start_note=(0, 6, 19), pan2=0.65, panx=0.65, panw=2.0),
        "0,6,20": Pan(start_note=(0, 6, 20), pan2=0.65, panx=0.65, panw=2.0),
        # m97
        "0,5,125": Pan(start_note=(0, 5, 125), pan2=0.4, panx=2.4, panw=2.0),
        "0,5,126": Pan(start_note=(0, 5, 126), pan2=0.4, panx=2.35, panw=2.0),
        "0,5,127": Pan(start_note=(0, 5, 127), pan2=0.4, panx=2.4, panw=2.0),
        "0,5,128": Pan(start_note=(0, 5, 128), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,129": Pan(start_note=(0, 5, 129), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,130": Pan(start_note=(0, 5, 130), pan2=0.5, panx=0.5, panw=2.0),
        "0,6,21": Pan(start_note=(0, 6, 21), pan2=0.6, panx=2.6, panw=2.0),
        "0,6,22": Pan(start_note=(0, 6, 22), pan2=0.6, panx=2.65, panw=2.0),
        "0,6,23": Pan(start_note=(0, 6, 23), pan2=0.6, panx=2.6, panw=2.0),
        # m98
        "0,5,131": Pan(start_note=(0, 5, 131), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,132": Pan(start_note=(0, 5, 132), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,133": Pan(start_note=(0, 5, 133), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,134": Pan(start_note=(0, 5, 134), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,135": Pan(start_note=(0, 5, 135), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,136": Pan(start_note=(0, 5, 136), pan2=0.55, panx=2.55, panw=2.0),
        "0,5,137": Pan(start_note=(0, 5, 137), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,138": Pan(start_note=(0, 5, 138), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,139": Pan(start_note=(0, 5, 139), pan2=0.4, panx=2.4, panw=2.0),
        "0,6,24": Pan(start_note=(0, 6, 24), pan2=0.6, panx=0.6, panw=2.0),
        "0,6,25": Pan(start_note=(0, 6, 25), pan2=0.6, panx=0.6, panw=2.0),
        "0,6,26": Pan(start_note=(0, 6, 26), pan2=0.6, panx=2.6, panw=2.0),
        # m99
        "0,0,229": Pan(start_note=(0, 0, 229), pan2=0.4, panx=3, panw=3.0),
        "0,0,230": Pan(start_note=(0, 0, 230), pan2=0.35, panx=2, panw=3.0),
        "0,0,231": Pan(start_note=(0, 0, 231), pan2=0.4, panx=0.5, panw=3.0),
        "0,0,232": Pan(start_note=(0, 0, 232), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,233": Pan(start_note=(0, 0, 233), pan2=0.4, panx=0.4, panw=2.0),
        # m100
        "0,0,234": Pan(start_note=(0, 0, 234), pan2=0.35, panx=0.35, panw=2.0),
        "0,0,235": Pan(start_note=(0, 0, 235), pan2=0.45, panx=2.5, panw=3.0),
        "0,0,236": Pan(start_note=(0, 0, 236), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,237": Pan(start_note=(0, 0, 237), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,238": Pan(start_note=(0, 0, 238), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,239": Pan(start_note=(0, 0, 239), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,140": Pan(start_note=(0, 5, 140), pan2=0.65, panx=0.65, panw=2.0),
        # m101
        "0,0,240": Pan(start_note=(0, 0, 240), pan2=0.35, panx=0.35, panw=2.0),
        "0,0,241": Pan(start_note=(0, 0, 241), pan2=0.35, panx=0.35, panw=2.0),
        "0,0,242": Pan(start_note=(0, 0, 242), pan2=0.35, panx=0.35, panw=2.0),
        "0,0,243": Pan(start_note=(0, 0, 243), pan2=0.35, panx=0.35, panw=2.0),
        "0,0,244": Pan(start_note=(0, 0, 244), pan2=0.35, panx=0.35, panw=2.0),
        "0,1,22": Pan(start_note=(0, 1, 22), pan2=0.5, panx=0.5, panw=2.0),
        "0,1,23": Pan(start_note=(0, 1, 23), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,141": Pan(start_note=(0, 5, 141), pan2=0.65, panx=0.65, panw=2.0),
        # m102
        "0,0,245": Pan(start_note=(0, 0, 245), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,246": Pan(start_note=(0, 0, 246), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,247": Pan(start_note=(0, 0, 247), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,248": Pan(start_note=(0, 0, 248), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,142": Pan(start_note=(0, 5, 142), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,143": Pan(start_note=(0, 5, 143), pan2=0.6, panx=0.6, panw=2.0),
        # m103
        "0,0,249": Pan(start_note=(0, 0, 249), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,250": Pan(start_note=(0, 0, 250), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,251": Pan(start_note=(0, 0, 251), pan2=0.55, panx=2.55, panw=2.0),
        "0,0,252": Pan(start_note=(0, 0, 252), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,253": Pan(start_note=(0, 0, 253), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,144": Pan(start_note=(0, 5, 144), pan2=0.6, panx=0.6, panw=2.0),
        # m104
        "0,5,145": Pan(start_note=(0, 5, 145), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,146": Pan(start_note=(0, 5, 146), pan2=0.4, panx=0.4, panw=2.0),
        "0,6,27": Pan(start_note=(0, 6, 27), pan2=0.6, panx=0.6, panw=2.0),
        # m105
        "0,5,147": Pan(start_note=(0, 5, 147), pan2=0.65, panx=0.65, panw=2.0),
        "0,5,148": Pan(start_note=(0, 5, 148), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,149": Pan(start_note=(0, 5, 149), pan2=0.4, panx=2.6, panw=2.0),
        "0,5,150": Pan(start_note=(0, 5, 150), pan2=0.45, panx=2.55, panw=2.0),
        "0,5,151": Pan(start_note=(0, 5, 151), pan2=0.5, panx=2.6, panw=2.0),
        "0,5,152": Pan(start_note=(0, 5, 152), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,153": Pan(start_note=(0, 5, 153), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,154": Pan(start_note=(0, 5, 154), pan2=0.4, panx=0.4, panw=2.0),
        "0,6,28": Pan(start_note=(0, 6, 28), pan2=0.6, panx=0.6, panw=2.0),
        "0,6,29": Pan(start_note=(0, 6, 29), pan2=0.65, panx=2.35, panw=2.0),
        "0,6,30": Pan(start_note=(0, 6, 30), pan2=0.6, panx=2.4, panw=2.0),
        "0,6,31": Pan(start_note=(0, 6, 31), pan2=0.65, panx=2.35, panw=2.0),
        "0,6,32": Pan(start_note=(0, 6, 32), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,33": Pan(start_note=(0, 6, 33), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,34": Pan(start_note=(0, 6, 34), pan2=0.65, panx=0.65, panw=2.0),
        # m106
        "0,5,155": Pan(start_note=(0, 5, 155), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,156": Pan(start_note=(0, 5, 156), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,157": Pan(start_note=(0, 5, 157), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,158": Pan(start_note=(0, 5, 158), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,159": Pan(start_note=(0, 5, 159), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,160": Pan(start_note=(0, 5, 160), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,161": Pan(start_note=(0, 5, 161), pan2=0.35, panx=0.35, panw=2.0),
        "0,5,162": Pan(start_note=(0, 5, 162), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,163": Pan(start_note=(0, 5, 163), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,164": Pan(start_note=(0, 5, 164), pan2=0.45, panx=0.45, panw=2.0),
        "0,6,35": Pan(start_note=(0, 6, 35), pan2=0.6, panx=0.6, panw=2.0),
        # m107
        "0,5,165": Pan(start_note=(0, 5, 165), pan2=0.5, panx=2.5, panw=3.0),
        "0,5,166": Pan(start_note=(0, 5, 166), pan2=0.65, panx=2.65, panw=3.0),
        "0,5,167": Pan(start_note=(0, 5, 167), pan2=0.5, panx=2.5, panw=3.0),
        "0,5,168": Pan(start_note=(0, 5, 168), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,169": Pan(start_note=(0, 5, 169), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,170": Pan(start_note=(0, 5, 170), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,171": Pan(start_note=(0, 5, 171), pan2=0.5, panx=0.5, panw=2.0),
        # m108
        "0,5,172": Pan(start_note=(0, 5, 172), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,173": Pan(start_note=(0, 5, 173), pan2=0.45, panx=0.45, panw=2.0),
        "0,6,36": Pan(start_note=(0, 6, 36), pan2=0.6, panx=0.6, panw=2.0),
        # m109
        "0,5,174": Pan(start_note=(0, 5, 174), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,175": Pan(start_note=(0, 5, 175), pan2=0.35, panx=0.35, panw=2.0),
        "0,5,176": Pan(start_note=(0, 5, 176), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,177": Pan(start_note=(0, 5, 177), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,178": Pan(start_note=(0, 5, 178), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,179": Pan(start_note=(0, 5, 179), pan2=0.4, panx=0.4, panw=2.0),
        # m110
        "0,5,180": Pan(start_note=(0, 5, 180), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,181": Pan(start_note=(0, 5, 181), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,182": Pan(start_note=(0, 5, 182), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,183": Pan(start_note=(0, 5, 183), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,184": Pan(start_note=(0, 5, 184), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,185": Pan(start_note=(0, 5, 185), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,186": Pan(start_note=(0, 5, 186), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,187": Pan(start_note=(0, 5, 187), pan2=0.4, panx=0.4, panw=2.0),
        "0,6,37": Pan(start_note=(0, 6, 37), pan2=0.55, panx=0.55, panw=2.0),
        # m111
        "0,5,188": Pan(start_note=(0, 5, 188), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,189": Pan(start_note=(0, 5, 189), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,190": Pan(start_note=(0, 5, 190), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,191": Pan(start_note=(0, 5, 191), pan2=0.4, panx=2.6, panw=2.0),
        "0,5,192": Pan(start_note=(0, 5, 192), pan2=0.4, panx=2.6, panw=2.0),
        "0,6,38": Pan(start_note=(0, 6, 38), pan2=0.6, panx=2.4, panw=2.0),
        "0,6,39": Pan(start_note=(0, 6, 39), pan2=0.65, panx=2.45, panw=2.0),
        # m112
        "0,0,254": Pan(start_note=(0, 0, 254), pan2=0.4, panx=0, panw=3.0),
        "0,0,255": Pan(start_note=(0, 0, 255), pan2=0.4, panx=0.15, panw=3.0),
        "0,0,256": Pan(start_note=(0, 0, 256), pan2=0.35, panx=0.25, panw=3.0),
        "0,0,257": Pan(start_note=(0, 0, 257), pan2=0.4, panx=0.4, panw=3.0),
        "0,0,258": Pan(start_note=(0, 0, 258), pan2=0.35, panx=0.5, panw=3.0),
        "0,0,259": Pan(start_note=(0, 0, 259), pan2=0.35, panx=0.65, panw=3.0),
        "0,0,260": Pan(start_note=(0, 0, 260), pan2=0.4, panx=0.75, panw=3.0),
        "0,0,261": Pan(start_note=(0, 0, 261), pan2=0.4, panx=0.9, panw=3.0),
        "0,0,262": Pan(start_note=(0, 0, 262), pan2=0.45, panx=1, panw=3.0),
        "0,5,193": Pan(start_note=(0, 5, 193), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,194": Pan(start_note=(0, 5, 194), pan2=0.55, panx=0.55, panw=2.0),
        "0,6,40": Pan(start_note=(0, 6, 40), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,41": Pan(start_note=(0, 6, 41), pan2=0.7, panx=0.7, panw=2.0),
        # m113
        "0,0,263": Pan(start_note=(0, 0, 263), pan2=0.4, panx=0.4, panw=2.0),
        "0,0,264": Pan(start_note=(0, 0, 264), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,265": Pan(start_note=(0, 0, 265), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,195": Pan(start_note=(0, 5, 195), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,196": Pan(start_note=(0, 5, 196), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,197": Pan(start_note=(0, 5, 197), pan2=0.75, panx=0.75, panw=2.0),
        "0,6,42": Pan(start_note=(0, 6, 42), pan2=0.7, panx=0.7, panw=2.0),
        # m114
        "0,0,266": Pan(start_note=(0, 0, 266), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,267": Pan(start_note=(0, 0, 267), pan2=0.45, panx=0.45, panw=2.0),
        "0,0,268": Pan(start_note=(0, 0, 268), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,269": Pan(start_note=(0, 0, 269), pan2=0.5, panx=0.5, panw=2.0),
        "0,0,270": Pan(start_note=(0, 0, 270), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,271": Pan(start_note=(0, 0, 271), pan2=0.45, panx=2.45, panw=2.0),
        "0,0,272": Pan(start_note=(0, 0, 272), pan2=0.5, panx=2.5, panw=2.0),
        "0,0,273": Pan(start_note=(0, 0, 273), pan2=0.55, panx=2.55, panw=2.0),
        "0,0,274": Pan(start_note=(0, 0, 274), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,198": Pan(start_note=(0, 5, 198), pan2=0.7, panx=0.7, panw=2.0),
        # m115
        "0,0,275": Pan(start_note=(0, 0, 275), pan2=0.45, panx=2.45, panw=2.0),
        "0,0,276": Pan(start_note=(0, 0, 276), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,277": Pan(start_note=(0, 0, 277), pan2=0.35, panx=2.35, panw=2.0),
        "0,5,199": Pan(start_note=(0, 5, 199), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,200": Pan(start_note=(0, 5, 200), pan2=0.5, panx=2.5, panw=2.0),
        # m116
        "0,0,278": Pan(start_note=(0, 0, 278), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,201": Pan(start_note=(0, 5, 201), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,202": Pan(start_note=(0, 5, 202), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,203": Pan(start_note=(0, 5, 203), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,204": Pan(start_note=(0, 5, 204), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,205": Pan(start_note=(0, 5, 205), pan2=0.5, panx=0.5, panw=2.0),
        # m117
        "0,0,279": Pan(start_note=(0, 0, 279), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,280": Pan(start_note=(0, 0, 280), pan2=0.35, panx=2.35, panw=2.0),
        "0,5,206": Pan(start_note=(0, 5, 206), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,207": Pan(start_note=(0, 5, 207), pan2=0.5, panx=2.5, panw=2.0),
        # m119
        "0,0,281": Pan(start_note=(0, 0, 281), pan2=0.35, panx=2.35, panw=2.0),
        "0,0,282": Pan(start_note=(0, 0, 282), pan2=0.35, panx=2.35, panw=2.0),
        "0,0,283": Pan(start_note=(0, 0, 283), pan2=0.35, panx=2.35, panw=2.0),
        "0,0,284": Pan(start_note=(0, 0, 284), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,285": Pan(start_note=(0, 0, 285), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,286": Pan(start_note=(0, 0, 286), pan2=0.4, panx=2.4, panw=2.0),
        "0,1,24": Pan(start_note=(0, 1, 24), pan2=0.5, panx=2.5, panw=2.0),
        "0,1,25": Pan(start_note=(0, 1, 25), pan2=0.6, panx=2.6, panw=2.0),
        # m121
        "0,5,208": Pan(start_note=(0, 5, 208), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,209": Pan(start_note=(0, 5, 209), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,210": Pan(start_note=(0, 5, 210), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,211": Pan(start_note=(0, 5, 211), pan2=0.55, panx=2.45, panw=2.0),
        "0,5,212": Pan(start_note=(0, 5, 212), pan2=0.55, panx=2.45, panw=2.0),
        "0,5,213": Pan(start_note=(0, 5, 213), pan2=0.45, panx=0.45, panw=2.0),
        "0,6,43": Pan(start_note=(0, 6, 43), pan2=0.45, panx=0.45, panw=2.0),
        "0,6,44": Pan(start_note=(0, 6, 44), pan2=0.55, panx=2.55, panw=2.0),
        # m122
        "0,5,214": Pan(start_note=(0, 5, 214), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,215": Pan(start_note=(0, 5, 215), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,216": Pan(start_note=(0, 5, 216), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,217": Pan(start_note=(0, 5, 217), pan2=0.4, panx=0.4, panw=2.0),
        # m123
        "0,5,218": Pan(start_note=(0, 5, 218), pan2=0.75, panx=0.75, panw=2.0),
        "0,5,219": Pan(start_note=(0, 5, 219), pan2=0.7, panx=0.7, panw=2.0),
        "0,5,220": Pan(start_note=(0, 5, 220), pan2=0.75, panx=0.75, panw=2.0),
        "0,5,221": Pan(start_note=(0, 5, 221), pan2=0.75, panx=0.75, panw=2.0),
        # m124
        "0,5,222": Pan(start_note=(0, 5, 222), pan2=0.8, panx=0.8, panw=2.0),
        "0,5,223": Pan(start_note=(0, 5, 223), pan2=0.8, panx=0.8, panw=2.0),
        # m126
        "0,5,224": Pan(start_note=(0, 5, 224), pan2=0.7, panx=0.7, panw=2.0),
        "0,5,225": Pan(start_note=(0, 5, 225), pan2=0.75, panx=0.75, panw=2.0),
        "0,5,226": Pan(start_note=(0, 5, 226), pan2=0.7, panx=0.7, panw=2.0),
        "0,5,227": Pan(start_note=(0, 5, 227), pan2=0.75, panx=0.75, panw=2.0),
        "0,5,228": Pan(start_note=(0, 5, 228), pan2=0.75, panx=0.75, panw=2.0),
        "0,5,229": Pan(start_note=(0, 5, 229), pan2=0.7, panx=0.7, panw=2.0),
        "0,5,230": Pan(start_note=(0, 5, 230), pan2=0.75, panx=0.75, panw=2.0),
        # m127
        "0,5,231": Pan(start_note=(0, 5, 231), pan2=0.7, panx=0.7, panw=2.0),
        # m128
        "0,5,232": Pan(start_note=(0, 5, 232), pan2=0.65, panx=0.65, panw=2.0),
        # m129
        "0,5,233": Pan(start_note=(0, 5, 233), pan2=0.65, panx=0.65, panw=2.0),
        "0,5,234": Pan(start_note=(0, 5, 234), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,235": Pan(start_note=(0, 5, 235), pan2=0.6, panx=0.6, panw=2.0),
        # m130
        "0,5,236": Pan(start_note=(0, 5, 236), pan2=0.65, panx=0.65, panw=2.0),
        "0,5,237": Pan(start_note=(0, 5, 237), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,238": Pan(start_note=(0, 5, 238), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,239": Pan(start_note=(0, 5, 239), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,240": Pan(start_note=(0, 5, 240), pan2=0.5, panx=2.5, panw=2.0),
        "0,5,241": Pan(start_note=(0, 5, 241), pan2=0.5, panx=2.5, panw=2.0),
        "0,6,45": Pan(start_note=(0, 6, 45), pan2=0.7, panx=2.7, panw=2.0),
        "0,6,46": Pan(start_note=(0, 6, 46), pan2=0.7, panx=2.7, panw=2.0),
        # m131
        "0,5,242": Pan(start_note=(0, 5, 242), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,243": Pan(start_note=(0, 5, 243), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,244": Pan(start_note=(0, 5, 244), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,245": Pan(start_note=(0, 5, 245), pan2=0.45, panx=2.45, panw=2.0),
        "0,5,246": Pan(start_note=(0, 5, 246), pan2=0.4, panx=2.4, panw=2.0),
        "0,6,47": Pan(start_note=(0, 6, 47), pan2=0.75, panx=2.75, panw=2.0),
        "0,6,48": Pan(start_note=(0, 6, 48), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,49": Pan(start_note=(0, 6, 49), pan2=0.75, panx=0.75, panw=2.0),
        "0,6,50": Pan(start_note=(0, 6, 50), pan2=0.7, panx=2.7, panw=2.0),
        "0,6,51": Pan(start_note=(0, 6, 51), pan2=0.7, panx=2.7, panw=2.0),
        # m132
        "0,5,247": Pan(start_note=(0, 5, 247), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,248": Pan(start_note=(0, 5, 248), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,249": Pan(start_note=(0, 5, 249), pan2=0.4, panx=0.4, panw=2.0),
        "0,5,250": Pan(start_note=(0, 5, 250), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,251": Pan(start_note=(0, 5, 251), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,252": Pan(start_note=(0, 5, 252), pan2=0.6, panx=0.6, panw=2.0),
        "0,5,253": Pan(start_note=(0, 5, 253), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,254": Pan(start_note=(0, 5, 254), pan2=0.5, panx=0.5, panw=2.0),
        "0,6,52": Pan(start_note=(0, 6, 52), pan2=0.55, panx=0.55, panw=2.0),
        "0,6,53": Pan(start_note=(0, 6, 53), pan2=0.7, panx=0.7, panw=2.0),
        # m133
        "0,5,255": Pan(start_note=(0, 5, 254), pan2=0.5, panx=0.5, panw=2.0),
        "0,5,256": Pan(start_note=(0, 5, 255), pan2=0.45, panx=0.45, panw=2.0),
        # m134
        "0,5,257": Pan(start_note=(0, 5, 257), pan2=0.55, panx=2.55, panw=2.0),
        "0,5,258": Pan(start_note=(0, 5, 258), pan2=0.6, panx=2.6, panw=2.0),
        "0,5,259": Pan(start_note=(0, 5, 259), pan2=0.6, panx=2.6, panw=2.0),
        "0,5,260": Pan(start_note=(0, 5, 260), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,261": Pan(start_note=(0, 5, 261), pan2=0.45, panx=0.45, panw=2.0),
        "0,5,262": Pan(start_note=(0, 5, 262), pan2=0.6, panx=2.6, panw=2.0),
        "0,5,263": Pan(start_note=(0, 5, 263), pan2=0.6, panx=2.6, panw=2.0),
        # m135
        "0,5,264": Pan(start_note=(0, 5, 264), pan2=0.55, panx=2.55, panw=2.0),
        "0,5,265": Pan(start_note=(0, 5, 265), pan2=0.5, panx=0.5, panw=2.0),
        # m136
        "0,5,266": Pan(start_note=(0, 5, 266), pan2=0.5, panx=0.5, panw=2.0),
    }
    pan2 = {
        # m5
        "0,1,0": Pan(start_note=(0, 1, 0), pan2=0.55, panx=0.55, panw=2.0),
        "0,1,1": Pan(start_note=(0, 1, 1), pan2=0.55, panx=0.55, panw=2.0),
        "0,1,2": Pan(start_note=(0, 1, 2), pan2=0.5, panx=0.5, panw=2.0),
        "0,7,0": Pan(start_note=(0, 7, 0), pan2=0.7, panx=0.7, panw=2.0),
        # m6
        "0,1,3": Pan(start_note=(0, 1, 3), pan2=0.5, panx=0.5, panw=2.0),
        # m7
        "0,1,4": Pan(start_note=(0, 1, 4), pan2=0.55, panx=0.55, panw=2.0),
        "0,1,5": Pan(start_note=(0, 1, 5), pan2=0.6, panx=0.6, panw=2.0),
        "0,7,1": Pan(start_note=(0, 7, 1), pan2=0.7, panx=0.7, panw=2.0),
        # m8
        "0,0,0": Pan(start_note=(0, 0, 0), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,1": Pan(start_note=(0, 0, 1), pan2=0.4, panx=2.4, panw=2.0),
        "0,0,2": Pan(start_note=(0, 0, 2), pan2=0.3, panx=0.3, panw=2.0),
        "0,1,6": Pan(start_note=(0, 1, 6), pan2=0.5, panx=2.5, panw=2.0),
        "0,1,7": Pan(start_note=(0, 1, 7), pan2=0.5, panx=2.5, panw=2.0),
        "0,1,8": Pan(start_note=(0, 1, 8), pan2=0.7, panx=0.7, panw=2.0),
        # m10
        "0,1,9": Pan(start_note=(0, 1, 9), pan2=0.55, panx=0.55, panw=2.0),
        "0,1,10": Pan(start_note=(0, 1, 10), pan2=0.55, panx=0.55, panw=2.0),
        "0,2,0": Pan(start_note=(0, 2, 0), pan2=0.7, panx=0.7, panw=2.0),
        "0,7,2": Pan(start_note=(0, 7, 2), pan2=0.7, panx=0.7, panw=2.0),
        # m11
        "0,1,11": Pan(start_note=(0, 1, 11), pan2=0.5, panx=0.5, panw=2.0),
        "0,1,12": Pan(start_note=(0, 1, 12), pan2=0.5, panx=0.5, panw=2.0),
        "0,7,3": Pan(start_note=(0, 7, 3), pan2=0.7, panx=0.7, panw=2.0),
        "0,7,4": Pan(start_note=(0, 7, 4), pan2=0.75, panx=0.75, panw=2.0),
        "0,7,5": Pan(start_note=(0, 7, 5), pan2=0.75, panx=0.75, panw=2.0),
        "0,7,6": Pan(start_note=(0, 7, 6), pan2=0.7, panx=0.7, panw=2.0),
        # m12
        "0,1,13": Pan(start_note=(0, 1, 13), pan2=0.5, panx=2.7, panw=2.0),
        "0,7,7": Pan(start_note=(0, 7, 7), pan2=0.7, panx=2.5, panw=2.0),
        # m14
        "0,1,14": Pan(start_note=(0, 1, 14), pan2=0.5, panx=0.5, panw=2.0),
        "0,7,8": Pan(start_note=(0, 7, 8), pan2=0.65, panx=0.65, panw=2.0),
        # m15
        "0,1,15": Pan(start_note=(0, 1, 15), pan2=0.45, panx=0.45, panw=2.0),
        "0,1,16": Pan(start_note=(0, 1, 16), pan2=0.4, panx=0.4, panw=2.0),
        "0,2,1": Pan(start_note=(0, 2, 1), pan2=0.5, panx=0.5, panw=2.0),
        "0,2,2": Pan(start_note=(0, 2, 2), pan2=0.45, panx=0.45, panw=2.0),
        "0,3,0": Pan(start_note=(0, 3, 0), pan2=0.65, panx=0.65, panw=2.0),
        "0,3,1": Pan(start_note=(0, 3, 1), pan2=0.55, panx=0.55, panw=2.0),
        "0,4,0": Pan(start_note=(0, 4, 0), pan2=0.65, panx=0.65, panw=2.0),
        # m17
        "0,1,17": Pan(start_note=(0, 1, 17), pan2=0.3, panx=2.3, panw=2.0),
        "0,2,3": Pan(start_note=(0, 2, 3), pan2=0.4, panx=2.4, panw=2.0),
        "0,3,2": Pan(start_note=(0, 3, 2), pan2=0.5, panx=2.5, panw=2.0),
        "0,4,1": Pan(start_note=(0, 4, 1), pan2=0.6, panx=2.6, panw=2.0),
        "0,5,0": Pan(start_note=(0, 5, 0), pan2=0.7, panx=2.7, panw=2.0),
        # m18
        "0,1,18": Pan(start_note=(0, 1, 18), pan2=0.15, panx=2.85, panw=2.0),
        "0,2,4": Pan(start_note=(0, 2, 4), pan2=0.3, panx=2.7, panw=2.0),
        "0,3,3": Pan(start_note=(0, 3, 3), pan2=0.45, panx=2.55, panw=2.0),
        "0,4,2": Pan(start_note=(0, 4, 2), pan2=0.55, panx=2.45, panw=2.0),
        "0,5,1": Pan(start_note=(0, 5, 1), pan2=0.7, panx=2.3, panw=2.0),
        "0,6,0": Pan(start_note=(0, 6, 0), pan2=0.85, panx=2.15, panw=2.0),
        # m20
        "0,1,19": Pan(start_note=(0, 1, 19), pan2=0.6, panx=0.6, panw=2.0),
        "0,1,20": Pan(start_note=(0, 1, 20), pan2=0.6, panx=0.6, panw=2.0),
        # m21
        "0,1,21": Pan(start_note=(0, 1, 21), pan2=0.6, panx=0.6, panw=2.0),
        "0,1,22": Pan(start_note=(0, 1, 22), pan2=0.6, panx=0.6, panw=2.0),
        "0,2,5": Pan(start_note=(0, 2, 5), pan2=0.7, panx=0.7, panw=2.0),
        # m22
        "0,1,23": Pan(start_note=(0, 1, 23), pan2=0.6, panx=0.6, panw=2.0),
        # m23
        "0,1,24": Pan(start_note=(0, 1, 24), pan2=0.15, panx=0.15, panw=2.0),
        "0,2,6": Pan(start_note=(0, 2, 6), pan2=0.3, panx=0.3, panw=2.0),
        "0,3,4": Pan(start_note=(0, 3, 4), pan2=0.45, panx=0.45, panw=2.0),
        "0,4,3": Pan(start_note=(0, 4, 3), pan2=0.55, panx=0.55, panw=2.0),
        "0,5,2": Pan(start_note=(0, 5, 2), pan2=0.7, panx=0.7, panw=2.0),
        "0,6,1": Pan(start_note=(0, 6, 1), pan2=0.85, panx=0.85, panw=2.0),
    }
    pan1l = []
    pan2l = []

    for i in range(len(parsed_parts1[0])):
        for j in range(len(parsed_parts1[0][i])):
            if f"{0},{i},{j}" not in pan1:
                pan1[f"{0},{i},{j}"] = Pan(start_note=(0, i, j), pan2=0, panx=0.5)

    for i in range(len(parsed_parts2[0])):
        for j in range(len(parsed_parts2[0][i])):
            if f"{0},{i},{j}" not in pan2:
                pan2[f"{0},{i},{j}"] = Pan(start_note=(0, i, j), pan2=0, panx=0.5)

    for panner in pan1:
        pan1l.append(pan1[panner])
    for panner in pan2:
        pan2l.append(pan2[panner])

    # Dynamics to insert into the score
    dynamics1 = [
        # m1
        Dynamic(synth=3, levels=[d[2], d[5], d[1], 0, 0], times=[1 / 3, 2 / 3, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 0), end_note=(0, 0, 0), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[2], d[5], d[1], 0, 0], times=[1 / 3, 2 / 3, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 0), end_note=(0, 0, 0), voice_index=(0, 5)),

        # m3
        Dynamic(synth=3, levels=[d[2], d[2], d[0], 0, 0], times=[3 / 4, 1 / 4, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 1), end_note=(0, 5, 1), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[2], d[2], d[0], 0, 0], times=[3 / 4, 1 / 4, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 1), end_note=(0, 5, 1), voice_index=(0, 5)),

        # m5
        Dynamic(synth=3, levels=[d[3], d[4], d[2], 0, 0], times=[1 / 4, 3 / 4, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 2), end_note=(0, 0, 2), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[6], d[3], d[2], 0, 0], times=[1 / 3, 2 / 3, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 2), end_note=(0, 0, 2), voice_index=(0, 5)),

        # m7
        Dynamic(synth=2, levels=[d[2], d[1], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 3), end_note=(0, 5, 3), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[2], d[1], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 3), end_note=(0, 5, 3), voice_index=(0, 5)),

        # m9
        Dynamic(synth=3, levels=[d[2], d[3], d[3], 0, 0], times=[5 / 6, 1 / 6, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 4), end_note=(0, 5, 4), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[2], d[3], d[3], 0, 0], times=[5 / 6, 1 / 6, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 4), end_note=(0, 5, 4), voice_index=(0, 5)),

        # m10
        Dynamic(synth=2, levels=[d[4], d[1], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 5), end_note=(0, 0, 18), voice_index=(0, 0)),

        # m13
        Dynamic(synth=2, levels=[d[1], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 19), end_note=(0, 5, 5), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[1], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 19), end_note=(0, 5, 5), voice_index=(0, 5)),

        # m15
        Dynamic(synth=4, levels=[d[6], d[6], d[2], d[1], 0], times=[1/4, 5/8, 1/8, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 6), end_note=(0, 0, 20), voice_index=(0, 0)),
        Dynamic(synth=4, levels=[d[6], d[6], d[2], d[1], 0], times=[1/4, 5/8, 1/8, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 6), end_note=(0, 0, 20), voice_index=(0, 5)),

        # m21
        Dynamic(synth=3, levels=[d[5], d[1], d[1], 0, 0], times=[4/5, 1/5, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 12), end_note=(0, 3, 0), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[3], d[1], d[1], 0, 0], times=[4/5, 1/5, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 12), end_note=(0, 3, 0), voice_index=(0, 3)),
        Dynamic(synth=3, levels=[d[3], d[1], d[1], 0, 0], times=[4/5, 1/5, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 12), end_note=(0, 3, 0), voice_index=(0, 4)),
        Dynamic(synth=3, levels=[d[3], d[1], d[1], 0, 0], times=[4/5, 1/5, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 12), end_note=(0, 3, 0), voice_index=(0, 5)),

        # m23
        Dynamic(synth=4, levels=[d[1], d[4], d[4], d[1], 0], times=[3/10, 2/5, 3/10, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 13), end_note=(0, 3, 1), voice_index=(0, 0)),
        Dynamic(synth=4, levels=[d[1], d[4], d[4], d[1], 0], times=[3/10, 2/5, 3/10, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 13), end_note=(0, 3, 1), voice_index=(0, 3)),
        Dynamic(synth=4, levels=[d[1], d[4], d[4], d[1], 0], times=[3/10, 2/5, 3/10, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 13), end_note=(0, 3, 1), voice_index=(0, 4)),
        Dynamic(synth=5, levels=[d[1], d[4], d[4], d[2], d[4]], times=[69/410, 46/205, 69/410, 18/41, 0],
                curves=[0, 0, 0, 0], start_note=(0, 5, 13), end_note=(0, 5, 13), voice_index=(0, 5)),

        # m30
        Dynamic(synth=2, levels=[d[4], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 39), end_note=(0, 0, 39), voice_index=(0, 0)),

        # m33
        Dynamic(synth=2, levels=[d[4], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 47), end_note=(0, 0, 51), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[3], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 19), end_note=(0, 5, 19), voice_index=(0, 5)),

        # m36
        Dynamic(synth=2, levels=[d[6], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 66), end_note=(0, 0, 66), voice_index=(0, 0)),

        # m44
        Dynamic(synth=3, levels=[d[4], d[1], d[5], 0, 0], times=[3/8, 5/8, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 30), end_note=(0, 5, 32), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[4], d[1], d[5], 0, 0], times=[3/8, 5/8, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 30), end_note=(0, 5, 32), voice_index=(0, 5)),

        # m47
        Dynamic(synth=2, levels=[d[4], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 99), end_note=(0, 0, 111), voice_index=(0, 0)),

        # m48
        Dynamic(synth=3, levels=[d[5], d[2], d[2], 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 34), end_note=(0, 0, 113), voice_index=(0, 0)),
        Dynamic(synth=3, levels=[d[5], d[2], d[2], 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 34), end_note=(0, 0, 113), voice_index=(0, 3)),
        Dynamic(synth=3, levels=[d[5], d[2], d[2], 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 34), end_note=(0, 0, 113), voice_index=(0, 5)),
        Dynamic(synth=3, levels=[d[5], d[2], d[2], 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 34), end_note=(0, 0, 113), voice_index=(0, 7)),

        # m51
        Dynamic(synth=4, levels=[d[2], d[4], d[7], d[5], 0], times=[11/32, 149/32, 3/8, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 114), end_note=(0, 0, 116), voice_index=(0, 0)),
        Dynamic(synth=4, levels=[d[2], d[4], d[7], d[5], 0], times=[11/32, 149/32, 3/8, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 114), end_note=(0, 0, 116), voice_index=(0, 5)),

        # m54
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 40), end_note=(0, 5, 41), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 40), end_note=(0, 5, 41), voice_index=(0, 5)),

        # m58
        Dynamic(synth=2, levels=[d[4], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 51), end_note=(0, 5, 51), voice_index=(0, 5)),

        # m61
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 141), end_note=(0, 5, 58), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 141), end_note=(0, 5, 58), voice_index=(0, 5)),

        # m66
        Dynamic(synth=2, levels=[d[2], d[3], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 64), end_note=(0, 5, 68), voice_index=(0, 5)),

        # m67
        Dynamic(synth=2, levels=[d[4], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 70), end_note=(0, 5, 76), voice_index=(0, 5)),

        # m70
        Dynamic(synth=2, levels=[d[1], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 150), end_note=(0, 0, 150), voice_index=(0, 0)),

        # m72
        Dynamic(synth=2, levels=[d[3], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 151), end_note=(0, 0, 151), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[3], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 151), end_note=(0, 0, 151), voice_index=(0, 5)),

        # m76
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 88), end_note=(0, 5, 88), voice_index=(0, 5)),

        # m77
        Dynamic(synth=2, levels=[d[6], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 92), end_note=(0, 5, 92), voice_index=(0, 5)),

        # m79
        Dynamic(synth=5, levels=[d[7], d[9], d[7], d[9], d[9]], times=[11/34, 4/17, 4/17, 7/34, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 93), end_note=(0, 5, 98), voice_index=(0, 5)),

        # m83
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 182), end_note=(0, 0, 189), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 182), end_note=(0, 0, 189), voice_index=(0, 1)),

        # m85
        Dynamic(synth=2, levels=[d[7], d[9], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 193), end_note=(0, 0, 195), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[7], d[9], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 193), end_note=(0, 0, 195), voice_index=(0, 1)),

        # m86
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 200), end_note=(0, 0, 203), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 200), end_note=(0, 0, 203), voice_index=(0, 1)),

        # m87
        Dynamic(synth=2, levels=[d[8], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 207), end_note=(0, 5, 99), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[8], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 207), end_note=(0, 5, 99), voice_index=(0, 1)),
        Dynamic(synth=2, levels=[d[8], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 207), end_note=(0, 5, 99), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[8], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 207), end_note=(0, 5, 99), voice_index=(0, 6)),

        # m89
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 100), end_note=(0, 5, 100), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 100), end_note=(0, 5, 100), voice_index=(0, 1)),
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 100), end_note=(0, 5, 100), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 100), end_note=(0, 5, 100), voice_index=(0, 6)),

        # m92
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 106), end_note=(0, 5, 109), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 106), end_note=(0, 5, 109), voice_index=(0, 6)),

        # m93
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 112), end_note=(0, 5, 115), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 112), end_note=(0, 5, 115), voice_index=(0, 6)),

        # m94
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 119), end_note=(0, 0, 224), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 119), end_note=(0, 0, 224), voice_index=(0, 5)),

        # m97
        Dynamic(synth=2, levels=[d[4], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 125), end_note=(0, 5, 130), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[4], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 125), end_note=(0, 5, 130), voice_index=(0, 6)),

        # m98
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 135), end_note=(0, 5, 139), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 135), end_note=(0, 5, 139), voice_index=(0, 6)),

        # m100
        Dynamic(synth=3, levels=[d[6], d[9], d[8], 0, 0], times=[1/2, 1/2, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 140), end_note=(0, 5, 140), voice_index=(0, 5)),

        # m102
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 245), end_note=(0, 0, 248), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[7], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 245), end_note=(0, 0, 248), voice_index=(0, 5)),

        # m106
        Dynamic(synth=2, levels=[d[3], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 158), end_note=(0, 5, 162), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[3], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 158), end_note=(0, 5, 162), voice_index=(0, 6)),

        # m107
        Dynamic(synth=2, levels=[d[6], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 165), end_note=(0, 5, 171), voice_index=(0, 5)),

        # m109
        Dynamic(synth=2, levels=[d[6], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 176), end_note=(0, 5, 185), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[6], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 176), end_note=(0, 5, 185), voice_index=(0, 6)),

        # m112
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 254), end_note=(0, 5, 195), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 254), end_note=(0, 5, 195), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[5], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 254), end_note=(0, 5, 195), voice_index=(0, 6)),

        # m114
        Dynamic(synth=2, levels=[d[4], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 270), end_note=(0, 0, 274), voice_index=(0, 0)),

        # m115
        Dynamic(synth=2, levels=[d[8], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 275), end_note=(0, 0, 277), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[8], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 0, 275), end_note=(0, 0, 277), voice_index=(0, 5)),

        # m116
        Dynamic(synth=2, levels=[d[8], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 201), end_note=(0, 5, 205), voice_index=(0, 0)),
        Dynamic(synth=2, levels=[d[8], d[5], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 201), end_note=(0, 5, 205), voice_index=(0, 5)),

        # m126
        Dynamic(synth=2, levels=[d[3], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 226), end_note=(0, 5, 229), voice_index=(0, 5)),

        # m126
        Dynamic(synth=2, levels=[d[4], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 230), end_note=(0, 5, 230), voice_index=(0, 5)),

        # m127
        Dynamic(synth=2, levels=[d[6], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 231), end_note=(0, 5, 231), voice_index=(0, 5)),

        # m128
        Dynamic(synth=2, levels=[d[5], d[6], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 232), end_note=(0, 5, 233), voice_index=(0, 5)),

        # m132
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 247), end_note=(0, 5, 251), voice_index=(0, 5)),
        Dynamic(synth=2, levels=[d[7], d[8], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 247), end_note=(0, 5, 251), voice_index=(0, 6)),

        # m136
        Dynamic(synth=2, levels=[d[7], d[4], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 5, 266), end_note=(0, 5, 266), voice_index=(0, 5))
    ]

    dynamics2 = [
        # m5
        Dynamic(synth=3, levels=[d[3], d[5], d[3], 0, 0], times=[6/11, 5/11, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 1, 0), end_note=(0, 7, 0), voice_index=(0, 1)),
        Dynamic(synth=3, levels=[d[3], d[5], d[3], 0, 0], times=[6/11, 5/11, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 1, 0), end_note=(0, 7, 0), voice_index=(0, 7)),

        # m10
        Dynamic(synth=2, levels=[d[3], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 1, 9), end_note=(0, 1, 9), voice_index=(0, 1)),
        Dynamic(synth=2, levels=[d[3], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 1, 9), end_note=(0, 1, 9), voice_index=(0, 2)),

        # m10
        Dynamic(synth=2, levels=[d[1], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 1, 10), end_note=(0, 1, 10), voice_index=(0, 1)),
        Dynamic(synth=2, levels=[d[1], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 1, 10), end_note=(0, 1, 10), voice_index=(0, 7)),

        # m14
        Dynamic(synth=2, levels=[d[1], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 7, 8), end_note=(0, 7, 8), voice_index=(0, 1)),
        Dynamic(synth=2, levels=[d[1], d[2], 0, 0, 0], times=[1, 0, 0, 0, 0], curves=[0, 0, 0, 0],
                start_note=(0, 7, 8), end_note=(0, 7, 8), voice_index=(0, 7))
    ]

    # A data structure that holds conversion information for FM synths. Index 1 holds the synth index in the score,
    # Index 2 is the new synth index, Index 3 is the dynamic values for the envelope, Index 4 is the time points
    # (excluding start) where dynamic peaks and valleys are, and Index 5 is the list of envelope curves.
    # The envelope times will be calculated automatically from Index 4. The values in Index 4 must sum to 1.
    synth_updates1 = [
        [[0, 0, 0], 10, [0.2, 0.5, 0.2], [0.375, 0.625], [0, 0]],
        # time is 1 because it takes the entire duration of the synth to get from beginning to end of the
        # timbre envelope
        [[0, 0, 1], 10, [0.5, 0.2], [1], [0]],
        [[0, 0, 2], 10, [0.3, 0.1], [1], [0]],
        [[0, 0, 3], 10, [0.3, 0.5, 0.35], [0.5, 0.5], [0, 0]],
        [[0, 0, 4], 10, [0.2, 0.3], [1], [0]],
        [[0, 5, 0], 10, [0.2, 0.5, 0.2], [0.571428, 0.428572], [0, 0]],
        [[0, 5, 1], 10, [0.4, 0.05], [1], [0]],
        [[0, 5, 2], 10, [0.3, 0.1], [1], [0]],
        [[0, 5, 3], 10, [0.5, 0.2], [1], [0]],
        [[0, 5, 4], 10, [0.25, 0.4], [1], [0]],

        # m13
        [[0, 0, 19], 10, [0.05, 0.1], [1], [0]],
        [[0, 5, 5], 10, [0.06, 0.11], [1], [0]],

        # m15
        [[0, 0, 20], 10, [0.5, 0.2], [1], [0]],
        [[0, 5, 6], 10, [0.5, 0.35], [1], [0]],

        # m16
        [[0, 5, 7], 10, [0.35, 0.2], [1], [0]],

        # m20
        [[0, 5, 11], 10, [0.3, 0.25], [1], [0]],

        # m21
        [[0, 0, 21], 10, [0.03, 0.01], [1], [0]],
        [[0, 3, 0], 10, [0.03, 0.011], [1], [0]],
        [[0, 4, 0], 10, [0.03, 0.011], [1], [0]],
        [[0, 5, 12], 10, [0.4, 0.1], [1], [0]],

        # m23
        [[0, 0, 22], 10, [0.02, 0.02], [1], [0]],
        [[0, 3, 1], 10, [0.02, 0.02], [1], [0]],
        [[0, 4, 1], 10, [0.02, 0.02], [1], [0]],
        [[0, 5, 13], 10, [0.1, 0.1], [1], [0]],

        # m29
        [[0, 0, 36], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 16], 10, [0.5, 0.5], [1], [0]],

        # m30
        [[0, 0, 39], 10, [0.5, 0.5], [1], [0]],
        [[0, 5, 18], 10, [0.5, 0.5], [1], [0]],

        # m33
        [[0, 0, 49], 10, [0.3, 0.3], [1], [0]],
        [[0, 0, 51], 10, [0.1, 0.3], [1], [0]],
        [[0, 5, 19], 10, [0.3, 0.45], [1], [0]],

        # m41-48
        [[0, 0, 90], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 91], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 92], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 93], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 96], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 97], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 98], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 25], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 26], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 27], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 28], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 30], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 32], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 33], 10, [0.2, 0.3], [1], [0]],
        [[0, 7, 0], 10, [0.2, 0.3], [1], [0]],

        # m48-55
        [[0, 0, 112], 10, [0.2, 0.1], [1], [0]],
        [[0, 0, 114], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 115], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 116], 10, [0.01, 0.01], [1], [0]],
        [[0, 0, 117], 10, [0.01, 0.01], [1], [0]],
        [[0, 3, 5], 10, [0.2, 0.1], [1], [0]],
        [[0, 0, 90], 10, [0.2, 0.5], [1], [0]],
        [[0, 5, 34], 10, [0.35, 0.2], [1], [0]],
        [[0, 5, 35], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 37], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 40], 10, [0.01, 0.01], [1], [0]],
        [[0, 5, 41], 10, [0.01, 0.01], [1], [0]],
        [[0, 7, 1], 10, [0.35, 0.2], [1], [0]],

        # m58
        [[0, 0, 135], 10, [0.08, 0.1], [1], [0]],
        [[0, 5, 51], 10, [0.05, 0.1], [1], [0]],

        # m68-75
        [[0, 0, 147], 10, [0.6, 0.6], [1], [0]],
        [[0, 0, 150], 10, [0.3, 0.5], [1], [0]],
        [[0, 0, 151], 10, [0.4, 0.5], [1], [0]],
        [[0, 5, 77], 10, [0.7, 0.7], [1], [0]],
        [[0, 5, 78], 10, [0.6, 0.6], [1], [0]],
        [[0, 5, 84], 10, [0.43, 0.55], [1], [0]],
        [[0, 5, 87], 10, [0.3, 0.3], [1], [0]],
        [[0, 6, 1], 10, [0.7, 0.7], [1], [0]],

        # m76-78
        [[0, 5, 88], 10, [0.2, 0.5, 0.35], [0.7, 0.3], [0, 0]],
        [[0, 5, 92], 10, [0.5, 0.6], [1], [0]],
        [[0, 7, 4], 10, [0.4, 0.4], [1], [0]],

        # m79-81
        [[0, 5, 95], 10, [0.3, 0.3], [1], [0]],
        [[0, 5, 96], 10, [0.5, 0.5], [1], [0]],
        [[0, 5, 97], 10, [0.3, 0.3], [1], [0]],
        [[0, 5, 98], 10, [0.5, 0.5], [1], [0]],

        # m87-90
        [[0, 0, 207], 10, [0.1, 0.03], [1], [0]],
        [[0, 1, 16], 10, [0.1, 0.03], [1], [0]],
        [[0, 5, 99], 10, [0.18, 0.04], [1], [0]],
        [[0, 5, 100], 10, [0.4, 0.5], [1], [0]],
        [[0, 6, 2], 10, [0.18, 0.04], [1], [0]],
        [[0, 6, 3], 10, [0.4, 0.5], [1], [0]],
        [[0, 0, 212], 10, [0.2, 0.25], [1], [0]],
        [[0, 1, 21], 10, [0.2, 0.25], [1], [0]],

        # m100-103
        [[0, 0, 244], 10, [0.1, 0.2], [1], [0]],
        [[0, 1, 23], 10, [0.1, 0.2], [1], [0]],
        [[0, 5, 140], 10, [0.2, 0.5, 0.4], [0.7, 0.3], [0, 0]],
        [[0, 5, 142], 10, [0.3, 0.3], [1], [0]],

        # m116-118
        [[0, 0, 275], 10, [0.1, 0.02], [1], [0]],
        [[0, 0, 278], 10, [0.05, 0.06], [1], [0]],
        [[0, 0, 279], 10, [0.06, 0.05], [1], [0]],
        [[0, 5, 200], 10, [0.04, 0.02], [1], [0]],
        [[0, 5, 207], 10, [0.06, 0.055], [1], [0]],

        # m127-129
        [[0, 5, 230], 10, [0.4, 0.5], [1], [0]],
        [[0, 5, 231], 10, [0.6, 0.45], [1], [0]],
        [[0, 5, 232], 10, [0.2, 0.3], [1], [0]],

        # m137
        [[0, 5, 266], 10, [0.5, 0.4], [1], [0]],
    ]

    synth_updates2 = [
        # m5-7
        [[0, 1, 0], 10, [0.2, 0.3], [1], [0]],
        [[0, 1, 1], 10, [0.3, 0.4], [1], [0]],
        [[0, 1, 3], 10, [0.3, 0.2], [1], [0]],
        [[0, 7, 0], 10, [0.2, 0.5, 0.2], [0.55, 0.45], [0, 0]],
        [[0, 7, 1], 10, [0.4, 0.4], [1], [0]],

        # m10-11
        [[0, 1, 9], 10, [0.5, 0.4], [1], [0]],
        [[0, 1, 10], 10, [0.2, 0.3], [1], [0]],
        [[0, 2, 0], 10, [0.5, 0.4], [1], [0]],
        [[0, 7, 2], 10, [0.2, 0.25], [1], [0]],
        [[0, 7, 3], 10, [0.25, 0.3], [1], [0]],

        # m14
        [[0, 1, 14], 10, [0.12, 0.15], [1], [0]],
        [[0, 7, 8], 10, [0.05, 0.15], [1], [0]],

        # m17
        [[0, 1, 17], 10, [0.2, 0.2], [1], [0]],
        [[0, 2, 3], 10, [0.2, 0.2], [1], [0]],
        [[0, 3, 2], 10, [0.2, 0.2], [1], [0]],
        [[0, 4, 1], 10, [0.2, 0.2], [1], [0]],
        [[0, 5, 0], 10, [0.2, 0.2], [1], [0]],

        # m23
        [[0, 1, 24], 10, [0.2, 0.2], [1], [0]],
        [[0, 2, 6], 10, [0.2, 0.2], [1], [0]],
        [[0, 3, 4], 10, [0.2, 0.2], [1], [0]],
        [[0, 4, 3], 10, [0.2, 0.2], [1], [0]],
        [[0, 5, 2], 10, [0.2, 0.2], [1], [0]],
        [[0, 6, 1], 10, [0.2, 0.2], [1], [0]],
    ]

    batch_fm_synth_update(parsed_parts1, synth_updates1)
    batch_fm_synth_update(parsed_parts2, synth_updates2)

    # adjust dynamics of individual notes
    # m25
    parsed_parts1[0][0][23].mul *= d[3]
    parsed_parts1[0][0][24].mul *= d[6]
    parsed_parts1[0][0][25].mul *= d[4]
    # m27
    parsed_parts1[0][0][26].mul *= d[3]
    parsed_parts1[0][0][27].mul *= d[5]
    parsed_parts1[0][0][28].mul *= d[4]
    parsed_parts1[0][0][29].mul *= d[3]
    parsed_parts1[0][0][30].mul *= d[5]
    parsed_parts1[0][0][31].mul *= d[8]
    parsed_parts1[0][0][32].mul *= d[9]
    parsed_parts1[0][0][33].mul *= d[8]
    parsed_parts1[0][0][34].mul *= d[9]
    parsed_parts1[0][0][35].mul *= d[6]
    # m29
    parsed_parts1[0][0][36].mul *= d[2]
    parsed_parts1[0][0][37].mul *= d[3]
    # m30
    parsed_parts1[0][0][38].mul *= d[4]
    # m32
    parsed_parts1[0][0][40].mul *= d[2]
    parsed_parts1[0][0][41].mul *= d[3]
    parsed_parts1[0][0][42].mul *= d[4]
    parsed_parts1[0][0][43].mul *= d[5]
    parsed_parts1[0][0][44].mul *= d[3]
    parsed_parts1[0][0][45].mul *= d[5]
    parsed_parts1[0][0][46].mul *= d[6]
    # m35
    parsed_parts1[0][0][52].mul *= d[6]
    parsed_parts1[0][0][53].mul *= d[7]
    parsed_parts1[0][0][54].mul *= d[7]
    parsed_parts1[0][0][55].mul *= d[8]
    # m36
    parsed_parts1[0][0][56].mul *= d[8]
    parsed_parts1[0][0][57].mul *= d[8]
    parsed_parts1[0][0][58].mul *= d[8]
    parsed_parts1[0][0][59].mul *= d[6]
    parsed_parts1[0][0][60].mul *= d[6]
    parsed_parts1[0][0][61].mul *= d[6]
    parsed_parts1[0][0][62].mul *= d[6]
    parsed_parts1[0][0][63].mul *= d[7]
    parsed_parts1[0][0][64].mul *= d[7]
    parsed_parts1[0][0][65].mul *= d[7]
    # m37
    parsed_parts1[0][0][67].mul *= d[6]
    parsed_parts1[0][0][68].mul *= d[5]
    parsed_parts1[0][0][69].mul *= d[6]
    parsed_parts1[0][0][70].mul *= d[4]
    # m38
    parsed_parts1[0][0][71].mul *= d[4]
    parsed_parts1[0][0][72].mul *= d[6]
    parsed_parts1[0][0][73].mul *= d[5]
    parsed_parts1[0][0][74].mul *= d[5]
    parsed_parts1[0][0][75].mul *= d[5]
    # m39
    parsed_parts1[0][0][76].mul *= d[4]
    parsed_parts1[0][0][77].mul *= d[5]
    parsed_parts1[0][0][78].mul *= d[6]
    parsed_parts1[0][0][79].mul *= d[6]
    parsed_parts1[0][0][80].mul *= d[7]
    parsed_parts1[0][0][81].mul *= d[7]
    parsed_parts1[0][0][82].mul *= d[8]
    parsed_parts1[0][0][83].mul *= d[9]
    parsed_parts1[0][0][84].mul *= d[8]
    # m40
    parsed_parts1[0][0][85].mul *= d[8]
    parsed_parts1[0][0][86].mul *= d[8]
    parsed_parts1[0][0][87].mul *= d[9]
    parsed_parts1[0][0][88].mul *= d[9]
    parsed_parts1[0][0][89].mul *= d[9]
    # m41
    parsed_parts1[0][0][90].mul *= d[2]
    parsed_parts1[0][0][91].mul *= d[2]
    # m42
    parsed_parts1[0][0][92].mul *= d[2]
    parsed_parts1[0][0][93].mul *= d[2]
    # m43
    parsed_parts1[0][0][94].mul *= d[2]
    # m56
    parsed_parts1[0][0][118].mul *= d[7]
    parsed_parts1[0][0][119].mul *= d[7]
    parsed_parts1[0][0][120].mul *= d[6]
    parsed_parts1[0][0][121].mul *= d[6]
    parsed_parts1[0][0][122].mul *= d[5]
    parsed_parts1[0][0][123].mul *= d[7]
    parsed_parts1[0][0][124].mul *= d[7]
    # m57
    parsed_parts1[0][0][125].mul *= d[8]
    parsed_parts1[0][0][126].mul *= d[8]
    parsed_parts1[0][0][127].mul *= d[6]
    parsed_parts1[0][0][128].mul *= d[6]
    parsed_parts1[0][0][129].mul *= d[8]
    # m58
    parsed_parts1[0][0][130].mul *= d[5]
    parsed_parts1[0][0][131].mul *= d[5]
    parsed_parts1[0][0][132].mul *= d[5]
    parsed_parts1[0][0][133].mul *= d[7]
    parsed_parts1[0][0][134].mul *= d[3]
    parsed_parts1[0][0][135].mul *= d[2]
    # m60
    parsed_parts1[0][0][136].mul *= d[4]
    parsed_parts1[0][0][137].mul *= d[4]
    parsed_parts1[0][0][138].mul *= d[5]
    parsed_parts1[0][0][139].mul *= d[5]
    parsed_parts1[0][0][140].mul *= d[6]
    # m61
    parsed_parts1[0][0][146].mul *= d[9]
    # m69
    parsed_parts1[0][0][147].mul *= d[2]
    # m70
    parsed_parts1[0][0][148].mul *= d[4]
    parsed_parts1[0][0][149].mul *= d[4]
    # m73
    parsed_parts1[0][0][152].mul *= d[7]
    parsed_parts1[0][0][153].mul *= d[7]
    # m75
    parsed_parts1[0][0][154].mul *= d[5]
    parsed_parts1[0][0][155].mul *= d[5]
    parsed_parts1[0][0][156].mul *= d[5]
    # m76
    parsed_parts1[0][0][157].mul *= d[5]
    parsed_parts1[0][0][158].mul *= d[8]
    parsed_parts1[0][0][159].mul *= d[6]
    parsed_parts1[0][0][160].mul *= d[6]
    parsed_parts1[0][0][161].mul *= d[8]
    # m77
    parsed_parts1[0][0][162].mul *= d[7]
    parsed_parts1[0][0][163].mul *= d[7]
    parsed_parts1[0][0][164].mul *= d[7]
    parsed_parts1[0][0][165].mul *= d[7]
    # m79
    parsed_parts1[0][0][166].mul *= d[7]
    parsed_parts1[0][0][167].mul *= d[8]
    parsed_parts1[0][0][168].mul *= d[9]
    parsed_parts1[0][0][169].mul *= d[8]
    # m80
    parsed_parts1[0][0][170].mul *= d[7]
    parsed_parts1[0][0][171].mul *= d[8]
    parsed_parts1[0][0][172].mul *= d[9]
    parsed_parts1[0][0][173].mul *= d[7]
    parsed_parts1[0][0][174].mul *= d[9]
    # m81
    parsed_parts1[0][0][175].mul *= d[9]
    parsed_parts1[0][0][176].mul *= d[9]
    parsed_parts1[0][0][177].mul *= d[6]
    parsed_parts1[0][0][178].mul *= d[6]
    parsed_parts1[0][0][179].mul *= d[7]
    # m82
    parsed_parts1[0][0][180].mul *= d[8]
    parsed_parts1[0][0][181].mul *= d[8]
    # m84
    parsed_parts1[0][0][190].mul *= d[8]
    parsed_parts1[0][0][191].mul *= d[8]
    parsed_parts1[0][0][192].mul *= d[8]
    # m85
    parsed_parts1[0][0][196].mul *= d[9]
    # m86
    parsed_parts1[0][0][197].mul *= d[6]
    parsed_parts1[0][0][198].mul *= d[6]
    parsed_parts1[0][0][199].mul *= d[6]

    parsed_parts1[0][0][204].mul *= d[9]
    # m87
    parsed_parts1[0][0][205].mul *= d[7]
    parsed_parts1[0][0][206].mul *= d[7]
    # m90
    parsed_parts1[0][0][210].mul *= d[7]
    parsed_parts1[0][0][211].mul *= d[8]
    parsed_parts1[0][0][212].mul *= d[8]
    # m91
    parsed_parts1[0][0][213].mul *= d[9]
    parsed_parts1[0][0][214].mul *= d[9]
    parsed_parts1[0][0][215].mul *= d[9]
    parsed_parts1[0][0][216].mul *= d[9]
    parsed_parts1[0][0][217].mul *= d[9]
    # m94
    parsed_parts1[0][0][225].mul *= d[8]
    parsed_parts1[0][0][226].mul *= d[8]
    parsed_parts1[0][0][227].mul *= d[8]
    parsed_parts1[0][0][228].mul *= d[8]
    # m99
    parsed_parts1[0][0][229].mul *= d[4]
    parsed_parts1[0][0][230].mul *= d[5]
    parsed_parts1[0][0][231].mul *= d[6]
    parsed_parts1[0][0][232].mul *= d[6]
    parsed_parts1[0][0][233].mul *= d[6]
    # m100
    parsed_parts1[0][0][234].mul *= d[8]
    parsed_parts1[0][0][235].mul *= d[6]
    parsed_parts1[0][0][236].mul *= d[8]
    parsed_parts1[0][0][237].mul *= d[6]
    parsed_parts1[0][0][238].mul *= d[6]
    parsed_parts1[0][0][239].mul *= d[7]
    # m101
    parsed_parts1[0][0][240].mul *= d[8]
    parsed_parts1[0][0][241].mul *= d[8]
    parsed_parts1[0][0][242].mul *= d[8]
    parsed_parts1[0][0][243].mul *= d[8]
    parsed_parts1[0][0][244].mul *= d[9]
    # m103
    parsed_parts1[0][0][249].mul *= d[8]
    parsed_parts1[0][0][250].mul *= d[8]
    parsed_parts1[0][0][251].mul *= d[8]
    parsed_parts1[0][0][252].mul *= d[8]
    parsed_parts1[0][0][253].mul *= d[8]
    # m113
    parsed_parts1[0][0][263].mul *= d[8]
    parsed_parts1[0][0][264].mul *= d[8]
    parsed_parts1[0][0][265].mul *= d[6]
    # m114
    parsed_parts1[0][0][266].mul *= d[6]
    parsed_parts1[0][0][267].mul *= d[6]
    parsed_parts1[0][0][268].mul *= d[5]
    parsed_parts1[0][0][269].mul *= d[5]
    # m117
    parsed_parts1[0][0][279].mul *= d[7]
    parsed_parts1[0][0][280].mul *= d[7]
    # m119
    parsed_parts1[0][0][281].mul *= d[8]
    parsed_parts1[0][0][282].mul *= d[8]
    parsed_parts1[0][0][283].mul *= d[9]
    parsed_parts1[0][0][284].mul *= d[9]
    parsed_parts1[0][0][285].mul *= d[9]
    parsed_parts1[0][0][286].mul *= d[7]

    # m56
    parsed_parts1[0][1][0].mul *= d[7]
    parsed_parts1[0][1][1].mul *= d[7]
    parsed_parts1[0][1][2].mul *= d[5]
    # m57
    parsed_parts1[0][1][3].mul *= d[8]
    # m60
    parsed_parts1[0][1][4].mul *= d[6]
    # m76
    parsed_parts1[0][1][5].mul *= d[5]
    parsed_parts1[0][1][6].mul *= d[6]
    parsed_parts1[0][1][7].mul *= d[6]
    # m82
    parsed_parts1[0][1][8].mul *= d[8]
    # m84
    parsed_parts1[0][1][10].mul *= d[8]
    parsed_parts1[0][1][11].mul *= d[8]
    # m85
    parsed_parts1[0][1][13].mul *= d[9]
    # m86
    parsed_parts1[0][1][15].mul *= d[9]
    # m90
    parsed_parts1[0][1][19].mul *= d[7]
    parsed_parts1[0][1][20].mul *= d[8]
    parsed_parts1[0][1][21].mul *= d[8]
    # m101
    parsed_parts1[0][1][22].mul *= d[8]
    parsed_parts1[0][1][23].mul *= d[9]
    # m119
    parsed_parts1[0][1][24].mul *= d[9]
    parsed_parts1[0][1][25].mul *= d[7]

    # m58
    parsed_parts1[0][2][0].mul *= d[8]

    # m34
    parsed_parts1[0][3][2].mul *= d[7]
    parsed_parts1[0][3][3].mul *= d[7]
    # m35
    parsed_parts1[0][3][4].mul *= d[7]

    # m20
    parsed_parts1[0][5][8].mul *= d[5]
    parsed_parts1[0][5][9].mul *= d[3]
    parsed_parts1[0][5][10].mul *= d[5]
    parsed_parts1[0][5][11].mul *= d[3]
    # m29
    parsed_parts1[0][5][14].mul *= d[3]
    parsed_parts1[0][5][15].mul *= d[4]
    parsed_parts1[0][5][16].mul *= d[2]
    # m30
    parsed_parts1[0][5][17].mul *= d[5]
    parsed_parts1[0][5][18].mul *= d[4]
    # m34
    parsed_parts1[0][5][20].mul *= d[7]
    parsed_parts1[0][5][21].mul *= d[7]
    parsed_parts1[0][5][22].mul *= d[7]
    # m38
    parsed_parts1[0][5][23].mul *= d[5]
    # m39
    parsed_parts1[0][5][24].mul *= d[4]
    # m43
    parsed_parts1[0][5][29].mul *= d[4]
    # m47
    parsed_parts1[0][5][33].mul *= d[5]
    # m56
    parsed_parts1[0][5][42].mul *= d[7]
    parsed_parts1[0][5][43].mul *= d[5]
    parsed_parts1[0][5][44].mul *= d[5]
    parsed_parts1[0][5][45].mul *= d[5]
    parsed_parts1[0][5][46].mul *= d[5]
    parsed_parts1[0][5][47].mul *= d[5]
    # m57
    parsed_parts1[0][5][48].mul *= d[8]
    parsed_parts1[0][5][49].mul *= d[6]
    parsed_parts1[0][5][50].mul *= d[8]
    # m60
    parsed_parts1[0][5][52].mul *= d[4]
    parsed_parts1[0][5][53].mul *= d[4]
    parsed_parts1[0][5][54].mul *= d[5]
    parsed_parts1[0][5][55].mul *= d[6]
    # m61
    parsed_parts1[0][5][59].mul *= d[9]
    # m63
    parsed_parts1[0][5][60].mul *= d[3]
    parsed_parts1[0][5][61].mul *= d[3]
    # m65
    parsed_parts1[0][5][62].mul *= d[5]
    parsed_parts1[0][5][63].mul *= d[5]
    # m66
    parsed_parts1[0][5][69].mul *= d[5]
    # m68
    parsed_parts1[0][5][77].mul *= d[6]
    # m69
    parsed_parts1[0][5][78].mul *= d[2]
    # m70
    parsed_parts1[0][5][79].mul *= d[1]
    # m71
    parsed_parts1[0][5][80].mul *= d[1]
    parsed_parts1[0][5][81].mul *= d[2]
    # m72
    parsed_parts1[0][5][82].mul *= d[5]
    parsed_parts1[0][5][83].mul *= d[5]
    # m73
    parsed_parts1[0][5][85].mul *= d[7]
    parsed_parts1[0][5][86].mul *= d[7]
    # m75
    parsed_parts1[0][5][87].mul *= d[5]
    # m77
    parsed_parts1[0][5][89].mul *= d[6]
    parsed_parts1[0][5][90].mul *= d[6]
    parsed_parts1[0][5][91].mul *= d[6]
    # m89
    parsed_parts1[0][5][101].mul *= d[8]
    parsed_parts1[0][5][102].mul *= d[8]
    parsed_parts1[0][5][103].mul *= d[8]
    # m90
    parsed_parts1[0][5][104].mul *= d[8]
    parsed_parts1[0][5][105].mul *= d[8]
    # m92
    parsed_parts1[0][5][110].mul *= d[9]
    parsed_parts1[0][5][111].mul *= d[9]
    # m93
    parsed_parts1[0][5][116].mul *= d[8]
    parsed_parts1[0][5][117].mul *= d[8]
    parsed_parts1[0][5][118].mul *= d[8]
    # m96
    parsed_parts1[0][5][121].mul *= d[7]
    parsed_parts1[0][5][122].mul *= d[3]
    parsed_parts1[0][5][123].mul *= d[4]
    parsed_parts1[0][5][124].mul *= d[4]
    # m98
    parsed_parts1[0][5][131].mul *= d[6]
    parsed_parts1[0][5][132].mul *= d[6]
    parsed_parts1[0][5][133].mul *= d[6]
    parsed_parts1[0][5][134].mul *= d[6]
    # m101
    parsed_parts1[0][5][141].mul *= d[9]
    # m104
    parsed_parts1[0][5][145].mul *= d[4]
    parsed_parts1[0][5][146].mul *= d[5]
    # m105
    parsed_parts1[0][5][147].mul *= d[6]
    parsed_parts1[0][5][148].mul *= d[5]
    parsed_parts1[0][5][149].mul *= d[4]
    parsed_parts1[0][5][150].mul *= d[4]
    parsed_parts1[0][5][151].mul *= d[5]
    parsed_parts1[0][5][152].mul *= d[6]
    parsed_parts1[0][5][153].mul *= d[4]
    parsed_parts1[0][5][154].mul *= d[4]
    # m106
    parsed_parts1[0][5][155].mul *= d[3]
    parsed_parts1[0][5][156].mul *= d[3]
    parsed_parts1[0][5][157].mul *= d[3]

    parsed_parts1[0][5][163].mul *= d[4]
    parsed_parts1[0][5][164].mul *= d[4]
    # m108
    parsed_parts1[0][5][172].mul *= d[8]
    parsed_parts1[0][5][173].mul *= d[8]
    # m109
    parsed_parts1[0][5][174].mul *= d[6]
    parsed_parts1[0][5][175].mul *= d[6]
    # m110
    parsed_parts1[0][5][186].mul *= d[9]
    parsed_parts1[0][5][187].mul *= d[9]
    # m111
    parsed_parts1[0][5][188].mul *= d[9]
    parsed_parts1[0][5][189].mul *= d[9]
    parsed_parts1[0][5][190].mul *= d[9]
    parsed_parts1[0][5][191].mul *= d[5]
    parsed_parts1[0][5][192].mul *= d[5]
    # m113
    parsed_parts1[0][5][196].mul *= d[8]
    parsed_parts1[0][5][197].mul *= d[8]
    # m114
    parsed_parts1[0][5][198].mul *= d[7]
    # m117
    parsed_parts1[0][5][206].mul *= d[7]
    parsed_parts1[0][5][207].mul *= d[7]
    # m121
    parsed_parts1[0][5][208].mul *= d[5]
    parsed_parts1[0][5][209].mul *= d[5]
    parsed_parts1[0][5][210].mul *= d[6]
    parsed_parts1[0][5][211].mul *= d[7]
    parsed_parts1[0][5][212].mul *= d[7]
    parsed_parts1[0][5][213].mul *= d[8]
    # m122
    parsed_parts1[0][5][214].mul *= d[5]
    parsed_parts1[0][5][215].mul *= d[6]
    parsed_parts1[0][5][216].mul *= d[7]
    parsed_parts1[0][5][217].mul *= d[8]
    # m123
    parsed_parts1[0][5][218].mul *= d[8]
    parsed_parts1[0][5][219].mul *= d[8]
    parsed_parts1[0][5][220].mul *= d[5]
    parsed_parts1[0][5][221].mul *= d[5]
    # m124
    parsed_parts1[0][5][222].mul *= d[3]
    parsed_parts1[0][5][223].mul *= d[3]
    # m126
    parsed_parts1[0][5][224].mul *= d[6]
    parsed_parts1[0][5][225].mul *= d[6]
    # m129
    parsed_parts1[0][5][234].mul *= d[5]
    parsed_parts1[0][5][235].mul *= d[5]
    # m130
    parsed_parts1[0][5][236].mul *= d[7]
    parsed_parts1[0][5][237].mul *= d[5]
    parsed_parts1[0][5][238].mul *= d[5]
    parsed_parts1[0][5][239].mul *= d[5]
    parsed_parts1[0][5][240].mul *= d[8]
    parsed_parts1[0][5][241].mul *= d[8]
    # m131
    parsed_parts1[0][5][242].mul *= d[8]
    parsed_parts1[0][5][243].mul *= d[7]
    parsed_parts1[0][5][244].mul *= d[7]
    parsed_parts1[0][5][245].mul *= d[6]
    parsed_parts1[0][5][246].mul *= d[6]
    # m132
    parsed_parts1[0][5][252].mul *= d[8]
    parsed_parts1[0][5][253].mul *= d[7]
    parsed_parts1[0][5][254].mul *= d[7]
    # m133
    parsed_parts1[0][5][255].mul *= d[8]
    parsed_parts1[0][5][256].mul *= d[8]
    # m134
    parsed_parts1[0][5][257].mul *= d[8]
    parsed_parts1[0][5][258].mul *= d[8]
    parsed_parts1[0][5][259].mul *= d[8]
    parsed_parts1[0][5][260].mul *= d[8]
    parsed_parts1[0][5][261].mul *= d[8]
    parsed_parts1[0][5][262].mul *= d[8]
    parsed_parts1[0][5][263].mul *= d[7]
    # m135
    parsed_parts1[0][5][264].mul *= d[8]
    parsed_parts1[0][5][265].mul *= d[9]

    # m57
    parsed_parts1[0][6][0].mul *= d[8]
    # m68
    parsed_parts1[0][6][1].mul *= d[6]
    # m89
    parsed_parts1[0][6][4].mul *= d[8]
    parsed_parts1[0][6][5].mul *= d[8]
    # m90
    parsed_parts1[0][6][6].mul *= d[8]
    parsed_parts1[0][6][7].mul *= d[8]
    # m92
    parsed_parts1[0][6][12].mul *= d[9]
    parsed_parts1[0][6][13].mul *= d[9]
    # m93
    parsed_parts1[0][6][17].mul *= d[8]
    parsed_parts1[0][6][18].mul *= d[8]
    # m96
    parsed_parts1[0][6][19].mul *= d[4]
    parsed_parts1[0][6][20].mul *= d[4]
    # m98
    parsed_parts1[0][6][24].mul *= d[6]
    # m104
    parsed_parts1[0][6][27].mul *= d[5]
    # m105
    parsed_parts1[0][6][28].mul *= d[5]
    parsed_parts1[0][6][29].mul *= d[4]
    parsed_parts1[0][6][30].mul *= d[4]
    parsed_parts1[0][6][31].mul *= d[5]
    parsed_parts1[0][6][32].mul *= d[6]
    parsed_parts1[0][6][33].mul *= d[4]
    parsed_parts1[0][6][34].mul *= d[4]
    # m108
    parsed_parts1[0][6][36].mul *= d[8]
    # m111
    parsed_parts1[0][6][38].mul *= d[5]
    parsed_parts1[0][6][39].mul *= d[5]
    # m121
    parsed_parts1[0][6][43].mul *= d[5]
    parsed_parts1[0][6][44].mul *= d[7]
    # m130
    parsed_parts1[0][6][45].mul *= d[8]
    parsed_parts1[0][6][46].mul *= d[8]
    # m131
    parsed_parts1[0][6][47].mul *= d[8]
    parsed_parts1[0][6][48].mul *= d[7]
    parsed_parts1[0][6][49].mul *= d[7]
    parsed_parts1[0][6][50].mul *= d[6]
    parsed_parts1[0][6][51].mul *= d[6]

    # m47
    parsed_parts1[0][7][0].mul *= d[5]
    # m96
    parsed_parts1[0][7][6].mul *= d[7]
    parsed_parts1[0][7][7].mul *= d[3]

    # m8
    parsed_parts2[0][0][0].mul *= d[5]
    parsed_parts2[0][0][1].mul *= d[5]
    parsed_parts2[0][0][2].mul *= d[7]

    # m7
    parsed_parts2[0][1][4].mul *= d[5]
    parsed_parts2[0][1][5].mul *= d[4]
    # m8
    parsed_parts2[0][1][6].mul *= d[5]
    parsed_parts2[0][1][7].mul *= d[5]
    parsed_parts2[0][1][8].mul *= d[7]
    # m11
    parsed_parts2[0][1][11].mul *= d[2]
    parsed_parts2[0][1][12].mul *= d[2]
    # m12
    parsed_parts2[0][1][13].mul *= d[2]
    # m15
    parsed_parts2[0][1][15].mul *= d[3]
    parsed_parts2[0][1][16].mul *= d[4]
    # m17
    parsed_parts2[0][1][17].mul *= d[3]
    # m18
    parsed_parts2[0][1][18].mul *= d[3]
    # m20
    parsed_parts2[0][1][19].mul *= d[2]
    parsed_parts2[0][1][20].mul *= d[2]
    # m21
    parsed_parts2[0][1][21].mul *= d[1]
    parsed_parts2[0][1][22].mul *= d[2]
    # m22
    parsed_parts2[0][1][23].mul *= d[1]
    # m23
    parsed_parts2[0][1][24].mul *= d[2]

    # m15
    parsed_parts2[0][2][1].mul *= d[3]
    parsed_parts2[0][2][2].mul *= d[4]
    # m17
    parsed_parts2[0][2][3].mul *= d[3]
    # m18
    parsed_parts2[0][2][4].mul *= d[3]
    # m21
    parsed_parts2[0][2][5].mul *= d[2]
    # m23
    parsed_parts2[0][2][6].mul *= d[2]

    # m15
    parsed_parts2[0][3][0].mul *= d[3]
    parsed_parts2[0][3][1].mul *= d[4]
    # m17
    parsed_parts2[0][3][2].mul *= d[5]
    # m18
    parsed_parts2[0][3][3].mul *= d[6]
    # m23
    parsed_parts2[0][3][4].mul *= d[2]

    # m15
    parsed_parts2[0][4][0].mul *= d[4]
    # m17
    parsed_parts2[0][4][1].mul *= d[3]
    # m18
    parsed_parts2[0][4][2].mul *= d[3]
    # m23
    parsed_parts2[0][4][3].mul *= d[2]

    # m17
    parsed_parts2[0][5][0].mul *= d[3]
    # m18
    parsed_parts2[0][5][1].mul *= d[3]
    # m23
    parsed_parts2[0][5][2].mul *= d[2]

    # m18
    parsed_parts2[0][6][0].mul *= d[3]
    # m23
    parsed_parts2[0][6][1].mul *= d[2]

    # m7
    parsed_parts2[0][7][1].mul *= d[3]
    # m11
    parsed_parts2[0][7][4].mul *= d[2]
    parsed_parts2[0][7][5].mul *= d[2]
    parsed_parts2[0][7][6].mul *= d[2]
    # m12
    parsed_parts2[0][7][7].mul *= d[2]

    parsed_parts1[0][0][76].buffer = "\"j\""
    parsed_parts1[0][0][78].buffer = "\"d\""
    parsed_parts1[0][0][81].buffer = "\"t\""
    parsed_parts1[0][0][84].buffer = "\"b\""
    parsed_parts1[0][0][86].buffer = "\"k\""
    parsed_parts1[0][0][89].buffer = "\"t\""
    parsed_parts1[0][0][219].buffer = "\"m\""
    parsed_parts1[0][0][221].buffer = "\"pak-002\""
    parsed_parts1[0][0][224].buffer = "\"t\""
    parsed_parts1[0][0][229].buffer = "\"uh\""
    parsed_parts1[0][0][230].buffer = "\"zh\""
    parsed_parts1[0][0][231].buffer = "\"k\""
    parsed_parts1[0][0][235].buffer = "\"v\""

    add_effects(parsed_parts1, pan1l)
    add_effects(parsed_parts1, dynamics1)
    batch_dynamic_synth_update(parsed_parts1)
    collapse_voices(parsed_parts1)

    add_effects(parsed_parts2, pan2l)
    add_effects(parsed_parts2, dynamics2)
    batch_dynamic_synth_update(parsed_parts2)
    collapse_voices(parsed_parts2)

    # Create the SuperCollider score
    xml_parse_sc.dump_sc_to_file(f"{OUTPUT}\\score1", parsed_parts1, "score1")
    xml_parse_sc.dump_sc_to_file(f"{OUTPUT}\\score2", parsed_parts2, "score2")


def collapse_voices(new_parts):
    """
    Collapses separately chained notes in a list of parts
    :param new_parts: A list of parts
    :return: None
    """
    for part in new_parts:
        for voice in part:
            i = 0
            while i < len(voice):
                if type(voice[i]) == list:
                    if len(voice[i]) > 0:
                        current = voice[i]
                        for j in range(len(current) - 1, -1, -1):
                            voice.insert(i, current[j])
                        current.clear()
                    else:
                        del voice[i]
                else:
                    i += 1


if __name__ == "__main__":
    build_score()
