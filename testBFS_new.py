from posixpath import basename
from fsBFS import fsBFS as FanSlice
from sympy import Rational
import argparse
from os import path

        # with open("polygons.json", "w") as f:
        #     f.write(json.dumps(polygons))
        # with open("visited.json", "w") as f:
        #     f.write(json.dumps([self.visited]))
        # with open("segments.json", "w") as f:
        #     f.write(json.dumps(self.tippingSegments))

parser = argparse.ArgumentParser()
parser.add_argument("fasta", nargs=1, help="fasta file")

args = parser.parse_args()

fan = FanSlice("/home/owen/Documents/research/pmfe/", args.fasta[0], bVal = Rational("0"), transform=False)

print(path.basename(args.fasta[0]))

fan.build()
fan.save_data(f"test_data/{basename(args.fasta[0])}.txt")