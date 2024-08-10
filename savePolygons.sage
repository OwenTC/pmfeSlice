from numpy import random

poly = polygon([(0,0), (0,0), (0,0)], alpha=0)
colors = ["blue", "green", "orange", "purple","cyan"]
with open("polygons_11.txt", "r") as p:
    for i, p in enumerate(p.readlines()):
        # shuffle(colors)
        data = p.strip("\n").split(": ")
        points = [tuple(p.strip("()").replace(" ", "").split(",")) for p in data[1].split(",(")]
        points = [(Rational(p[0]), Rational(p[1])) for p in points]
        poly = poly + polygon(points, color=list(random.rand(3,)), dpi=4000)
        poly += point((56/5,-67/10), color="black",size=1,zorder=100)

        for p in [(-50,103/10),(-50,323/30),(-50,173/15),(-50,361/30),(-50,182/15),(-50,188/15),(-50,193/15),(-50,403/30),(-50,419/30),(-50,147/10),(-50,16),(-50,81/5),(-50,88/5),(-50,187/10),(50,-173/26),(50,-7),(50,-73/10),(50,-39/5),(50,-42/5),(50,-91/10),(50,-93/10),(50,-47/5),(50,-101/10),(50,-56/5),(50,-121/10),(50,-253/10),(50,-128/5),(50,-521/20),(50,-261/10),(50,-529/20),(50,-53/2),(50,-136/5),(50,-551/20),(50,-761/25),(50,-169/5),(50,-819/20),(-50,171/10)]:
            poly += point(p, color="black",size=1,zorder=100)
poly.save("polygraph.svg")