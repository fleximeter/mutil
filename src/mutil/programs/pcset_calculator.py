"""
File: pcset_calculator.py
Date: 3/14/24

This file contains standard functionality for interactive pctheory calculations.
"""

import pctheory.pitch as pitch
import pctheory.pcset as pcset
import pctheory.transformations as transformations

HEX_MAP = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

VALID_COMMANDS = {"about", "a", "calculate", "c", "exit", "x", "info", "n", "load", "l", "mod", "quit", "q", "search", "h", "subsets", "s", "subsets prime", "sp"}
NON_NUMERIC_TRANSFORMATIONS = {"I"}
NUMERIC_TRANSFORMATIONS = {"T", "M"}
VALID_TRANSFORMATIONS = NUMERIC_TRANSFORMATIONS.union(NON_NUMERIC_TRANSFORMATIONS)
sc = pcset.SetClass(pc_mod=12)


def about():
    """
    Displays info about the program
    """
    print(("pcset calculator copyright (c) 2024 by Jeffrey Martin. All rights reserved.\n"
        "This program is free software: you can redistribute it and/or modify\n"
        "it under the terms of the GNU General Public License as published by\n"
        "the Free Software Foundation, either version 3 of the License, or\n"
        "(at your option) any later version.\n\n"
        "This program is distributed in the hope that it will be useful,\n"
        "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n"
        "GNU General Public License for more details.\n\n"
        "You should have received a copy of the GNU General Public License\n"
        "along with this program. If not, see https://www.gnu.org/licenses/."))


def calculate():
    """
    Enters continuous calculation mode
    """
    print("Continuous calculation mode (enter \'q\' to quit)...")
    user_input = input("...> ").lower()
    while user_input not in ["quit", "q", "exit", "x"]:
        if load(user_input, True):
            info()
        user_input = input("...> ").lower()


def info():
    """
    Displays info about the set class
    """
    if sc.mod == 12:
        print("{0: <17}{1}".format("Prime form name:", sc.name_prime),
            "\n{0: <17}{1}".format("Forte name:", sc.name_forte),
            "\n{0: <17}{1}".format("IC vector:", sc.ic_vector_str),
            "\n{0: <17}{1}".format("Dsym:", sc.dsym))
    else:
        print("{0: <17}{1}".format("Prime form name:", sc.name_prime),
            "\n{0: <17}{1}".format("IC vector:", sc.ic_vector_str),
            "\n{0: <17}{1}".format("Dsym:", sc.dsym))


def load(command, print_tn=False):
    """
    Loads the set class
    :param command: The set class prime form
    :param print_tn: Whether or not to print the transformation that was entered
    """
    try:
        if '-' in command:
            sc.load_from_name(command)
        else:
            pcs = {pitch.PitchClass(n, mod=sc.mod) for n in parser(command)}
            sc.pcset = pcs
            if print_tn:
                print("You entered", sorted(list(transformations.find_utos(sc.pcset, pcs))))
        return True
    except Exception:
        print("Please enter a valid pcset to load...")
        return False


def mod(command):
    """
    Sets the mod of the set class
    :param command: The mod number
    """
    global sc
    try:
        command = int(command)
        sc = pcset.SetClass(pc_mod=command)
    except Exception:
        print("Please enter a valid number for the mod value...")


def search(command):
    """
    Searches transformations of the set class
    :param command: The pcs to search for
    """
    try:
        utos = transformations.find_utos(sc.pcset, {pitch.PitchClass(n, mod=sc.mod) for n in parser(command)})
        utos = sorted(list(utos))
        print(utos)
    except Exception:
        print("Please enter a valid pcset to search for...")


def subsets():
    """
    Calculates the subsets of the set class
    """
    s = pcset.subsets(sc.pcset)
    s = sorted(list(s))
    print(s)


def subsets_prime():
    """
    Calculates the abstract subsets of the set class
    """
    sp = sc.get_abstract_subset_classes()
    sp = sorted(list(sp))
    print(sp)


def transform(command):
    """
    Transforms the prime form of the set class
    :command: The transformation string
    """
    tr = pcset.transform(sc.pcset, command)
    tr = sorted(list(tr))
    print("{", end="")
    for i, pc in enumerate(tr):
        if sc.mod == 12:
            print(f"{pc}", end="")
        else:
            if i < len(tr) - 1:
                print(f"{pc}, ", end="")
            else:
                print(f"{pc}", end="")
    print("}")


