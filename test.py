import mgen.tempo as tempo
from fractions import Fraction

tempi = (48, 60, 72)
durations = (4, 2, Fraction(2, 3), 1, Fraction(1, 2), Fraction(2, 5), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(1, 6), Fraction(1, 7), Fraction(1, 8), Fraction(1, 9))

tempo.plot_tempo_table(tempi, durations)