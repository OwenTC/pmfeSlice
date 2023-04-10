import argparse
from fsWithoutSubopt import fanSlice as FS
from fsWithSubopt import fanSlice as FS_subopt
import squareCompute

#Takes in a dictionary of scores with corresponding points and saves it.
def saveScores(scores):
    with open(args.output, 'w') as f:
        f.write("score, points\n")
        for s in scores.keys():
            f.write(f"{s}, {scores[s]}\n")

parser = argparse.ArgumentParser(description="Computes Approximate Slice of Normal Fan By computing Squares")
parser.add_argument("output")
parser.add_argument("rna_file")
parser.add_argument("pmfe_path")
parser.add_argument("--subopt", action="store_true")
parser.add_argument("-s", "--square", type=int, nargs=2)

args = parser.parse_args()

fanSlice = FS(args.pmfe_path, args.rna_file) if not args.subopt else FS_subopt(args.pmfe_path, args.rna_file)

if(args.square):
    saveScores(squareCompute.computeSquare(fanSlice, args.square[0], args.square[1]))