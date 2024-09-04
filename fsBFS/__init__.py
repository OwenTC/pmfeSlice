# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from collections import defaultdict
from sympy import Point, Segment2D, convex_hull, Segment, Rational, Polygon
# from tippingSegment import TippingSegment
from random import randint

from pmfeInterface import pmfeInterface

class fsBFS():
    def __init__(self, pmfe, rna_file, transform = True, bVal : Rational = 0, aB : Rational = 50, cB : Rational = 50, ab : Rational = -50, cb : Rational = -50):
        self.bVal = bVal
        self.dVal = 1
        self.ab = ab
        self.cb = cb
        self.aB = aB
        self.cB = cB

        self.nntm = pmfeInterface(pmfe, rna_file, transform=transform)

        self.pointQueue = []
        self.tippingSegments = {}
        self.visited = set()
        self.point_TLs = {}
        self.signatures = defaultdict(set)

        self.pointQueueHull = None

    from ._tippingSegment import construct_segment_from_point, find_tipping_line_intersection, find_segment_endpoint, shorten_segment, find_segment_direction, distance_to_intersection, shorten_segment_2
    from ._saveData import save_data
    
    def build(self):
        # Initialize
        # return starting queue with boundry
        self.initialize_square()   

        # print(self.pointQueue)
        # print(self.tippingSegments)
        while len(self.pointQueue) > 0:
            # print("VERTICES REMAINING:", len(self.pointQueue))
            # point = self.pointQueue.pop(0)
            self.pointQueueHull = convex_hull(*self.pointQueue, polygon=True)
            points = self.vertices_from_geometry(self.pointQueueHull)
            point = points[len(points)//2]
            self.pointQueue.remove(point)

            adjacent_points = self.get_adjacent(point)
            
            for p in adjacent_points:
                if p not in self.visited:
                    self.visited.add(p)
                    self.pointQueue.append(p)

        print("PMFE CALLS:", self.nntm.pmfeCalls, "SUBOPT CALLS:", self.nntm.suboptCalls)

    def initialize_square(self):
        #Possible Issue:
        # Doesn't add corner points to queue (so if they have more than one optimal structure it will be unknown.)

        #Initialize points and scores
        p1, p2, p3, p4 = Point(self.aB, self.cB), Point(self.ab, self.cB), Point(self.ab, self.cb), Point(self.aB, self.cb)
        s1_sigs = self.nntm.subopt_oracle(p1[0], self.bVal, p1[1], self.dVal)
        s2_sigs = self.nntm.subopt_oracle(p2[0], self.bVal, p2[1], self.dVal)
        s3_sigs = self.nntm.subopt_oracle(p3[0], self.bVal, p3[1], self.dVal)
        s4_sigs = self.nntm.subopt_oracle(p4[0], self.bVal, p4[1], self.dVal)

        s1 = self.nntm.vertex_oracle(p1[0], self.bVal, p1[1], self.dVal)
        s2 = self.nntm.vertex_oracle(p2[0], self.bVal, p2[1], self.dVal)
        s3 = self.nntm.vertex_oracle(p3[0], self.bVal, p3[1], self.dVal)
        s4 = self.nntm.vertex_oracle(p4[0], self.bVal, p4[1], self.dVal)

        #Set p1, p2, p3, p4 to visited
        self.visited.add(p1)
        self.visited.add(p2)
        self.visited.add(p3)
        self.visited.add(p4)

        #Update signature dictionary
        self.update_saved_signatures(s1_sigs, p1)
        self.update_saved_signatures(s2_sigs, p2)
        self.update_saved_signatures(s3_sigs, p3)
        self.update_saved_signatures(s4_sigs, p4)

        #Create queue of points on the frame
        self.add_frame_point_to_queue(self.find_collinear_tipping_points(p1, p2, s1, s2))
        self.add_frame_point_to_queue(self.find_collinear_tipping_points(p2, p3, s2, s3))
        self.add_frame_point_to_queue(self.find_collinear_tipping_points(p3, p4, s3, s4))
        self.add_frame_point_to_queue(self.find_collinear_tipping_points(p4, p1, s4, s1))

    def add_frame_point_to_queue(self, points):
        for i, (point,_) in enumerate(points):
            #Remove duplicates found from find_colinear_tipping_points
            if point == points[(i+1)%len(points)][0]:
                continue
            # if i+1 < len(points):
            #     self.tippingSegments.add(Segment(point, points[i+1][0]))
            # if point in self.visited:
            #     continue

            # print(score, point)
            self.update_ray_scores(point)
            self.pointQueue.append(point)
            self.visited.add(point)


    def find_collinear_tipping_points(self, p1, p2, s1, s2):
        # Remove intersectionVal information!!!
        intersection, _ = self.find_tipping_line_intersection(p1, p2, s1, s2)

        if intersection == None:
            return []
        if intersection == p1:
            return [(intersection, s1)]
        if intersection == p2:
            return [(intersection, s2)]

        score = self.nntm.vertex_oracle(intersection[0], self.bVal, intersection[1], self.dVal)

        if s1 == score:
            return self.find_collinear_tipping_points(intersection, p2, score, s2) + [(intersection, score)]
        
        if s2 == score: 
            return self.find_collinear_tipping_points(p1, intersection, s1, score) + [(intersection, score)]
        
        return self.find_collinear_tipping_points(intersection, p2, score, s2) + self.find_collinear_tipping_points(p1, intersection, s1, score)

    def get_adjacent(self, p):
        # subopt = self.nntm.subopt_oracle(p[0], self.bVal, p[1], self.dVal)
        # self.update_saved_signatures(subopt, p)

        # sigs = self.sort_signatures([*set(subopt)])

        # if len(sigs) < 2:
        #     print("Only one unique a, c signature from subopt", sigs)
        #     return [], []
        # if len(sigs) == 2:
        #     #THIS MIGHT BE UNESSASARY, need to check the output of convex_hull
        #     #If there are only 2 signatures we want the left signature at index 0 and right at index 1. [sig_l, sig_r]
        #     if p[0] == self.aB:
        #         sigs.sort(key=lambda t: t[2], reverse=True)
        #     elif p[0] == self.ab:
        #         sigs.sort(key=lambda t: t[2])
        #     elif p[1] == self.cB:
        #         sigs.sort(key=lambda t: t[0])
        #     elif p[1] == self.cb:
        #         sigs.sort(key=lambda t: t[0], reverse=True)
        #     else:
        #         print(f"ERROR: NON-BOUNDRY POINT ({p}) WITH {len(sigs)} SIGNATURES")

        potential_segments = self.point_TLs[p]
        adjPoints = []
        for s1, s2 in potential_segments:
            _, end_point = self.construct_segment_from_point(p, s1, s2)
            
            if end_point not in self.visited:
                self.update_ray_scores(end_point)
            
            adjPoints.append(end_point)

        return adjPoints

    def OBframeSignature(self, p, score_r, score_l):
        if (p[0] not in [self.ab, self.aB]) and (p[1] not in [self.cb, self.cB]):
            return False
        
        dx = score_r[0] - score_l[0]
        dz = score_r[2] - score_l[2]
        if p[1] == self.cB and dx <= 0:
            #North
            return True
        if p[1] == self.cb and dx > 0:
            #South
            return True
        if p[0] == self.aB and dz > 0:
            #East
            return True
        if p[0] == self.ab and dz <= 0:
            #West
            return True
        
        return False

    def sort_signatures(self, sigs):
        sigs2D = [Point(sig[0], sig[2]) for sig in sigs]
        pointDict = dict(zip(sigs2D,sigs))
        hull = convex_hull(*sigs2D)

        if type(hull) is Segment2D:
            return [pointDict[hull.p1], pointDict[hull.p2]]

        return([pointDict[v] for v in hull.vertices])
    
    #Add the 
    def update_ray_scores(self, p):
        subopt = self.nntm.subopt_oracle(p[0], self.bVal, p[1], self.dVal)
        self.update_saved_signatures(subopt, p)
        sorted_sigs = self.sort_signatures([*set(subopt)])
        # self.point_TLs[p] = sorted_sigs
        if len(sorted_sigs) < 2:
            print("ERROR: Only one unique a, c signature from subopt", sorted_sigs)
            exit()
        if len(sorted_sigs) == 2:
            #If there are only 2 signatures we want the left signature at index 0 and right at index 1. [sig_l, sig_r]
            if p[0] == self.aB:
                sorted_sigs.sort(key=lambda t: t[2], reverse=True)
            elif p[0] == self.ab:
                sorted_sigs.sort(key=lambda t: t[2])
            elif p[1] == self.cB:
                sorted_sigs.sort(key=lambda t: t[0])
            elif p[1] == self.cb:
                sorted_sigs.sort(key=lambda t: t[0], reverse=True)
            else:
                print(f"ERROR: NON-BOUNDRY POINT ({p}) WITH {len(sorted_sigs)} SIGNATURES")

        for i in range(-1, len(sorted_sigs) - 1):
            sig_pair = (sorted_sigs[i], sorted_sigs[i + 1])
            if self.OBframeSignature(p, *sig_pair):
                continue
            try:
                self.point_TLs[p].append(sig_pair)
            except KeyError:
                self.point_TLs[p] = [sig_pair]

            sig_set = frozenset(s[::2] for s in sig_pair)
            try:
                if len(self.tippingSegments[sig_set]) == 1:
                    self.tippingSegments[sig_set] += (p,)
                elif len(self.tippingSegments[sig_set]) == 2:
                    print(f"More than 2 TPs {self.tippingSegments[sig_pair]} for a TL: {sig_pair} ")
                    exit()
            except KeyError:
                self.tippingSegments[sig_set] = (p,)

            if len(sorted_sigs) == 2:
                break

    def update_saved_signatures(self, sigs, p):
        for s in sigs:
            self.signatures[s].add(p)

    #Gets vertices from point2d, segment2D, and polygon
    def vertices_from_geometry(self, geom):
        if issubclass(type(geom),Point):
            return [geom]
        if issubclass(type(geom),Segment):
            return [geom.p1, geom.p2]
        if issubclass(type(geom),Polygon):
            return geom.vertices
        raise TypeError(f"Geometry {geom} is not a Polygon, Segment, or Point.")