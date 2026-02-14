"""
File: algorithms.py

Implements various compositional algorithms
"""

from typing import Callable, Any

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
