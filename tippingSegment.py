
from fileinput import hook_compressed
from nntplib import NNTPTemporaryError
from typing import List
from sympy import Point, Line, Segment, Line2D
from pmfeInterface import pmfeInterface
from tippingPoint import tippingPoint

cB = 50
aB = 50

class TippingSegment():
    def __init__(self, score_right, score_left, segment: Segment, boundry=False):
        self.segment = segment
        self.score_left = score_left
        self.score_right = score_right
        self.boundry = boundry
        # self.score_middle = score_middle

        # self.aB = 50
        # self.cB = 50

        # self.nntm = interface

        # print(self)

    @classmethod
    def construct_from_point(cls, point: tippingPoint, score_r, score_l, nntm: pmfeInterface, segments = []):
        dx = score_r[0] - score_l[0]
        dz = score_r[2] - score_l[2]
        # print("THIS IS THE POINT", point, point.boundry, "SCORES:", score_r, score_l)

        longSeg = None
        a1 = point.point[0]
        c1 = point.point[1]
        # print((-dz / dx)*(cB-c1) + a1)
        # print("Scores", score_r, score_l)
        vSegments = []
        hSegments = []
        if (dz != 0):
            # vSegments = None #(Segment(point.point, Point(point.point[0], cB)), Segment(point.point, Point(point.point[0], -cB)))
            hSegments = [Segment(point.point, Point(aB, (-dx/dz)*(aB-a1) + c1)),  Segment(point.point, Point(-aB, (-dx/dz)*(-aB-a1) + c1))]
        if (dx != 0):
            vSegments = [Segment(point.point, Point((-dz/dx)*(cB-c1) + a1, cB)), Segment(point.point, Point((-dz/dx)*(-cB-c1) + a1, -cB))]
            # hSegments = None #(Segment(point.point, Point(aB, point.point[1])),  Segment(point.point, Point(-aB, point.point[1])))
        # else: 
        #     vSegments = (Segment(point.point, Point((-dz/dx)*(cB-c1) + a1, cB)), Segment(point.point, Point((-dz/dx)*(-cB-c1) + a1, -cB)))
        #     hSegments = (Segment(point.point, Point(aB, (-dx/dz)*(aB-a1) + c1)),  Segment(point.point, Point(-aB, (-dx/dz)*(-aB-a1) + c1)))
        
        # print("SEGMENTS", hSegments, vSegments)
        # if point.boundry:
        #     # print("SORTEED SEGMENTS", [s for s in sorted(list(hSegments + vSegments), key=lambda t: t.length) if s.length > 0])
        #     longSeg = [s for s in sorted(list(hSegments + vSegments), key=lambda t: t.length) if s.length > 0][-1]
        #     print("LONG SEGMENT", longSeg)
        vert = (hSegments == [])
        hor = (vSegments == [])
        if dx <= 0 and dz <= 0:
            #upper left 
            if vert or ((not hor) and abs(vSegments[0].p2[0]) <= aB and abs(vSegments[0].p2[1]) <= cB): 
                longSeg = vSegments[0]
            else:
                longSeg = hSegments[1]
        elif dx > 0 and dz <= 0:
            #bottom left
            if hSegments == [] or ((not hor) and abs(vSegments[1].p2[0]) <= aB and abs(vSegments[1].p2[1]) <= cB): 
                longSeg = vSegments[1]
            else:
                longSeg = hSegments[1]
        elif dx <= 0 and dz > 0:
            #uper right
            if hSegments == [] or ((not hor) and abs(vSegments[0].p2[0]) <= aB and abs(vSegments[0].p2[1]) <= cB): 
                longSeg = vSegments[0]
            else:
                longSeg = hSegments[0]
        elif dx > 0 and dz > 0:
            #bottom right
            if hSegments == [] or ((not hor) and abs(vSegments[1].p2[0]) <= aB and abs(vSegments[1].p2[1]) <= cB): 
                longSeg = vSegments[1]
            else:
                longSeg = hSegments[0]

        # print("LONG SEGMENT", longSeg)
        for s in segments:
            if longSeg.contains(s.segment) and (s.segment.p1 == point.point or s.segment.p2 == point.point):
                print("Already Computed")
                endpoint = s.segment.p1
                if endpoint == point:
                    endpoint = s.segment.p2
                return s, tippingPoint(endpoint, score_l, score_r)

        # print(score_r, score_l, longSeg)
        
        # print("TRANSFORMED", nntm.transform, longSeg.p2)
        longSegScore = nntm.vertex_oracle(longSeg.p2[0], 0, longSeg.p2[1], 1)
        # print("LONG SEG", longSeg, longSegScore)
        endpoint = cls.find_segment_endpoint(point.point, score_l, longSeg.p2, longSegScore, None, score_r, 0, 1, nntm)
        s = TippingSegment(score_r, score_l, Segment(point.point, endpoint))
        return s, tippingPoint(endpoint, score_l, score_r)

    @classmethod
    def find_segment_endpoint(cls, vertex, sv, point, sp, prevPt, altsv, bVal: int, dVal: int, nntm: pmfeInterface):

        intersection, _ = cls.findIntersection(vertex, point, sv, sp)
        
        if type(intersection) == Line2D:
            intersection, _ = cls.findIntersection(vertex, point, altsv, sp)

        # print("FINDING SEGMENT FROM RAY:", intersection, point, sv, altsv)
        if intersection == None or intersection == point or type(intersection) == Line2D:
            # print("BASE CASE")
            # print("EQUALITY")
            return point

        interScore = nntm.vertex_oracle(intersection[0], bVal, intersection[1], dVal)
        return cls.find_segment_endpoint(vertex, sv, intersection, interScore, point, altsv, bVal, dVal, nntm)

        # print("SCORE", score)

        # if s1 == score:
        #     # print("S1 MATCH")
        #     return self.findIntersections(intersection, p2, score, s2) + [(intersectionVal, score)]
        
        # if s2 == score: 
        #     # print("S2 MATCH")
        #     return self.findIntersections(p1, intersection, s1, score) + [(intersectionVal, score)]
        
        # # print("Intersection", intersection, p2)
        # score = nntm.vertex_oracle(inter[0], b_val, inter[1], d_val)
    
    @classmethod
    def findIntersection(cls, p1, p2, s1, s2):
        bVal = 0
        dVal = 1
        aB = 50
        cB = 50
        # print ("S1 S2:", s1, s2)
        # print("P1 P2:", p1, p2)

        paramLine = Line(p1, p2)
        
        x1, y1, z1, w1 = s1
        x2, y2, z2, w2 = s2
        
        k1 = bVal * y1 + dVal * w1
        k2 = bVal * y2 + dVal * w2

        if ((z2 - z1) == 0 and (x1-x2) == 0):
            return None, None
            # print("SAME x, z SIGNATURE")
        
        # print("s1, s2", s1, s2)
        #define line
        if ((z2 - z1) == 0): 
            #VERTICAL LINE
            a = (k2 - k1) / (x1 - x2)
            # print(self.aB, k2, k1, x1, x2, a)
            point1 = Point(a, cB)
            point2 = Point(a, -cB)
            line = Line(point1, point2)

            # print(point1, point2, paramLine,  line.intersection(paramLine))
            interPoint = line.intersection(paramLine)[0]
            # print("INTERPOINT", interPoint)
            return interPoint, (point1, point2)

        else:
            x = (x1 - x2)
            const = (k1 - k2)
            point1 = Point(aB, (aB * x + const) / (z2 - z1))
            point2 = Point(-aB, (-aB * x + const) / (z2 - z1))
            
            # print("Po1 Po2:", point1, point2)
            # print("PARAM LINE", paramLine)
            interPoint = Line(point1, point2).intersection(paramLine)[0]
            # print("INTERPOINT", interPoint) 

            return interPoint, (point1, point2)


    # # def iteratePoint(self, step):
    # #     return tippingPoint(
    # #         self.nntm,
    # #         self.b,
    # #         self.d,
    # #         Point(self.point[0] + (self.delta_x * step), self.point[1] + (self.delta_z * step)),
    # #         self.score1,
    # #         self.score2
    # #     )

    def __repr__(self) -> str:
        return f"TippingSegment({self.segment}, {self.score_left}, {self.score_right})"

    def __eq__(self, __o: object) -> bool:
        if type is not TippingSegment:
            return False
        return self.segment == __o.segment