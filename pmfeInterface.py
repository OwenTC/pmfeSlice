import subprocess
# from os import path
import os
from sympy import Point, Line, Rational

class pmfeInterface:
    #Initialize with b and d!!!
    def __init__(self, pmfePath, filePath, transform = False):
        self.pmfePath = pmfePath
        self.filePath = filePath
        self.transform = transform

    def vertex_oracle(self, a, b, c, d):
        if self.transform:
            a = a-(c*3)
            return self.transform_z(self.call_pmfe(a,b,c,d)) #self.transform_z

        return self.call_pmfe(a,b,c,d)

    def subopt_oracle(self, a, b, c, d):
        return self.call_subopt(a,b,c,d)

    # Internal 
    def call_pmfe(self, a, b, c, d):
        cwd = os.getcwd()
        os.chdir(self.pmfePath)
        command = f"./pmfe-findmfe -a {a} -b {b} -c {c} -d {d} {self.filePath}".split()
        # print(command)

        pmfe_raw = subprocess.run(command, stdout=subprocess.PIPE, encoding='UTF-8')
        pmfe = [b for b in pmfe_raw.stdout.split()]
        print(pmfe)
        sig = Point(pmfe[1],pmfe[2],pmfe[3],pmfe[4])

        # print(x,y,z,w)
        #HANDLE ERRORS
        os.chdir(cwd)
        return (sig)

        # /home/owen/Documents/research/pmfe/pmfe-findmfe

    def call_subopt(self, a, b, c, d):
        cwd = os.getcwd()
        os.chdir(self.pmfePath)
        command = f"./pmfe-subopt -a {a} -b {b} -c {c} -d {d} -o out.tmp {self.filePath}".split()
        
        subprocess.run(command) # text=True)
        #HANDLE ERRORS
        #
        #
        #
        suboptScores = [] #tuples x,y,z,w
        with open("out.tmp", "r") as out:
            for line in out.readlines()[4:]:
                line = line.split()                
                x,y,z,w = Point(line[2], line[3], line[4], line[5])
                suboptScores.append((x,y,z,w))
            # print(out.readlines());

        os.remove("out.tmp")
        os.chdir(cwd)

        return (suboptScores)
    
    def transform_z(self, point):
        x,y,z,w = point
        return Point(x, y, z - (3*x), w)

# interface = pmfeInterface("/home/owen/Documents/research/pmfe", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta")

# print(interface.vertex_oracle(1, 0, 1, 1))