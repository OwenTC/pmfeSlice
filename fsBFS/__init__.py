# TO DO
# MOVE ROUNDING SO THAT IT IS ALL IN ONE PLACE
#FIX FRAME CORNER ISSUE CHECKING IF IT IS A TIPPING VERTEX

# BUG
# Segment added to segments multiple times... (this is a set how is this even possible????)
#   While computing Aquifex.aeolicus.VF5_AE000657 with pmfe using vienna code

# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from collections import defaultdict
from sympy import Point, Segment2D, convex_hull, Segment, Rational, Polygon, Line, Symbol, floor, ceiling, zoo

# from tippingSegment import TippingSegment
# from random import randint
import networkx as nx

from pmfeInterface import pmfeInterface
from viennaInterface import ViennaInterface
from tippingPoint import TippingPoint as TP
from tippingPoint import GridSegment as GS

class fsBFS():
    def __init__(self, pmfe, rna_file, transform = True, bVal : Rational = 0, aB : Rational = 50, cB : Rational = 50, ab : Rational = -50, cb : Rational = -50):
        self.bVal = bVal
        self.dVal = 1
        self.ab = ab
        self.cb = cb
        self.aB = aB
        self.cB = cB

        self.nntm = ViennaInterface(pmfe, rna_file, transform=transform)
        # self.nntm = ViennaInterface(pmfe, rna_file, transform=transform)

        self.pointQueue = {} #tp.center_point():tp
        self.visited = {} #tp.center_point():tp
        self.segments = {} #set(score, score): [tp, tp]

        self.pointQueueHull = None

    from ._tippingSegment import construct_segment_from_point, find_tipping_line_intersection, find_segment_endpoint, shorten_segment, find_segment_direction, distance_to_intersection, shorten_segment_2, find_ray_hull_intersection, find_tipping_line
    from ._saveData import save_data, save_signatures, save_segments
    
    def build(self):
        # Initialize
        # return starting queue with boundry
        self.initialize_square() 
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print("INITIALIZED")
        print(self.pointQueue, self.visited)

        # print(self.tipGraph.edges(data=True))

        # print(self.pointQueue)
        # print(self.tippingSegments)
        while len(self.pointQueue) > 0:
            # print("POINT QUEUE", [(p[0],p[1]) for p in self.pointQueueHull])
            # print("VERTICES REMAINING:", len(self.pointQueue))
            # point = self.pointQueue.pop(0)
            # tipGraph["queueHull"] = convex_hull(*self.pointQueue.keys(), polygon=True)
            self.pointQueueHull = convex_hull(*self.pointQueue.keys(), polygon=True)
            points = self.vertices_from_geometry(self.pointQueueHull)
            point = self.pointQueue.pop(points[len(points)//2])

            # print("DEQUEUING POINT", (point.center()))
            # print("HULL BEFORE DEQUEUE", [tuple(p) for p in points])
            # print("QUEUE AFTER DEQUQUE", [tuple(p) for p in self.pointQueue])
            # print("VISITED AFTER DEQUQUE", [tuple(p) for p in self.visited])
            # print(f"SEGMENTS: {[(tuple(i), tuple(p for p in j)) for i, j in self.segments.items()]}")

            adjacent_points = self.get_adjacent(point)
            
            # print("ADJACENT POINTS", adjacent_points)
            for p in adjacent_points:
                p_center = p.center()
                if p_center not in self.visited.keys():
                    self.visited[p_center] = p
                    self.pointQueue[p_center] = p

        # print("VISITED AFTER DEQUQUE", [tuple(p) for p in self.visited])
        print("PMFE CALLS:", self.nntm.pmfeCalls, "SUBOPT CALLS:", self.nntm.suboptCalls)

    def initialize_square(self):
        #Possible Issue:
        # Doesn't add corner points to graph (so if they have more than one optimal structure it will be unknown.)

        #Initialize points and scores
        corners = [(self.aB, self.cB), (self.ab, self.cB), (self.ab, self.cb), (self.aB, self.cb)]
        frame_points = []
        for i, p in enumerate(corners):
            frame_points.append(TP.tp_from_grid_point(p, ((i+2)%4)+1, corner_point=True))
            # self.visited.add(p)
        
        # self.tipGraph.add_nodes_from((t.center(), {"tipping_point":t}) for t in frame_points)

        score_corners = []
        for i, p in enumerate(frame_points):
            corner_point = p.defining_points[(i+2)%4]
            score = self.nntm.vertex_oracle(corner_point.a, self.bVal, corner_point.c, self.dVal)
            p.add_scores([score],start=1)
            score_corners.append(score)
        
        # colinear_tps = []
        for i in range(4):
            print(f"FRAME{i}")
            p1 = corners[i]
            p2 = corners[(i+1)%4]
            grid_segments = self.find_collinear_grid_segments(p1, p2, score_corners[i], score_corners[(i+1)%4])

            #Create tipping points from gridsegments p1's
            tipping_points = [TP.tp_from_grid_point(g.p1, ((i+3)%4)+1, frame_point=(i+1)) for g in grid_segments]            

            for j,t in enumerate(tipping_points):
                if j < (len(tipping_points)-1):
                    t.add_adjacency(tipping_points[j+1], (i+1)%4, (i-1)%4)
                    
                self.find_tp_scores(t)
                if t.scores[(i+2)%4] == t.scores[(i+3)%4]:
                    raise Exception(f"SCORES ARE THE SAME: { t.scores[(i+2)%4], t.scores[(i+3)%4]}")

                self.segments[frozenset((t.scores[(i+2)%4],t.scores[(i+3)%4]))] = [t]
                self.pointQueue[t.center()] = t
                self.visited[t.center()] = t

            


        # print([((p[0][0]+p[1][0])/2, (p[0][1]+p[0][1])/2) for p in colinear_points])

    """
    params: Points p1, p2 with scores s1, s2
    return: All tipping points beteween p1 and p2
    restrictions: p1 and p2 must be collinear on a horizontal or vertical line
    """
    def find_collinear_grid_segments(self, p1, p2, s1, s2):
        # print(p1, p2, s1, s2)
        # Remove intersectionVal information!!!
        intersection, _ = self.find_tipping_line_intersection(p1, p2, s1, s2)
        # print(intersection)

        if intersection == None:
            return []
        
        grid_seg = GS.gs_from_inter_point(intersection, p1, p2)
        grid_seg.s1 = self.nntm.vertex_oracle(grid_seg.p1[0], self.bVal, grid_seg.p1[1], self.dVal)
        grid_seg.s2 = self.nntm.vertex_oracle(grid_seg.p2[0], self.bVal, grid_seg.p2[1], self.dVal)

        int_intersection = (grid_seg.p1 == tuple(intersection)) or (grid_seg.p2 == tuple(intersection))
        if int_intersection and (grid_seg.s1 == grid_seg.s2): 
            new_grid_seg = GS.alt_gs_from_grid_point(intersection, p1, p2)

            if new_grid_seg.p1 in (grid_seg.endpoints()):
                new_grid_seg.s1 = grid_seg.s1
                new_grid_seg.s2 = self.nntm.vertex_oracle(new_grid_seg.p2[0], self.bVal, new_grid_seg.p2[1], self.dVal)
            else:
                new_grid_seg.s2 = grid_seg.s2
                new_grid_seg.s1 = self.nntm.vertex_oracle(new_grid_seg.p1[0], self.bVal, new_grid_seg.p1[1], self.dVal)
            
            grid_seg = new_grid_seg

        grid_segments = []
        if grid_seg.s1 != grid_seg.s2:
            grid_segments.append(grid_seg)
        
        grid_segments.extend(self.find_collinear_grid_segments(p1, grid_seg.p1, s1, grid_seg.s1))
        grid_segments.extend(self.find_collinear_grid_segments(grid_seg.p2, p2, grid_seg.s2, s2))

        return grid_segments
        
        # return self.find_collinear_grid_segments(intersection, p2, score, s2) + self.find_collinear_grid_segments(p1, intersection, s1, score)
    
    def find_collinear_tipping_points(self, p1, p2, s1, s2):
        grid_segs = self.find_collinear_grid_segments(p1, p2, s1, s2)
        return [(g.p1, g.p2) for g in grid_segs]


    # def find_cyclically_ordered_signatures(self, p, eng):
    #     subopt = self.nntm.subopt_oracle(p[0], self.bVal, p[1], self.dVal, eng=eng)
    #     self.update_saved_signatures(subopt, p)
    #     print("SUBOPT", subopt, tuple(p))

    #     subopt_no_duplicates = {}
    #     for s in subopt[::-1]:
    #         subopt_no_duplicates[(s[0],s[2])] = s
    #     print("SUBOPT", subopt_no_duplicates, tuple(p))
    #     return self.sort_signatures([*subopt_no_duplicates.values()])

    def find_tp_scores(self, tp):
        # print(tp.scores)
        for i, s in enumerate(tp.scores):
            if s == None:
                p = tp.defining_points[i]
                tp.scores[i] = self.nntm.vertex_oracle(p.a, self.bVal, p.c, self.dVal)

    def get_search_range(self, p1, p2, s1, s2, slope, eq_a, eq_c, loc):
                
        # end_switch = {(0,True): min(self.cB, eq_a(self.aB), key=lambda c: (abs(p1.c - c))), (0,False): min(self.cB, eq_a(self.ab)), (1, True): min(self.cb, eq_a(self.ab)), (1, False): min(self.cB, eq_a(self.aB)), (2, True): min(self.cB, eq_a(self.aB)), (2, False): min(self.cB, eq_a(self.aB)), (3,True): min(self.cB, eq_a(self.aB)), (3, False): min(self.cB, eq_a(self.aB))}
        if (p1.a == p2.a):
            point = (p1.a, eq_a(p1.a))
        elif (p1.c == p2.c):
            point = (eq_c(p1.c), p1.c)

        ray = self.find_segment_direction(point, s1, s2)
        # print(ray)
        inter_points = ray.intersection(Polygon((self.aB+1, self.cB+1),(self.ab-1, self.cB+1),(self.ab-1, self.cb-1),(self.aB+1, self.cb-1)))
        endpoint = inter_points[0] if inter_points[0] != Point(point) else inter_points[1]

        if (slope == zoo) or abs(slope) > 1:
            # print(f"POSITIVE SLOPE, {slope}")
            c_endpoint = int(endpoint[1]) #Last segment it intersects
            if loc%2 == 1: #East or west edges
                if slope > 0:
                    loc_start_switch = {1: floor(point[1]), 3:ceiling(point[1])}
                else:
                    loc_start_switch = {1: ceiling(point[1]), 3:floor(point[1])}

                start_point = loc_start_switch[loc]
            else:
                start_point = point[1]

            return (range(c_endpoint, start_point+1), eq_c) if c_endpoint <= start_point else (range(c_endpoint, start_point-1, -1), eq_c)
        else:
            # print(f"NEGATIVE SLOPE, {slope}")
            a_endpoint = int(endpoint[0]) #Last segment it intersects
            if loc%2 == 0:  #North or south edges
                if slope > 0:
                    loc_start_switch = {0: ceiling(point[0]), 2:floor(point[0])}
                else:
                    loc_start_switch = {0: floor(point[0]), 2:ceiling(point[0])}

                start_point = loc_start_switch[loc]
            else:
                start_point = point[0]
            
            return (range(a_endpoint, start_point+1), eq_a) if a_endpoint <= start_point else (range(a_endpoint, start_point-1, -1), eq_a)

    def find_adjacent_from_scores(self, tp: TP, loc):
        #loc denotes location north, west, east, south
        if tp.adjacentPoints[loc] != None:
            return tp.adjacentPoints[loc]
        
        s1, s2 = tp.scores[loc],tp.scores[(loc+1)%4]
        if frozenset((s1,s2)) in self.segments.keys():
            # DEBUGING
            if len(self.segments[frozenset((s1,s2))]) > 1 and tp not in self.segments[frozenset((s1,s2))]:
                raise Exception(f"Segment with more than 2 tps: {self.segments[frozenset((s1,s2))], tp, s1, s2}")
            #DEBUGING
            
            if (len(self.segments[frozenset((s1,s2))]) > 1):
                try: 
                    index = (self.segments[frozenset((s1,s2))].index(tp) + 1) % 2
                except ValueError:
                    index = 0  
                return self.segments[frozenset((s1,s2))][index]
            elif tp not in self.segments[frozenset((s1,s2))]:  
                return self.segments[frozenset((s1,s2))][0]
            
        p1, p2 = tp.defining_points[loc],tp.defining_points[(loc+1)%4]

        # print("SCORES", s1, s2)
        # print("POINTS", tp, loc, tp.adjacentPoints)

        tl_a, tl_c, slope = self.find_tipping_line(s1, s2)
        
        # direction_switch = {0:range(self.cB,p1.c+1,-1), 1:range(self.ab,p1.a+1), 2:range(self.cb,p1.c+1), 3:range(self.aB,p1.a+1,-1)}
        # if abs(slope) > 1:
        #     # positive = True if slope > 0 else False
        #     if loc in (1,3):
        #         if slope > 0:
        #             direction_switch = {1:range(self.ab,p1.a+1), 3:range(self.aB,p1.a+1,-1)}
        #         else:
        #             dir_range = range()
        #     else:


        #     direction_switch = {(0,):range(self.cB,p1.c+1,-1), 1:range(self.ab,p1.a+1), 2:range(self.cb,p1.c+1), 3:range(self.aB,p1.a+1,-1)}
        # else:
        #     direction_switch = {0:range(self.cB,p1.c+1,-1), 1:range(self.ab,p1.a+1), 2:range(self.cb,p1.c+1), 3:range(self.aB,p1.a+1,-1)}
        
        potential_endpoints = []

        search_range, eq = self.get_search_range(p1, p2, s1, s2, slope, tl_a, tl_c, loc)
        # print("RANGE", search_range, loc)
        # print("POINT", tp, tp.scores)
        # eq = tl_a if (loc % 2) else tl_c
        segment_type = "v" if (slope == zoo or abs(slope) > 1) else "h"
        for n in search_range:
            potential_endpoints.append((n, eq(n)) if segment_type == "h" else (eq(n), n))

        print(search_range, potential_endpoints[0],potential_endpoints[-1], sep=",")

        if loc < 2:
            s1, s2 = s2, s1

        endpoint = self.find_segment_endpoint(potential_endpoints, s1, s2, tp, segment_type)
        # print("SCORES", s2, s1)
        # adj_edge = min() = [Line(*(tuple(p) for p in end_point.defining_points)]

        endpoint.add_scores((self.nntm.vertex_oracle(p.a, self.bVal, p.c, self.dVal) for p in endpoint.defining_points))
        # print("ENDPOINT", endpoint, endpoint.center(), endpoint.scores)

        adjacency_added = False
        for i, s in enumerate(endpoint.scores):
            print((s, endpoint.scores[(i+1)%4]))
            temp_scores = (s, endpoint.scores[(i+1)%4])
            if temp_scores == (s1, s2) or temp_scores == (s2, s1):
                #Check if we are passed the frame:
                for j in (i, (i+1)%4):
                    p = endpoint.defining_points[j]
                    if p.a > self.aB or p.a < self.ab or p.c > self.cB or p.c > self.cB:
                        break
                else:
                    tp.add_adjacency(endpoint, loc, i)
                    adjacency_added = True
                # print("ADDING ADJACENCY")
            set_scores = frozenset(temp_scores)
            if len(set_scores) >= 2:
                try:
                    self.segments[set_scores].append(endpoint)
                except KeyError:
                    self.segments[set_scores] = [endpoint]
        
        if not adjacency_added:
            print(f"No adjacency added")
            print(str(tp).replace(";",","), str(endpoint).replace(";",","), endpoint.scores)
            quit()
        
        return endpoint
    
    # def floor_ceil_point(point, f_point, c_point, vert):
    #     if vert not in [0, 1]:
    #         raise ValueError(f"vert must be 0 or 1 not {vert}")
        
    #     floor_point, ceil_point = floor(point), ceiling(point)
    #     index = 0 + vert #vert is 

    def get_ceil_floor_pts(self, p, segment_type):
        p_f = (floor(p[0]), floor(p[1]))
        p_c = (ceiling(p[0]), ceiling(p[1]))
        if p_f == p_c:
            if segment_type == "h":
                return ((p_f[0], p_f[1]-1), p_f, (p_f[0], p_f[1]+1))
            elif segment_type == "v":
                return ((p_f[0]-1, p_f[1]), p_f, (p_f[0]+1, p_f[1]))
            else: 
                raise ValueError(f"Segment type should be v or h not: {segment_type}")
        
        return (p_f, p_c)

    def get_potential_tp(self, p_far, p_close, segment_type):
        #THIS HAS BUGS FOR SLOPE == 1 
        close_points = self.get_ceil_floor_pts(p_close, segment_type)
        far_points = self.get_ceil_floor_pts(p_far, segment_type)

        a_vals = sorted(list(set(p[0] for p in close_points+far_points)), reverse=True)
        c_vals = sorted(list(set(p[1] for p in close_points+far_points)), reverse=True)

        # if len(a_vals) > 3 or len(c_vals) > 3:
        #     raise ValueError(f"Too many a, c values {a_vals}; {c_vals}.")
        
        print("LENGHTS", a_vals, c_vals, len(a_vals), len(c_vals), close_points, far_points)
        if len(a_vals) >= 3:
            return tuple(TP((a_vals[i],c_vals[0]),(a_vals[i+1],c_vals[0]),(a_vals[i+1],c_vals[1]),(a_vals[i],c_vals[1])) for i in range(len(a_vals)-1))
        if len(c_vals) >= 3:
            return tuple(TP((a_vals[0],c_vals[i]),(a_vals[1],c_vals[i]),(a_vals[1],c_vals[i+1]),(a_vals[0],c_vals[i+1])) for i in range(len(c_vals)-1))

    def find_segment_endpoint(self, potential_endpoints, score_f, score_c, base_point, segment_type):
        start = 0
        end = len(potential_endpoints)-1
        #Finding tipping point with score matching lower score (score_f)

        score_p = lambda p: self.nntm.vertex_oracle(p[0], self.bVal, p[1], self.dVal)

        while start < (end-1):
            mid = (start + end) // 2
            
            mid_p_f = (floor(potential_endpoints[mid][0]), floor(potential_endpoints[mid][1]))
            mid_p_c = (ceiling(potential_endpoints[mid][0]), ceiling(potential_endpoints[mid][1]))
            
            if mid_p_f == mid_p_c:
                # print("EQUALITY CASE")
                if segment_type == "h":
                    points = [(mid_p_f[0], mid_p_f[1]-1), (mid_p_f[0], mid_p_f[1]+1)]
                elif segment_type == "v":
                    points = [(mid_p_f[0]-1, mid_p_f[1]), (mid_p_f[0]+1, mid_p_f[1])]
                
                # print(points, mid_p_f, score_p(points[0]), score_p(points[1]), score_p(mid_p_f), score_f, score_c)
                # print(start, mid, end)
                if (score_p(points[0]) == score_f and score_p(mid_p_f) == score_c) or ((score_p(points[1]) == score_c and score_p(mid_p_f) == score_f)):
                    end = mid
                else:
                    start = mid

                # print(start, mid, end, (start < (end-1)))
            else:
                if (score_p(mid_p_f) == score_f and score_p(mid_p_c) == score_c):
                    end = mid
                else:
                    start = mid
                
                # print("2",start, mid, end, (start < (end-1)))
        
        p1 = potential_endpoints[start]
        p2 = potential_endpoints[end]
        mid_p = ((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)
        
        index = 1 if segment_type == "h" else 0
        if (floor(p1[index]) != floor(p2[index])) or (ceiling(p1[index]) != ceiling(p2[index])):
            # print("POINT", p1, p2)
            index = 1 if segment_type == "h" else 0
            potential_tps = self.get_potential_tp(p1, p2, segment_type)
            # print(f"POTENTIAL TPS:{potential_tps}")
            for tp in potential_tps:
                self.find_tp_scores(tp)
                if (score_f in tp.scores and score_c in tp.scores) and len(set(tp.scores)) >= 3:
                    return tp
            
        #     if f_point == c_point:
        #         score_at_point = score_p(f_point)
        #         if score_at_point == score_f:
        #             new_point = (c_point[0], c_point[1]+1) if segment_type == "h" else (c_point[0]+1, c_point[1])
        #             points = (f_point, new_point)
        #         elif score_at_point == score_c:
        #             new_point = (c_point[0], c_point[1]-1) if segment_type == "h" else (c_point[0]-1, c_point[1])
        #             points = (new_point, f_point)
        #         else:
        #             raise Exception(f"No score matches s1, s2: {score_at_point, score_c, score_f}")
        #     else:
        #         points = (f_point, c_point)
            
        #     print("POINTS AFTER POINT", points, f_point, c_point)
        #     if p1[(index+1)%2] < p2[(index+1)%2]:
        #         #q1 is always ceiling for neg to pos segments
        #         return TP.tp_from_grid_point(points[1], 1)
        #     else:
        #         #q3 is always floot for pos to neg segments
        #         return TP.tp_from_grid_point(points[0], 3)
            
        try:
            return TP.tp_from_float_point(mid_p)
        except ValueError:
            if p1[0] == p2[0]:
                segment_dir = "v"
            elif p1[1] == p2[1]:
                segment_dir = "h"
            else:
                raise ValueError(f"Points not vertical or horizontal: {p1, p2}")
            
            check_vals_switch = {"v":[d.a for d in base_point.defining_points], "h":[d.c for d in base_point.defining_points]}
            test_vals_switch = {"v":(int(p2[0]+1), int(p2[0]-1)), "h":(int(p2[1]+1), int(p2[1]-1))}

            # print(list(check_vals_switch[segment_dir]), test_vals_switch[segment_dir], test_vals_switch[segment_dir][0] in check_vals_switch[segment_dir], [type(x) for x in list(check_vals_switch[segment_dir])])

            if test_vals_switch[segment_dir][0] in check_vals_switch[segment_dir]:
                #Positive side of outgoing segment
                val = .5
            elif test_vals_switch[segment_dir][1] in check_vals_switch[segment_dir]:
                val = -.5

            if segment_dir == "v":
                new_mid_p = (mid_p[0] + val, mid_p[1])
            if segment_dir == "h":
                new_mid_p = (mid_p[0], mid_p[1] + val)
            
            # print("VALUERROR", segment_dir, mid_p, new_mid_p)
            return TP.tp_from_float_point(new_mid_p)


            # for p in points_switch[segment_dir]:
            #     score = self.nntm.vertex_oracle(p[0], self.bVal, p[1], self.bVal)

            #     if score != p2_score:
            #         return TP.tp_from_grid_point()
                

            # tps = TP.tps_from_segment(potential_endpoints[index],potential_endpoints[index+1])
            # for point in tps:
            #     gp = point.defining_points[]
            #     point.scores[] = self.nntm.vertex_oracle(gp.a, self.bVal, gp.c, self.bVal)
            #     if point.scores

        # endpoints.append(TP.tp_from_float_point(mid_p))
        # print("POINT", potential_endpoints[index])
        # # end = len(potential_endpoints)-1
        # # #Check with upper score to see if there is a closer tipping point
        # start = index
        # end = len(potential_endpoints)-1
        # while start < end:
        #     mid = (start + end) // 2
        #     mid_p = (ceiling(potential_endpoints[mid][0]), ceiling(potential_endpoints[mid][1]))
        #     mid_score = self.nntm.vertex_oracle(mid_p[0], self.bVal, mid_p[1], self.dVal)
        #     if (mid_score == score_c):
        #        end = mid
        #     else:
        #         start = mid+1
        
        # print("POINT", potential_endpoints[mid])

        # return endpoints

    def get_adjacent(self, p):
        self.find_tp_scores(p)
        print(p.defining_points, p.scores, p.frame_point)

        adjPoints = []
        if p.frame_point:
            print(p.frame_point)
            adjPoints.append(self.find_adjacent_from_scores(p, ((p.frame_point+1)%4)))
        else:
            for i in range(4):
                s1, s2 = p.scores[i], p.scores[(i+1)%4]
                if s1 != s2:
                    adjPoints.append(self.find_adjacent_from_scores(p, i))

        # if len(sigs) < 2:
        #     print(f"Only one unique a, c signature from subopt for {tuple(p)}.", "Signatures are:", sigs)
        #     while len(sigs) < 2:
        #         eng += eng
        #         print(f"Iterating subopt until multiple signatures are found, eng={eng}")

        #         sigs = self.find_cyclically_ordered_signatures(p, eng)

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

        # adjPoints = []
        # adjSegments = []
        # for i in range(-1, len(sigs) - 1):
        #     if self.OBframeSignature(p, sigs[i], sigs[i + 1]):
        #         continue
        #     seg, point = self.construct_segment_from_point(p, sigs[i], sigs[i + 1])
        #     adjSegments.append(seg)
        #     adjPoints.append(point)

        #     if len(sigs) == 2:
        #         break
                
        print(p, adjPoints)
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

        return([pointDict[v] for v in self.vertices_from_geometry(hull)])
    
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
