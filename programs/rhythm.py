import pctheory.tempo as tempo
from fractions import Fraction

divisions = [
    Fraction(1, 8),
    Fraction(1, 7),
    Fraction(1, 6),
    Fraction(1, 5),
    Fraction(1, 4),
    Fraction(2, 7),
    Fraction(1, 3),
    Fraction(3, 8),
    Fraction(2, 5),
    Fraction(3, 7),
    Fraction(1, 2),
    Fraction(4, 7),
    Fraction(3, 5),
    Fraction(2, 3),
    Fraction(3, 4),
    Fraction(4, 5),
    Fraction(4, 4),
    Fraction(4, 3),
    Fraction(3, 2),
    Fraction(2, 1),
    Fraction(3, 1),
    Fraction(4, 1),
]

divisions.reverse()

tempo.plot_tempo_table([60, 72, 84, 96, 108, 120], divisions)

