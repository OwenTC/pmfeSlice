
from sympy import Point, Line
# import numpy as np

from pmfeInterface import pmfeInterface


class tippingPoint():
    def __init__(self, interface: pmfeInterface, bVal, dVal, point: Point, score1, score2):
        self.point = point
        self.score1 = score1
        self.score2 = score2
        self.a = point[0]
        self.c = point[1]
        self.b = bVal
        self.d = dVal
        self.delta_x = score1[0] - score2[0]
        self.delta_z = -(score1[2] - score2[2])

        self.aB = 50
        self.cB = 50

        print("X AND Z", self.delta_x, self.delta_z)

        self.nntm = interface

    def findEndpoint(self, step):
        nextPoint = self.iteratePoint(step)
        print("POINT", nextPoint.point)

        newScores = self.nntm.call_subopt(nextPoint.a, nextPoint.b, nextPoint.c, nextPoint.d)
        print("SCORES", newScores)

        while(self.score1 in newScores and self.score2 in newScores):
            print("POINT", nextPoint.point)
            print("SCORES", newScores)
            nextPoint = self.iteratePoint(step)
            newScores = self.nntm.call_subopt(nextPoint.a, nextPoint.b, nextPoint.c, nextPoint.d)
        
        endpoint, scores = self.getEndpoint(self.point, nextPoint.point, self.score1, newScores[0])

        print(scores)
        scores.sort(key = lambda s: (s[0], s[2]))
        newPoints = []
        for i, s in enumerate(scores):
            newPoints.append(tippingPoint(self.nntm, self.b, self.d, endpoint, s, scores[i+1]))

        return (endpoint, scores), newPoints


    def getEndpoint(self, p1, p2, s1, s2):
        intersection, endpoints = self.findIntersection(p1, p2, s1, s2)
        intersectionVal = (intersection, endpoints)
        # print("INTERSECTION", intersection)
        if intersection == None:
            print("INTERSECTION NONE ERROR")
        # if findIntersection(p1, p2, s1, s2) == []:
        #     return []
        scores = self.nntm.vertex_oracle(intersection[0], self.b, intersection[1], self.d)
        # print("SCORES", scores)

        if s1 in scores and s2 in scores: 
            return (intersectionVal, scores)
        
        return self.findIntersections(p1, intersection, scores[0], s2)
    
    def findIntersection(self, p1, p2, s1, s2):
        paramLine = Line(p1, p2)

        # print ("S1 S2:", s1, s2)
        # print("P1 P2:", p1, p2)
        x1, y1, z1, w1 = s1
        x2, y2, z2, w2 = s2
        
        k1 = self.b * y1 + self.d * w1
        k2 = self.b * y2 + self.d * w2

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


    def iteratePoint(self, step):
        return tippingPoint(
            self.nntm,
            self.b,
            self.d,
            Point(self.point[0] + (self.delta_x * step), self.point[1] + (self.delta_z * step)),
            self.score1,
            self.score2
        )