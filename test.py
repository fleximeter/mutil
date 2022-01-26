from pctheory import group, pcseg, pcset, pitch, set_complex, tables, transformations, util

s4 = pcseg.make_pcseg(0, 11, 7, 8, 3, 1, 2, 10, 6, 5, 4, 9)
s4mx = pcseg.TwelveToneMatrix(s4)
pc = [pitch.PitchClass(n) for n in range(12)]
tmx = pcseg.InvarianceMatrix("T", s4, s4)
imx = pcseg.InvarianceMatrix("I", s4, s4)

imx.print([pc[11]])

