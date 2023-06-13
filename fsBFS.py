# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from collections import defaultdict
from sympy import Point, Line, convex_hull, Segment, Polygon
from tippingSegment import TippingSegment

import json

from pmfeInterface import pmfeInterface
from tippingPoint import tippingPoint

class fanSlice():
    def __init__(self, pmfe, rna_file, transform = False):
        self.bVal = 0
        self.dVal = 1

        self.nntm = pmfeInterface(pmfe, rna_file, transform=True)

        self.pointQueue = []
        self.tippingSegments = []
        self.visited = set()
        self.signatures = defaultdict(set)

        self.tippingLinesComputed = 0

    # def __init__(self):
    #     self.__init__(Fraction(50),Fraction(50))
    
    def build(self, aB, cB):
        self.aB = aB
        self.cB = cB
        # Initialize
        #return starting queue with all the 
        self.initialize_square()   

        # print(self.pointQueue)
        # print(self.tippingSegments)
        while len(self.pointQueue) > 0:
            print("LENGTH REMAINING:", len(self.pointQueue))
            point = self.pointQueue.pop(0)

            adjacent_points, segments = self.get_adjacent(point)
            
            for p in adjacent_points:
                if p.point not in self.visited:
                    self.visited.add(p.point)
                    self.pointQueue.append(p)
                    self.signatures[Point(p.scoreL[0], p.scoreL[2])].add(p.point)
                    self.signatures[Point(p.scoreR[0], p.scoreR[2])].add(p.point)
            
            for s in segments: 
                if s not in self.tippingSegments:
                    self.tippingSegments.append(s)

            print("SIZE REMAINING END", len(self.pointQueue))
        
        print(self.visited)
        self.save_data()

    def initialize_square(self):
        p1, p2, p3, p4 = Point(self.aB, self.cB), Point(-self.aB, self.cB), Point(-self.aB, -self.cB), Point(self.aB, -self.cB)
        s2 = self.nntm.vertex_oracle(p2[0], self.bVal, p2[1], self.dVal)
        s1 = self.nntm.vertex_oracle(p1[0], self.bVal, p1[1], self.dVal)
        s3 = self.nntm.vertex_oracle(p3[0], self.bVal, p3[1], self.dVal)
        s4 = self.nntm.vertex_oracle(p4[0], self.bVal, p4[1], self.dVal)

        print(self.nntm.pmfeCalls)

        #(p1,p2)
        print("1,2")
        self.addBoundryPointToQueue(self.findIntersections(p1, p2, s1, s2))
        print("pmfe calls:", self.nntm.pmfeCalls)
        print("TL:", self.tippingLinesComputed)

        #(p2,p3)
        print("2,3")
        self.addBoundryPointToQueue(self.findIntersections(p2, p3, s2, s3))
        print("pmfe calls:", self.nntm.pmfeCalls)
        print("TL:", self.tippingLinesComputed)

        #(p3,p4)
        print("3,4")
        self.addBoundryPointToQueue(self.findIntersections(p3, p4, s3, s4))
        print("pmfe calls:", self.nntm.pmfeCalls)
        print("TL:", self.tippingLinesComputed)


        #(p4, p1):
        print("4, 1")
        self.addBoundryPointToQueue(self.findIntersections(p4, p1, s4, s1))
        print("pmfe calls:", self.nntm.pmfeCalls)
        print("TL:", self.tippingLinesComputed)

    
    def addBoundryPointToQueue(self, points):
        for i, (p, score) in enumerate(points):
            point, _ = p
            
            #ISSUE: Stop saving extra endpoint data with points. Or change to tipping point earlier?
            if i+1 < len(points):
                self.tippingSegments.append(TippingSegment(score, score, Segment(point, points[i+1][0][0]), boundry=True))
            if point in self.visited:
                continue
            else:
                # print(score, point)
                self.pointQueue.append(tippingPoint(point, score, score, boundry=True))
                self.visited.add(point)


    def findIntersections(self, p1, p2, s1, s2):
        intersection, endpoints = self.findIntersection(p1, p2, s1, s2)
        intersectionVal = (intersection, endpoints)
        # print("INTERSECTION", intersection)
        if intersection == None or intersection == p1 or intersection == p2:
            # print("EQUALITY")
            return []
        # if findIntersection(p1, p2, s1, s2) == []:
        #     return []
        score = self.nntm.vertex_oracle(intersection[0], self.bVal, intersection[1], self.dVal)
        # print("SCORE", score)

        if s1 == score:
            # print("S1 MATCH")
            return self.findIntersections(intersection, p2, score, s2) + [(intersectionVal, score)]
        
        if s2 == score: 
            # print("S2 MATCH")
            return self.findIntersections(p1, intersection, s1, score) + [(intersectionVal, score)]
        
        # print("Intersection", intersection, p2)
        return self.findIntersections(intersection, p2, score, s2) + self.findIntersections(p1, intersection, s1, score)


    def findIntersection(self, p1, p2, s1, s2):
        # print ("S1 S2:", s1, s2)
        # print("P1 P2:", p1, p2)
        self.tippingLinesComputed += 1

        paramLine = Line(p1, p2)
        
        x1, y1, z1, w1 = s1
        x2, y2, z2, w2 = s2
        
        k1 = self.bVal * y1 + self.dVal * w1
        k2 = self.bVal * y2 + self.dVal * w2

        if ((z2 - z1) == 0 and (x1-x2) == 0):
            return None, None
            # print("SAME x, z SIGNATURE")
        
        # print("s1, s2", s1, s2)
        #define line
        if ((z2 - z1) == 0): 
            #VERTICAL LINE
            a = (k2 - k1) / (x1 - x2)
            # print(self.aB, k2, k1, x1, x2, a)
            point1 = Point(a, self.cB)
            point2 = Point(a, -self.cB)
            line = Line(point1, point2)

            # print(point1, point2, paramLine,  line.intersection(paramLine))
            interPoint = line.intersection(paramLine)[0]
            # print("INTERPOINT", interPoint)
            return interPoint, (point1, point2)

        else:
            x = (x1 - x2)
            const = (k1 - k2)
            point1 = Point(self.aB, (self.aB * x + const) / (z2 - z1))
            point2 = Point(-self.aB, (-self.aB * x + const) / (z2 - z1))
            
            # print("Po1 Po2:", point1, point2)
            interPoint = Line(point1, point2).intersection(paramLine)[0]
            # print("INTERPOINT", interPoint) 

            return interPoint, (point1, point2)

    def get_adjacent(self, p: tippingPoint):
        subopt = self.nntm.subopt_oracle(p.point[0], self.bVal, p.point[1], self.dVal)
        print(subopt)

        sigs = [*set(subopt)]
        print("SIGNATURES", sigs)
        if len(sigs) > 2: 
            sigs = self.sort_signatures(sigs) 
        else:
            #If there are only 2 signatures we want the left signature at index 0 and right at index 0. [sig_l, sig_r]
            if not p.boundry:
                print(f"ERROR: NON-BOUNDRY POINT WITH {len(sigs)} SIGNATURES")
            if p.point[0] == self.aB:
                sigs.sort(key=lambda t: t[2], reverse=True)
            elif p.point[0] == -self.aB:
                sigs.sort(key=lambda t: t[2])
            elif p.point[1] == self.cB:
                sigs.sort(key=lambda t: t[0])
            elif p.point[1] == -self.cB:
                sigs.sort(key=lambda t: t[0], reverse=True)

        adjPoints = []
        adjSegments = []
        print("SIGNATURES AGAIN! SO COOL!", sigs)
        for i in range(-1, len(sigs) - 1):
            seg, point = TippingSegment.construct_from_point(p, sigs[i], sigs[i + 1], self.nntm, segments = self.tippingSegments)
            adjSegments.append(seg)
            adjPoints.append(point)

            if len(sigs) == 2:
                break

        return adjPoints, adjSegments

    #N
    def sort_signatures(self, sigs):
        sigs2D = [Point(sig[0], sig[2]) for sig in sigs]
        pointDict = dict(zip(sigs2D,sigs))
        hull = convex_hull(*sigs2D)

        # print(type(hull), hull is Segment2D)
        # if type(hull) == Segment2D:
        #     print("SEGMENT")
        #     return [pointDict[hull.p1], pointDict[hull.p2]]
        return([pointDict[v] for v in hull.vertices])
    

    def save_data(self):
        # Construct Polygons
        polygons = []
        self.signatures[Point(0,1)].add((1,2))
        self.signatures[Point(0,1)].add((1,3))
        self.signatures[Point(0,1)].add((1,4))
        self.signatures[Point(0,1)].add((1,5))
        for s in self.signatures.keys():
            polygons.append((s, convex_hull(*self.signatures[s])))
        
        with open("polygons.json", "w") as f:
            f.write(json.dumps(polygons))
        with open("visited.json", "w") as f:
            f.write(json.dumps([self.visited]))
        with open("segments.json", "w") as f:
            f.write(json.dumps(self.tippingSegments))


    # def line_intersection(self, line1, line2):
    #     adiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    #     cdiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    #     def det(a, b):
    #         return a[0] * b[1] - a[1] * b[0]

    #     div = det(xdiff, ydiff)
    #     if div == 0:
    #         raise Exception('lines do not intersect')

    #     d = (det(*line1), det(*line2))
    #     a = det(d, adiff) / div
    #     c = det(d, cdiff) / div
        
    #     return a, c

# s = fanSlice(50, 50)
# s.build()

# print(*[str(p)[7:] for p in s.searched.keys()], sep=",")