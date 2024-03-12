from fsBFS import fsBFS as FanSlice
from sympy import Rational
import argparse
from os import path
from sympy import *

parser = argparse.ArgumentParser(description="Computes Slice of Normal Fan")
parser.add_argument("fasta", nargs=1, help="fasta file")
parser.add_argument("pmfe_path", help="path to pmfe")
parser.add_argument("--b_val", default=0, type=Rational, help="b value")
parser.add_argument("-C", type=Rational, default=50, help="Upper c bound")
parser.add_argument("-A", type=Rational, default=50, help="Upper a bound")
parser.add_argument("-c", type=Rational, default=-50, help="Lower c bound")
parser.add_argument("-a", type=Rational, default=-50, help="Lower a bound")
parser.add_argument("-O", "--transform", action="store_true", help="Transform Output")

args = parser.parse_args()
print(args)

# (109/10, -5),(64/5, -119/20),(49/2, -119/20),(207/10, -5)

fan = FanSlice(args.pmfe_path, args.fasta[0], bVal = args.b_val, transform=args.transform, aB=args.A, cB=args.C, ab=args.a, cb=args.c)

# print(path.basename(args.fasta[0]))


# fan.pointQueueHull = convex_hull((-50, 47/5), (50, -321/10), (1669/100, -97/10), (39/5, -23/5), (-51/10, 5/2), (-50, 187/10))

# ray = Ray(Point2D(39/5, -23/5),Point2D(44/5, -51/10))
# point = Point2D(39/5, -23/5)

# print(fan.find_ray_hull_intersection(ray, point))

fan.build()
fan.save_data()