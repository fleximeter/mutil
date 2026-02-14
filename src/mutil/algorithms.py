"""
File: algorithms.py

Implements various compositional algorithms
"""

from typing import Callable, Any

class Range:
    """
    Represents a range to constrain pitches
    """
    def __init__(self, low, high):
        """
        Creates a new Range
        :param low: The low bound
        :param high: The high bound
        """
        if not low < high:
            raise ValueError(f"The low value must be lower than the high value, but `{low}` is not lower than `{high}`.")
        self.low = low
        self.high = high
        self.mod = high - low + 1
    
    def fold(self, val):
        """
        Folds a value into the range
        :param val: The value to fold
        """
        fold_range = self.mod * 2 - 2
        fold_step_1 = (val - self.low) % fold_range
        if fold_step_1 >= self.mod:
            fold_step_1 = fold_range - fold_step_1
        return fold_step_1 + self.low
    
    def wrap(self, val):
        """
        Wraps a value into the range
        :param val: The value to wrap
        """
        return (val - self.low) % self.mod + self.low

class Rule:
    """
    Represents a grammar rule
    :param condition: The rule condition callable. It should return a boolean
    indicating whether or not the rule applies.
    :param action: The action callable. This is the action that can be taken
    if the rule applies. It should return a list of items.
    """
    def __init__(self, condition: Callable[..., bool], action: Callable[..., Any]):
        self.applies = condition
        self.invoke = action

class LindenmayerSystem:
    """
    A Lindenmayer system
    """
    def __init__(self):
        """
        Initializes the Lindenmayer system
        """
        self.token_stream = []
        self.rules = []
    
    def add_rule(self, rule: Rule):
        """
        Adds a Rule to the Lindenmayer system
        :param rule: The Rule to add
        """
        self.rules.append(rule)
    
    def set_axiom(self, axiom):
        """
        Initializes the Lindenmayer system with an axiom,
        erasing all preexisting tokens.
        :param axiom: The axiom to use
        """
        self.token_stream.clear()
        self.token_stream.append(axiom)
    
    def grow(self, n=1):
        """
        Grows the Lindenmayer system recursively for N iterations
        :param n: The number of iterations to grow
        """
        for _ in range(n):
            new_token_stream = []
            for token in self.token_stream:
                for rule in self.rules:
                    if rule.applies(token):
                        new_token_stream += rule.invoke(token)
            self.token_stream = new_token_stream