def menu():
    """
    Displays the application menu
    """
    user_input = ""
    while user_input not in ["quit", "q", "exit", "x"]:
        user_input = input("> ")
        if validate_command(user_input):
            process_command(user_input)
        else:
            print("Enter a valid command (q to quit)...")


def parser(command) -> list:
    """
    Parses a hexadecimal string and makes a list of decimal numbers
    :command: The command string to parse
    :return: A list of numbers
    """
    num_list = []
    if ' ' in command:
        command = command.split(' ')
    elif ',' in command:
        command = command.split(' ')
    if type(command) == list:
        for c in command:
            if c in HEX_MAP:
                num_list.append(HEX_MAP[c])
            else:
                num_list.append(int(c))
    else:
        for c in command:
            if c not in HEX_MAP:
                raise Exception("Invalid input")
            else:
                num_list.append(HEX_MAP[c])
    return num_list


def process_command(command: str) -> None:
    """
    Processes a valid command
    :param command: The command string
    :return: None
    """
    command = command.strip()
    if command[0] in VALID_TRANSFORMATIONS:
        transform(command)
    else:
        command_words = command.lower().split()
        if len(command_words) > 0:
            # some commands are 2 words
            command1 = command_words[0]
            command2 = command1
            if len(command_words) > 1:
                command2 = f"{command_words[0]} {command_words[1]}"
            if command2 != command1 and command2 in VALID_COMMANDS:
                match command2:
                    case "subsets prime":
                        subsets_prime()
            else:
                match command1:
                    case "about" | "a":
                        about()
                    case "calculate" | "c":
                        calculate()
                    case "info" | "n":
                        info()
                    case "load" | "l":
                        load(" ".join(command_words[1:]))
                    case "mod":
                        mod(" ".join(command_words[1:]))
                    case "search" | "h":
                        search(" ".join(command_words[1:]))
                    case "subsets" | "s":
                        subsets()
                    case "sp":
                        subsets_prime()


    if len(command) > 0:
        if command[0] in VALID_TRANSFORMATIONS:
            return validate_transformation(command)
        else:
            command_words = command.lower().split()
            if len(command_words) > 0:
                # some commands are 2 words
                command1 = command_words[0]
                command2 = command1
                if len(command_words) > 1:
                    command2 = f"{command_words[0]} {command_words[1]}"

                # is the command valid?
                if command2 not in VALID_COMMANDS and command1 not in VALID_COMMANDS:
                    return False
                else:
                    return True
            else:
                return False
    else:
        return False


def validate_command(command: str) -> bool:
    """
    Validates a command
    :param command: The command string
    :return: True or False
    """
    command = command.strip()
    if len(command) > 0:
        if command[0] in VALID_TRANSFORMATIONS:
            return validate_transformation(command)
        else:
            command_words = command.lower().split()
            if len(command_words) > 0:
                # some commands are 2 words
                command1 = command_words[0]
                command2 = command1
                if len(command_words) > 1:
                    command2 = f"{command_words[0]} {command_words[1]}"

                # is the command valid?
                if command2 not in VALID_COMMANDS and command1 not in VALID_COMMANDS:
                    return False
                else:
                    return True
            else:
                return False
    else:
        return False


def validate_transformation(transformation: str) -> bool:
    """
    Validates a transformation
    :param transformation: The transformation string
    :return: True or False
    """
    transformation = transformation.strip()
    for i, c in enumerate(transformation):
        # check for invalid characters
        if c not in VALID_TRANSFORMATIONS and not '0' <= c <= '9':
            return False
        
        # check for numbers being given to transformations that can't take them
        elif i < len(transformation) - 1 and c in NON_NUMERIC_TRANSFORMATIONS and '0' <= transformation[i+1] <= '9':
            return False
        
        # check for numbers not being given to transformations that need them
        elif i < len(transformation) - 1 and c in NUMERIC_TRANSFORMATIONS and not '0' <= transformation[i+1] <= '9':
            return False
        elif i == len(transformation) - 1 and c in NUMERIC_TRANSFORMATIONS:
            return False
    return True


if __name__ == "__main__":
    print(("#################### pcset calculator #####################\n"
           "Copyright (c) 2024 by Jeffrey Martin. All rights reserved.\n"
           "https://www.jeffreymartincomposer.com\n"
           "This program is licensed under the GNU GPL v3 and comes\n"
           "with ABSOLUTELY NO WARRANTY. For details, type \'about\'."))
    menu()
