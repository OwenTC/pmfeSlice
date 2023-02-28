import subprocess
# from os import path
import os
from fractions import Fraction

class pmfeInterface:
    #Initialize with b and d!!!
    def __init__(self, pmfePath, filePath):
        self.pmfePath = pmfePath
        self.filePath = filePath

    def vertex_oracle(self, a, b, c, d):
        return self.call_subopt(a,b,c,d)

    # Internal 
    def call_pmfe(self, a, b, c, d):
        cwd = os.getcwd()
        os.chdir(self.pmfePath)
        command = f"./pmfe-findmfe -a {a} -b {b} -c {c} -d {d} {self.filePath}".split()
        # print(command)

        pmfe = subprocess.run(command, capture_output=True, text=True).stdout.split()
        x, y, z, w = Fraction(pmfe[1]), Fraction(pmfe[2]), Fraction(pmfe[3]), Fraction(pmfe[4])

        # print(x,y,z,w)
        #HANDLE ERRORS
        os.chdir(cwd)

        
        return (pmfe)

        # /home/owen/Documents/research/pmfe/pmfe-findmfe

    def call_subopt(self, a, b, c, d):
        cwd = os.getcwd()
        os.chdir(self.pmfePath)
        command = f"./pmfe-subopt -a {a} -b {b} -c {c} -d {d} -o out.tmp {self.filePath}".split()
        
        subprocess.run(command, text=True)
        #HANDLE ERRORS
        #
        #
        #
        suboptScores = [] #tuples x,y,z,w
        with open("out.tmp", "r") as out:
            for line in out.readlines()[4:]:
                line = line.split()                
                x,y,z,w = Fraction(line[2]), Fraction(line[3]), Fraction(line[4]), Fraction(line[5])
                suboptScores.append((x,y,z,w))
            # print(out.readlines());

        os.remove("out.tmp")
        os.chdir(cwd)

        return (suboptScores)

# interface = pmfeInterface("/home/owen/Documents/research/pmfe", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta")

# print(interface.vertex_oracle(1, 0, 1, 1))