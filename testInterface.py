from pmfeInterface import pmfeInterface
from viennaInterface import ViennaInterface
from sympy import Point2D
from random import randint

Vinterface = ViennaInterface("/home/owen/Documents/research/pmfe2023/","/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta", transform=False)
Pinterface = pmfeInterface("/home/owen/Documents/research/pmfe2023/", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta", transform=False)

# points = [(1120,-29),(1119,-29),(1119,-30),(1120,-30),(1121,-30),(1120,-30),(1120,-31),(1121,-31),(1119,-31)]
# points = [(3112, -1460),(3111, -1460),(3111, -1461),(3112, -1461)]
# (3113, -1460);(3112, -1460);(3112, -1461);(3113, -1461)

points = [(randint(-50000,50000),randint(-50000,50000)) for _ in range(1722)]

#(463.5, -187.5), (465.5, -188.5)

# points = [(464, -187), (463, -187), (463, -188), (464, -188)]
# points += [(466,-188),(465,-188),(465,-189),(466,-189)]

points = [(2170, -1059),(2169, -1059),(2169, -1060),(2170, -1060),(2171, -1060),(2170, -1060),(2170, -1061),(2171, -1061)]

#Potential 26 points

# points = [(1713.33333333,-893.33333333),(1705,-890),(1700.,-890.),(1715.,-895.)]


# point = (round(1713.33333333),round(-893.33333333))
# points = [(point[0]+i, point[1]+j) for i in range(-2,3) for j in range(-2,3)]
print(points)

for p in points:
    # print(p)
    # for i in range(1722):
        # print(interface.subopt_oracle(5000,0,-978,1))
        # print(Vinterface.vertex_oracle(p[0],0,p[1],1))
    print(Vinterface.vertex_oracle(p[0],0,p[1],1))
        # print(Vinterface.subopt_oracle(p[0],0,p[1],1, eng=20))
        # print(Pinterface.subopt_oracle(p[0],0,p[1],1, eng=0))

        # print(interface.scored_structure(".((((.........(((........))).....(((((......)).)))....)))).."))
    # for i in range(54):
    #     interface.subopt_oracle(p[0], 1, p[1], 1)

    # print(Vinterface.subopt_oracle(p[0],0,p[1],1,eng=0))