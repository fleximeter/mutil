"""
File: fibonacci.py
Author: Jeff Martin
Date: 9/4/21
This file implements the Fibonacci sequence.
"""


def fibonacci_calc(n):
    """
    Calculates and returns a list of the first n integers in the Fibonacci sequence
    :param n: The number of integers
    :return: The sequence
    """
    if n >= 0:
        sequence = [0, 1, 1]
        while len(sequence) > n:
            del sequence[len(sequence) - 1]
        while len(sequence) < n:
            sequence.append(sequence[len(sequence) - 1] + sequence[len(sequence) - 2])
        return sequence
    else:
        return []


sequence_fib20 = [num % 12 for num in fibonacci_calc(100)]
print(sequence_fib20)