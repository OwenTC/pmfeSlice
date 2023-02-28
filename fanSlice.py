# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from fractions import Fraction
from queue import Queue
from sympy import Point, Line

from pmfeInterface import pmfeInterface

class fanSlice():
    def __init__(self):
        self.aB = 50
        self.cB = 50
        self.bVal = 0
        self.dVal = 1

        self.nntm = pmfeInterface("/home/owen/Documents/research/pmfe", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta")

        self.bordersRemaing = Queue()
        self.searched = {}

    # def __init__(self):
    #     self.__init__(Fraction(50),Fraction(50))
    


    def build(self):
        # Initialize
        #return starting queue with all the 
        self.initialize()
        return
    
    def initialize(self):
        p1, p2, p3, p4 = Point(self.aB, self.cB), Point(-self.aB, self.cB), Point(-self.aB, -self.cB), Point(self.aB, -self.cB)
        s1 = self.nntm.vertex_oracle(p1[0], self.bVal, p1[1], self.dVal)[0]
        s2 = self.nntm.vertex_oracle(p2[0], self.bVal, p2[1], self.dVal)[0]
        s3 = self.nntm.vertex_oracle(p3[0], self.bVal, p3[1], self.dVal)[0]
        s4 = self.nntm.vertex_oracle(p4[0], self.bVal, p4[1], self.dVal)[0]

        #(p1,p2)
        for p, s in self.findIntersections(p1, p2, s1, s2):
            if p in self.searched:
                continue
            else:
                self.bordersRemaing.put(p)
                self.searched[p] = s

        #(p2,p3)
        for p, s in self.findIntersections(p2, p3, s2, s3):
            if p in self.searched:
                continue
            else:
                self.bordersRemaing.put(p)
                self.searched[p] = s
        #(p3,p4)
        for p, s in self.findIntersections(p3, p4, s3, s4):
            if p in self.searched:
                continue
            else:
                self.bordersRemaing.put(p)
                self.searched[p] = s

        #(p4, p1):
        for p, s in self.findIntersections(p3, p4, s3, s4):
            if p in self.searched:
                continue
            else:
                self.bordersRemaing.put(p)
                self.searched[p] = s
    

    # def findIntersection(self, s1, s2):
    #     x1, y1, z1, w1 = s1[0], s1[1], s1[2], s1[3]     
    #

    def findIntersections(self, p1, p2, s1, s2):
        intersection = findIntersection(p1, p2, s1, s2)
        # if findIntersection(p1, p2, s1, s2) == []:
        #     return []
        scores = self.nntm.vertex_oracle(intersection[0], self.bVal, intersection[1], self.dVal)

        if s1 in scores and s2 in scores: 
            return [(intersection, scores)]

        if s1 in scores:
            return self.findIntersections(p1, p2, intersection, s2).append((intersection, scores))
        
        if s2 in scores: 
            return self.findIntersections(p1, p2, s1, intersection).append((intersection, scores))
        
        return self.findIntersections(p1, p2, intersection, s2) + self.findIntersections(p1, p2, s1, intersection)


    def findIntersection(self, p1, p2, s1, s2):
        paramLine = Line(p1, p2)

        x1, y1, z1, w1 = s1
        x2, y2, z2, w2 = s2
        
        k1 = self.bVal * y1 + self.dVal * w1
        k2 = self.bVal * y2 + self.dVal * w2

        if ((z2 - z1) == 0 and (x1-x2) == 0):
            raise("SAME x, z SIGNATURE")
        
        #define line
        if ((z2 - z1) == 0): 
            #Vertical, return a-intersection
            a = (k2 - k1) / x1 - x2
            line = Line(Point(a, self.cB), Point(a, -self.cB))
            return line.intersection(paramLine)[0]
        else:
            x = (x1 - x2)
            const = (k1 - k1)
            point1 = Point(self.aB, (x + const) / (z2 - z1))
            point2 = Point(-self.aB, (x + const) / (z2 - z1))
            
            return Line(point1, point2).intersection(paramLine)[0]

        
    
    def line_intersection(self, line1, line2):
        adiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        cdiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        a = det(d, adiff) / div
        c = det(d, cdiff) / div
        
        return a, c


s = fanSlice()
s.build()