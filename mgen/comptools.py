"""
File: comptools.py

This file contains basic functionality for things like list manipulation, etc. for algorithmic composition.
"""

import random
_rng = random.Random()
_rng.seed()

def add(l: list, val, in_place: bool = False):
    """
    Adds a constant to a list
    :param l: The list
    :param val: The value to add (can be int or float)
    :param in_place: Whether or not to add in place
    :return: If `in_place` is `False`, returns a multiplied copy of the list
    """
    if in_place:
        for i, item in enumerate(l):
            l[i] = item + val
    else:
        l2 = l.copy()
        for i, item in enumerate(l2):
            l2[i] = item + val
        return l2

def lambda_op(l: list, op: function, in_place: bool = False):
    """
    Performs a generic operation on a list
    :param l: The list
    :param op: The operation function
    :param in_place: Whether or not to perform the operation in place
    :return: If `in_place` is `False`, returns a multiplied copy of the list
    """
    if in_place:
        for i, val in enumerate(l):
            l[i] = op(val)
    else:
        l2 = l.copy()
        for i, val in enumerate(l2):
            l2[i] = op(val)
        return l2
    
def multiply(l: list, multiplicand, in_place: bool = False):
    """
    Multiplies a list
    :param l: The list
    :param multiplicand: The multiplicand (can be int or float)
    :param in_place: Whether or not to multiply in place
    :return: If `in_place` is `False`, returns a multiplied copy of the list
    """
    if in_place:
        for i, val in enumerate(l):
            l[i] = val * multiplicand
    else:
        l2 = l.copy()
        for i, val in enumerate(l2):
            l2[i] = val * multiplicand
        return l2

def rotate(l: list, index_of_rotation: int) -> list:
    """
    Rotates a list
    :param l: The list
    :param index_of_rotation: The index of rotation
    :return: A rotated copy of the list
    """
    index_of_rotation %= len(l)
    return l[index_of_rotation:] + l[:index_of_rotation]

def scramble(l: list) -> list:
    """
    Scrambles a list
    :param l: The list
    :return: The scrambled list
    """
    templist = l.copy()
    newlist = []
    for i in range(len(l)):
        val = _rng.randrange(0, len(l))
        newlist.append(templist[val])
        del templist[val]
    return newlist
