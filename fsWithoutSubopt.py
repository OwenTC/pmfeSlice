# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from sympy import Point, Line

from pmfeInterface import pmfeInterface
from tippingPoint import tippingPoint

class fanSlice():
    def __init__(self, pmfe, rna_file, transform = False):
        self.bVal = 0
        self.dVal = 1

        self.nntm = pmfeInterface(pmfe, rna_file, transform)

        self.bordersRemaining = []
        self.searched = {}

    # def __init__(self):
    #     self.__init__(Fraction(50),Fraction(50))
    
    def build(self, aB, cB):
        self.aB = aB
        self.cB = cB
        # Initialize
        #return starting queue with all the 
        self.initialize_square()   

        # while len(self.bordersRemaining) > 0:
        #     print("LENGTH REMAINING:", len(self.bordersRemaining))
        #     p = self.bordersRemaining.pop(len(self.bordersRemaining) - 1)
        #     ps, newPoints = p.findEndpoint(1)
        #     point, scores = ps

        #     if point in self.searched:
        #         continue
        #     else:
        #         self.bordersRemaining.extend(newPoints)
        #         self.searched[point] = (0, scores)

        #     p1, p2 = endpoints
        #     intersections = self.findIntersections(p1, p2, s1, s2)
        #     self.addToQueue([(p, s) for p, s in intersections if score in s])

        #     print("SIZE REMAINING END", len(self.bordersRemaining))

    def initialize_square(self):
        p1, p2, p3, p4 = Point(self.aB, self.cB), Point(-self.aB, self.cB), Point(-self.aB, -self.cB), Point(self.aB, -self.cB)
        s2 = self.nntm.vertex_oracle(p2[0], self.bVal, p2[1], self.dVal)
        s1 = self.nntm.vertex_oracle(p1[0], self.bVal, p1[1], self.dVal)
        s3 = self.nntm.vertex_oracle(p3[0], self.bVal, p3[1], self.dVal)
        s4 = self.nntm.vertex_oracle(p4[0], self.bVal, p4[1], self.dVal)

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

    def addBoundryPointToQueue(self, points):
        for p, score in points:
            point, endpoints = p 
            if point in self.searched:
                continue
            else:
                # print(score, point)
                self.bordersRemaining.append(tippingPoint(self.nntm, self.bVal, self.dVal, point, score, score))
                self.searched[point] = (endpoints, score)

    def findIntersections(self, p1, p2, s1, s2):
        intersection, endpoints = self.findIntersection(p1, p2, s1, s2)
        intersectionVal = (intersection, endpoints)
        print("INTERSECTION", intersection)
        if intersection == None or intersection == p1 or intersection == p2:
            print("EQUALITY")
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
        
        print("Intersection", intersection, p2)
        return self.findIntersections(intersection, p2, score, s2) + self.findIntersections(p1, intersection, s1, score)


    def findIntersection(self, p1, p2, s1, s2):
        # print ("S1 S2:", s1, s2)
        # print("P1 P2:", p1, p2)

        paramLine = Line(p1, p2)
        
        x1, y1, z1, w1 = s1
        x2, y2, z2, w2 = s2
        
        k1 = self.bVal * y1 + self.dVal * w1
        k2 = self.bVal * y2 + self.dVal * w2

        if ((z2 - z1) == 0 and (x1-x2) == 0):
            return None, None
            # print("SAME x, z SIGNATURE")
        
        print("s1, s2", s1, s2)
        #define line
        if ((z2 - z1) == 0): 
            #VERTICAL LINE
            a = (k2 - k1) / (x1 - x2)
            print(self.aB, k2, k1, x1, x2, a)
            point1 = Point(a, self.cB) #Adds one/minus one to ensure vertical intersection.
            point2 = Point(a, -self.cB)
            line = Line(point1, point2)

            print(point1, point2, paramLine,  line.intersection(paramLine))
            interPoint = line.intersection(paramLine)[0]
            print("INTERPOINT", interPoint)
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