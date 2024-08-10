import subprocess
# from os import path
import os
from sympy import Point, Line, Rational

class pmfeInterface:
    #Initialize with b and d!!!
    def __init__(self, pmfePath: str, filePath:str, transform: bool = False): 
        self.pmfePath = pmfePath
        self.filePath = filePath
        self.transform = transform
        self.pmfeCalls = 0
        self.suboptCalls = 0

    #Calls pmfe with params a, b, c, d
    def vertex_oracle(self, a: Rational, b: Rational, c: Rational, d: Rational):
        self.pmfeCalls += 1
        if self.transform:
            a = a-(c*3)
            return self.transform_z(self.call_pmfe(a,b,c,d)) #self.transform_z

        return self.call_pmfe(a,b,c,d)

    #Calls subopt with params a, b, c, d
    def subopt_oracle(self, a: Rational, b: Rational, c: Rational, d: Rational):
        self.suboptCalls += 1
        if self.transform:
            a = a-(c*3)
            subopt= self.call_subopt(a,b,c,d)
            transformed = []
            for s in subopt:
                transformed.append(self.transform_z(s))

            return transformed
        return self.call_subopt(a,b,c,d)

#----------------------------------------------------------------------------------------------------------
    # Internal Methods

    def call_pmfe(self, a, b, c, d):
        # cwd = os.getcwd()
        # os.chdir(self.pmfePath)
        findmfe_path = os.path.join(self.pmfePath, "pmfe-findmfe")
        command = f"{findmfe_path} -a {a} -b {b} -c {c} -d {d} {self.filePath}".split()

        pmfe_raw = subprocess.run(command, stdout=subprocess.PIPE, encoding='UTF-8')
        pmfe = [b for b in pmfe_raw.stdout.split()]
        sig = Point(pmfe[1],pmfe[2],pmfe[3],pmfe[4])

        #HANDLE ERRORS
        #
        #
        #

        # os.chdir(cwd)
        return (sig)

    def call_subopt(self, a, b, c, d):
        # cwd = os.getcwd()
        # os.chdir(self.pmfePath)
        subopt_path = os.path.join(self.pmfePath, "pmfe-subopt")
        command = f"{subopt_path} -a {a} -b {b} -c {c} -d {d} --delta 0 -C {self.filePath}".split()
        
        subopt_raw = subprocess.run(command, stdout=subprocess.PIPE, encoding='UTF-8') # text=True)
        #HANDLE ERRORS
        #
        #
        #
        suboptScores = [] #tuples x,y,z,w
        # with open("out.tmp", "r") as out:
        for line in subopt_raw.stdout.split("\n")[5:-1]:
            line = line.split()                
            x,y,z,w = Point(line[2], line[3], line[4], line[5])
            suboptScores.append(Point(x,y,z,w))
            # print(out.readlines());

        # os.remove("out.tmp")
        # os.chdir(cwd)

        return (suboptScores)
    
    def transform_z(self, point):
        x,y,z,w = point
        return Point(x, y, z - (3*x), w)

# interface = pmfeInterface("/home/owen/Documents/research/pmfe", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta")

# print(interface.vertex_oracle(1, 0, 1, 1))