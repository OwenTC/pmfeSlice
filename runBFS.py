from fsBFS import fsBFS as FanSlice
from sympy import Rational
import argparse
from os import path

parser = argparse.ArgumentParser(description="Computes Slice of Normal Fan")
parser.add_argument("fasta", nargs=1, help="fasta file")
parser.add_argument("pmfe_path", help="path to pmfe")
parser.add_argument("-b", default=0, type=Rational, help="b value")
parser.add_argument("-cB", default=50, help="Upper c bound")
parser.add_argument("-aB", default=50, help="Upper a bound")
parser.add_argument("-cb", default=-50, help="Lower c bound")
parser.add_argument("-ab", default=-50, help="Lower a bound")

args = parser.parse_args()

# (109/10, -5),(64/5, -119/20),(49/2, -119/20),(207/10, -5)

fan = FanSlice(args.pmfe_path, args.fasta[0], bVal = args.b, transform=False, aB=args.aB, cB=args.cB, ab=args.ab, cb=args.cb)

print(path.basename(args.fasta[0]))

fan.build()
fan.save_data()