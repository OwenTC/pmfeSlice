from fsBFS import FanSlice
from sympy import convex_hull

        # with open("polygons.json", "w") as f:
        #     f.write(json.dumps(polygons))
        # with open("visited.json", "w") as f:
        #     f.write(json.dumps([self.visited]))
        # with open("segments.json", "w") as f:
        #     f.write(json.dumps(self.tippingSegments))

fan = FanSlice("/home/owen/Documents/research/pmfe/", "/home/owen/Documents/research/RNA_Data/tRNA/o.nivara_tRNA.fasta", transform=True)

fan.build(50, 50)
fan.save_data()