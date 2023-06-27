from pmfeInterface import pmfeInterface
from sympy import Point2D

interface = pmfeInterface("/home/owen/Documents/research/pmfe/", "/home/owen/Documents/research/pmfe/test_seq/synthetic/time_test/sequence_2.fasta", transform=False)

points = [Point2D(50, -128/5)]

for p in points:
    print(p)
    for i in range(288):
        interface.vertex_oracle(p[0], 0, p[1], 1)
    for i in range(50):
        interface.subopt_oracle(p[0], 1, p[1], 1)