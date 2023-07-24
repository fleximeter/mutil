from matplotlib import pyplot
import networkx
import random
from ..pctheory import pitch, pcset, tables

random.seed()

a = pcset.make_pcset(0, 1, 4, 6)
g = networkx.Graph()

for i in range(20):
    g.add_node(i)

for i in range(40):
    g.add_edge(int(random.random() * 251) % len(g), int(random.random() * 251) % len(g))

subax1 = pyplot.subplot(121)
networkx.draw(g, pos=networkx.circular_layout(g))
pyplot.show()
