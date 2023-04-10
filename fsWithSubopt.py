# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from sympy import Point, Line

from pmfeInterface import pmfeInterface
from tippingPoint import tippingPoint


class fanSlice():
    def __init__(self, pmfe, rna_file):
        self.bVal = 0
        self.dVal = 1

        self.nntm = pmfeInterface(pmfe, rna_file)

        self.bordersRemaining = []
        self.searched = {}

    # def __init__(self):
    #     self.__init__(Fraction(50),Fraction(50))
    
    def build(self, aB, cB):
        self.aB = aB
        self.cB = cB
        # Initialize
        #return starting queue with all the 
        self.initialize()   

        while len(self.bordersRemaining) > 0:
            print("LENGTH REMAINING:", len(self.bordersRemaining))
            p = self.bordersRemaining.pop(len(self.bordersRemaining) - 1)
            ps, newPoints = p.findEndpoint(1)
            point, scores = ps

            if point in self.searched:
                continue
            else:
                self.bordersRemaining.extend(newPoints)
                self.searched[point] = (0, scores)

            p1, p2 = endpoints
            intersections = self.findIntersections(p1, p2, s1, s2)
            self.addToQueue([(p, s) for p, s in intersections if score in s])

            print("SIZE REMAINING END", len(self.bordersRemaining))

    def initialize(self):
        p1, p2, p3, p4 = Point(self.aB, self.cB), Point(-self.aB, self.cB), Point(-self.aB, -self.cB), Point(self.aB, -self.cB)
        s1 = self.nntm.subopt_oracle(p1[0], self.bVal, p1[1], self.dVal)[0]
        s2 = self.nntm.subopt_oracle(p2[0], self.bVal, p2[1], self.dVal)[0]
        s3 = self.nntm.subopt_oracle(p3[0], self.bVal, p3[1], self.dVal)[0]
        s4 = self.nntm.subopt_oracle(p4[0], self.bVal, p4[1], self.dVal)[0]

        #(p1,p2)
        print("1,2")
        self.addBoundryPointToQueue(self.findIntersections(p1, p2, s1, s2))
        
        #(p2,p3)
        print("2,3")
        self.addBoundryPointToQueue(self.findIntersections(p2, p3, s2, s3))

        #(p3,p4)
        print("3,4")
        self.addBoundryPointToQueue(self.findIntersections(p3, p4, s3, s4))

        #(p4, p1):
        print("4, 1")
        self.addBoundryPointToQueue(self.findIntersections(p4, p1, s4, s1))

    # def findIntersection(self, s1, s2):
    #     x1, y1, z1, w1 = s1[0], s1[1], s1[2], s1[3]     
    #        

    def addBoundryPointToQueue(self, points):
        for p, score in points:
            point, endpoints = p 
            if point in self.searched:
                continue
            else:
                score = [*set(score)]
                print(score, point)
                self.bordersRemaining.append(tippingPoint(self.nntm, self.bVal, self.dVal, point, score[0], score[1]))
                self.searched[point] = (endpoints, score)

    def findIntersections(self, p1, p2, s1, s2):
        intersection, endpoints = self.findIntersection(p1, p2, s1, s2)
        intersectionVal = (intersection, endpoints)
        # print("INTERSECTION", intersection)
        if intersection == None:
            return []
        # if findIntersection(p1, p2, s1, s2) == []:
        #     return []
        scores = self.nntm.subopt_oracle(intersection[0], self.bVal, intersection[1], self.dVal)
        # print("SCORES", scores)

        if s1 in scores and s2 in scores: 
            return [(intersectionVal, scores)]

        #We can just return scores[0] because once all scores are correct.
        if s1 in scores:
            return self.findIntersections(p1, intersection, scores[0], s2).append((intersectionVal, scores))
        
        if s2 in scores: 
            return self.findIntersections(intersection, p2, s1, scores[0]).append((intersectionVal, scores))
        
        return self.findIntersections(intersection, p2, s1, scores[0]) + self.findIntersections(p1, intersection, scores[0], s2)


    def findIntersection(self, p1, p2, s1, s2):
        paramLine = Line(p1, p2)

        # print ("S1 S2:", s1, s2)
        # print("P1 P2:", p1, p2)
        x1, y1, z1, w1 = s1
        x2, y2, z2, w2 = s2
        
        k1 = self.bVal * y1 + self.dVal * w1
        k2 = self.bVal * y2 + self.dVal * w2

        if ((z2 - z1) == 0 and (x1-x2) == 0):
            return None, None
            # print("SAME x, z SIGNATURE")
        
        #define line
        if ((z2 - z1) == 0): 
            #Vertical, return a-intersection
            a = (k2 - k1) / x1 - x2
            point1 = Point(a, self.cB)
            point2 = Point(a, -self.cB)
            line = Line(point1, point2)
            interPoint = line.intersection(paramLine)[0]
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
