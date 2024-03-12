from pmfeInterface import pmfeInterface
from viennaInterface import ViennaInterface
from sympy import Point2D

Vinterface = ViennaInterface("/home/owen/Documents/research/pmfe2023/","/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta", transform=False)
Pinterface = pmfeInterface("/home/owen/Documents/research/pmfe2023/", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta", transform=False)

points = [(5000,5000)]

for p in points:
    print(p)
    for i in range(1):
        # print(interface.subopt_oracle(5000,0,-978,1))
        # print(Vinterface.vertex_oracle(p[0],0,p[1],1))
        print(Vinterface.vertex_oracle(p[0],0,p[1],1))
        print(Vinterface.subopt_oracle(p[0],0,p[1],1, eng=20))
        print(Pinterface.subopt_oracle(p[0],0,p[1],1, eng=0))

        # print(interface.scored_structure(".((((.........(((........))).....(((((......)).)))....)))).."))
    # for i in range(54):
    #     interface.subopt_oracle(p[0], 1, p[1], 1)