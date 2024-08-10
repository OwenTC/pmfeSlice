from viennaInterface import ViennaInterface
from sys import argv
import sys
sys.path.append("/home/owen/Documents/research/ViennaCode/ViennaRNA-2.5.1/interfaces/Python")
import RNA
from scorer import RNAStructure
import pandas as pd

def sequence_from_fasta(filePath):
        with open(filePath) as f:
            seq = f.readline()
            while seq[0] == ">":
                seq = f.readline()
            return seq.strip("\n")

eng = 10000000 #C max int 
seq_path = argv[1]

#Vienna setup
md = RNA.md()
md.uniq_ML = 1
md.compute_bpp = 0
fc = RNA.fold_compound(sequence_from_fasta(seq_path), md)

def change_params(a, b, c):
        #String b 0 a 0 c 0 found from /ViennaRNA-2.5.1/misc/rna_turner1999.par (search for "ML_params")
        string = f"## RNAfold parameter file v2.0\n# ML_params\n{b} 0 {a} 0 {c} 0 \n"

        RNA.params_load_from_string(string)
        p = RNA.param(md)
        exp_p = RNA.exp_param(md)

        # substitute energy parameters within the fold_compound
        # with the 'new' global settings
        fc.params_subst(p)
        fc.exp_params_subst(exp_p)

# def get_w(params, sig, eng):
#         #times 100 to convert from kkals to dckals
        # return (round(eng*100) - sum((s*p) for s,p in zip(sig, params[:3])))/params[3]

def get_subopt(a, b, c, d=1, eng=5):
        a = int(round(a, 0))
        b = int(round(b, 0))
        c = int(round(c, 0))

        change_params(a, b, c)

        # compute MFE
        # print(self.fc.subopt(0))
        #120 here is tunned and it seems like it works
        structs = ((RNAStructure(s.structure),s.energy) for s in fc.subopt(eng))
        sigs = list(tuple(s[0].score_structure())+(s[0].structure,) for s in structs)
        # sigs_w_eng = [(get_w((a,b,c,d),s[0],s[2]),s[1]) for s in sigs]
        # subopt = [s for s,_ in sigs_no_w]

        return sigs

Vinterface = ViennaInterface("/home/owen/Documents/research/pmfe2023/",seq_path, transform=False)

possible_stucts = pd.DataFrame(get_subopt(0,0,0,1,eng=eng), columns=["x","y","z","dot_brac"])
possible_stucts.to_csv("c2_possible_structs.csv", index=False)

print(possible_stucts.shape)
# max_x = possible_stucts["x"].max()
# possible_stucts[possible_stucts["x"] == max_x]
