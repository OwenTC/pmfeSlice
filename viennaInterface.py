import subprocess
# from os import path
import os
from sympy import Point, Line, Rational

import sys
sys.path.append("/home/owen/Documents/research/ViennaCode/ViennaRNA-2.5.1/interfaces/Python")
import RNA

class ViennaInterface:
    #Initialize with b and d!!!
    def __init__(self, pmfePath: str, filePath:str, transform: bool = False): 
        self.pmfePath = pmfePath
        self.filePath = filePath
        self.transform = transform
        self.pmfeCalls = 0
        self.suboptCalls = 0

        #Setup Vienna
        self.md = RNA.md()
        self.md.uniq_ML = 1
        self.md.compute_bpp = 0
        self.fc = RNA.fold_compound(self.sequence_from_fasta(), self.md)

    #Calls pmfe with params a, b, c, d
    def vertex_oracle(self, a: Rational, b: Rational, c: Rational, d: Rational):
        self.pmfeCalls += 1
        if self.transform:
            a = a-(c*3)
            return self.transform_z(self.get_mfe(a,b,c,d)) #self.transform_z

        return self.get_mfe(a,b,c,d)

    #Calls subopt with params a, b, c, d
    def subopt_oracle(self, a: Rational, b: Rational, c: Rational, d: Rational, eng=15):
        self.suboptCalls += 1
        if self.transform:
            a = a-(c*3)
            subopt= self.get_subopt(a,b,c,d)
            transformed = []
            for s in subopt:
                transformed.append(self.transform_z(s))

            return transformed
        return self.get_subopt(a,b,c,d,eng=eng)

#----------------------------------------------------------------------------------------------------
    # Internal Methods
    
    #Returns sig (x, y, z) not w because scorer outputs inf.
    def scored_structure(self, struct):
        full_path = os.path.join(self.pmfePath, "pmfe-scorer")
        command = f"{full_path} {self.filePath} {struct}".split()
        print(" ".join(command))

        pmfe_raw = subprocess.run(command, stdout=subprocess.PIPE, encoding='UTF-8')
        # return(pmfe_raw)
        lines = [tuple(b.split(":")) for b in pmfe_raw.stdout.split("\n")][:-1]
        sig = tuple(int(l[1]) for l in lines[0:3]) #Ignore w and parametrized energy lines since they are inf
        w_val = float(lines[-3][1].replace(" ", "").split("≈")[1])
        sig += (w_val*100,) #Multiply by 100 for kCals to dcCals

        #HANDLE ERRORS
        #
        #
        #

        return sig
    
    #NEED TO TEST THIS METHOD RIGOROUSLY
    def compute_w(self, sig, params, eng):
        #times 100 to convert from kkals to dckals
        # print(list((s,p) for s,p in zip(sig, params[:3])))
        return (eng*100 - sum((s*p) for s,p in zip(sig, params[:3])))/params[3]

    def change_params(self, a, b, c):
        #String b 0 a 0 c 0 found from /ViennaRNA-2.5.1/misc/rna_turner1999.par (search for "ML_params")
        string = f"## RNAfold parameter file v2.0\n# ML_params\n{b} 0 {a} 0 {c} 0 \n"

        RNA.params_load_from_string(string)
        p = RNA.param(self.md)
        exp_p = RNA.exp_param(self.md)

        # substitute energy parameters within the fold_compound
        # with the 'new' global settings
        self.fc.params_subst(p)
        self.fc.exp_params_subst(exp_p)

    #NEED TO TEST THIS METHOD RIGOROUSLY
    def get_mfe(self, a, b, c, d=1):
        #Round since Vienna accepts integer inputs
        a = int(round(a, 0))
        b = int(round(b, 0))
        c = int(round(c, 0))
        # print("PARAMS", a, b, c, d)
        self.change_params(a, b, c)
        # compute MFE
        (structure, en) = self.fc.mfe()
        # print(structure, en)
        print(a, b, c, d)
        sig_no_w = self.scored_structure(structure)
        sig = sig_no_w[:3] + (self.compute_w(sig_no_w, (a,b,c,d), en),)
        # sig = sig_no_w
        print("ENERGY DIFF", (sig_no_w[-1] - sig[-1]), sig, sig_no_w, en)
        # print("STRUCTURE SIG", structure, sig, en)
        return sig
    
    def sequence_from_fasta(self):
        with open(self.filePath) as f:
            seq = f.readline()
            while seq[0] == ">":
                seq = f.readline()
            return seq.strip("\n")

    def get_subopt(self, a, b, c, d=1, eng=5):
        a = int(round(a, 0))
        b = int(round(b, 0))
        c = int(round(c, 0))

        self.change_params(a, b, c)

        # compute MFE
        # print(self.fc.subopt(0))
        #120 here is tunned and it seems like it works
        sigs_no_w = ((self.scored_structure(s.structure), s.energy) for s in self.fc.subopt(eng))
        subopt = [s[:3] + (self.compute_w(s, (a,b,c,d),en),) for s, en in sigs_no_w]
        # subopt = [s for s,_ in sigs_no_w]

        return subopt
    
    def transform_z(self, point):
        x,y,z,w = point
        return Point(x, y, z - (3*x), w)

# interface = pmfeInterface("/home/owen/Documents/research/pmfe", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta")

# print(interface.vertex_oracle(1, 0, 1, 1))