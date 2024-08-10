from viennaInterface import ViennaInterface
from pmfeInterface import pmfeInterface
import numpy as np
from sympy import Point
fasta_file = "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta"

interface = ViennaInterface("../pmfe2023", fasta_file, False)
# interface = pmfeInterface("../pmfe2023", fasta_file, True)

# A, C = 2000

C = (-900,-885)
A = (1695, 1720)

# C_offset = 4000

# scores = np.zeros((2*A//grid,2*C//grid), dtype=Point)
scores = np.zeros((abs(A[1]-A[0]),abs(C[1]-C[0])), dtype=Point)
for i, a in enumerate(range(*A)):
    # for j, c in enumerate(range(C_offset-C,C_offset+C,grid)):
    for j, c in enumerate(range(*C)):
        # if j%500 == 0:
        #     print(f"A = {a}", f"C = {c}")
        scores[i,j] = tuple(x for x in interface.vertex_oracle(a, 0, c, 1))


print(scores)
scores.tofile('non_int_tp_scores.csv',sep=';')

