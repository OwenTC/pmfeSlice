from numpy import random

poly = polygon([(0,0), (0,0), (0,0)], alpha=0)
colors = ["blue", "green", "orange", "purple","cyan"]
with open("test_data/sequence_2.fasta.txt", "r") as p:
    for i, p in enumerate(p.readlines()):
        # shuffle(colors)
        data = p.strip("\n").split(": ")
        points = [tuple(p.strip("()").replace(" ", "").split(",")) for p in data[1].split(",(")]
        points = [(Rational(p[0]), Rational(p[1])) for p in points]
        poly = poly + polygon(points, color=list(random.rand(3,)), dpi=1000)

poly.save("polygraph.png")