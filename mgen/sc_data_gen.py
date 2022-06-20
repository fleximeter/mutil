"""
File: sc_data_gen.py
Author: Jeff Martin
Email: jeffreymartin@outlook.com
This file contains functionality for generating SuperCollider data such as envelopes.
Copyright © 2022 by Jeff Martin. All rights reserved.
"""


def env4_strong_atk(duration):
    """
    Generates a 4-point envelope with a strong attack. Minimum duration of note: 0.08 seconds.
    :param duration: The duration
    :return: The envelope as a string
    """
    env = f"[[0, 1, 0.5, 0, 0, 0, 0, 0, 0, 0], [0.04, {duration - 0.04 - 0.04}, " \
          f"0.04, 0, 0, 0, 0, 0, 0], [4, -4, -4, 0, 0, 0, 0, 0, 0]]"
    return env


def env4_weak_atk(duration):
    """
    Generates a 4-point envelope with a weak attack. Minimum duration of note: 0.08 seconds.
    :param duration: The duration
    :return: The envelope as a string
    """
    env = f"[[0, 1, 0.75, 0, 0, 0, 0, 0, 0, 0], [0.04, {duration - 0.04 - 0.04}, " \
          f"0.04, 0, 0, 0, 0, 0, 0], [4, -4, -4, 0, 0, 0, 0, 0, 0]]"
    return env


def env5_strong_atk(duration):
    """
    Generates a 5-point envelope with a strong attack. Minimum duration of note: 0.22 seconds.
    :param duration: The duration
    :return: The envelope as a string
    """
    env = f"[[0, 1, 0.5, 0.5, 0, 0, 0, 0, 0], [0.04, 0.1" \
          f"{duration - 0.04 - 0.12 - 0.06}, 0.06, 0, 0, 0, 0], " \
          f"[4, -3, 0, -4, 0, 0, 0, 0]]"
    return env


def env5_weak_atk(duration):
    """
    Generates a 5-point envelope with a weak attack. Minimum duration of note: 0.22 seconds.
    :param duration: The duration
    :return: The envelope as a string
    """
    env = f"[[0, 1, 0.75, 0.75, 0, 0, 0, 0, 0], [0.04, 0.1" \
          f"{duration - 0.04 - 0.12 - 0.06}, 0.06, 0, 0, 0, 0], " \
          f"[4, -3, 0, -4, 0, 0, 0, 0]]"
    return env


def env6_strong_atk(duration):
    """
    Generates a 6-point envelope with a strong attack. Minimum duration of note: 0.26 seconds.
    :param duration: The duration
    :return: The envelope as a string
    """
    env = f"[[0, 1, 0.9, 0.5, 0.5, 0, 0, 0, 0, 0], [0.04, 0.1, 0.04, " \
          f"{duration - 0.04 - 0.1 - 0.04 - 0.08}, 0.08, 0, 0, 0, 0], " \
          f"[4, -2, -4, 0, -4, 0, 0, 0, 0]]"
    return env


def env6_weak_atk(duration):
    """
    Generates a 6-point envelope with a weak attack. Minimum duration of note: 0.26 seconds.
    :param duration: The duration
    :return: The envelope as a string
    """
    env = f"[[0, 1, 0.95, 0.75, 0.75, 0, 0, 0, 0, 0], [0.04, 0.1, 0.04, " \
          f"{duration - 0.04 - 0.1 - 0.04 - 0.08}, 0.08, 0, 0, 0, 0], " \
          f"[4, -2, -4, 0, -4, 0, 0, 0, 0]]"
    return env
