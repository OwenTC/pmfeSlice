from pmfeInterface import pmfeInterface
from sympy import Point2D

interface = pmfeInterface("/home/owen/Documents/research/pmfe/", "/home/owen/Documents/research/RNA_Data/tRNA/o.nivara_tRNA.fasta", transform=True)

points = [Point2D(50, "-147/10")]

for p in points:
    print(p)
    print(interface.vertex_oracle(p[0], 0, p[1], 1))
    print(interface.subopt_oracle(p[0], 0, p[1], 1))