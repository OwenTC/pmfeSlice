
from sympy import Point, convex_hull
# import numpy as np

from pmfeInterface import pmfeInterface


class tippingPoint():
    def __init__(self, point, scoreL, scoreR, boundry = False) -> None:
        self.point = Point(point)
        self.scoreL = scoreL
        self.scoreR = scoreR
        self.boundry = boundry
        # self.delta_x = score1[2] - score2[2]
        # self.delta_z = -(score1[0] - score2[0])

    #     self.aB = 50
    #     self.cB = 50

    #     self.nntm = interface

    #     # print(self)

    # def sort_signatures(self, sigs):
    #     base_point = Point(sigs[0][0], sigs[0][2])
    #     height = base_point[1]
    #     base_line = Line(base_point,Point(100,height)) #Creates a "horizontal" line in signature space to measure angles

    #     above = []
    #     below = []
    #     for s in sigs[1:]:
    #         s_point = Point(-s[0], -s[2])
    #         line = Line(base_point, s_point)
    #         angle = base_line.angle_between(line)

    #         if s_point[1] >= height:
    #             above.append((s, angle))
    #         else:
    #             below.append((s, angle))

    #     sorted_above = sorted([(sig,k) for sig,k in above], key = lambda t: t[1])
    #     sorted_below = sorted([(sig,k) for sig,k in below], key = lambda t: t[1], reverse = True)
    #     sorted_sigs = [(sigs[0], 0)] + sorted_above + sorted_below
    #     print(self.point, sorted_sigs)
    #     return [s for s, _ in sorted_sigs]

    # def getEndpoint(self, p1, p2, s1, s2):
    #     intersection, _ = self.findIntersection(p1, p2, s1, s2)
    #     print("INTERSECTION", intersection)
    #     if intersection == None:
    #         print("INTERSECTION NONE ERROR")
    #     # if findIntersection(p1, p2, s1, s2) == []:
    #     #     return []
    #     scores = [*set(self.nntm.vertex_oracle(intersection[0], self.b, intersection[1], self.d))]
    #     # print("SCORES", scores)

    #     if s1 in scores and s2 in scores: 
    #         return (intersection, scores)
        
    #     return self.getEndpoint(p1, intersection, s1, scores[0])
    
    # def findIntersection(self, p1, p2, s1, s2):
    #     paramLine = Line(p1, p2)

    #     print ("S1 S2:", s1, s2)
    #     print("P1 P2:", p1, p2)
    #     x1, y1, z1, w1 = s1
    #     x2, y2, z2, w2 = s2
        
    #     k1 = self.b * y1 + self.d * w1
    #     k2 = self.b * y2 + self.d * w2

    #     if ((z2 - z1) == 0 and (x1-x2) == 0):
    #         return None, None
    #         # print("SAME x, z SIGNATURE")
        
    #     #define line
    #     if ((z2 - z1) == 0): 
    #         #Vertical, return a-intersection
    #         a = (k2 - k1) / x1 - x2
    #         point1 = Point(a, self.cB)
    #         point2 = Point(a, -self.cB)
    #         line = Line(point1, point2)
    #         interPoint = line.intersection(paramLine)[0]
    #         return interPoint, (point1, point2)

    #     else:
    #         x = (x1 - x2)
    #         const = (k1 - k2)
    #         point1 = Point(self.aB, (self.aB * x + const) / (z2 - z1))
    #         point2 = Point(-self.aB, (-self.aB * x + const) / (z2 - z1))
            
    #         # print("Po1 Po2:", point1, point2)
    #         interPoint = Line(point1, point2).intersection(paramLine)[0]
    #         # print("INTERPOINT", interPoint) 

    #         return interPoint, (point1, point2)


    def __repr__(self) -> str:
        return f"{self.point}"
    
    def __eq__(self, other: object) -> bool:
        if type(other) != tippingPoint:
            return False

        return self.point == other.point