from sympy import Point, Line, Segment, Line2D, Segment2D, Point2D, atan, Ray, zoo, pi, Polygon, convex_hull

_debug = True
_rounding = 2

def debug_print(*s):
    if _debug:
        print(*s)

def construct_segment_from_point(self, point, score_r, score_l):
    ray = self.find_segment_direction(point, score_r, score_l)
    debug_print("RAY", ray.p1, ray.p2, score_r, score_l)

    # Check if segment has already been found in ray
    for s in self.tippingSegments:
                # if (s.p1 == point or s.p2 == point) and ray.contains(s):
        if (s.p2 == point and (s.p1.distance(ray) < 0.02 or abs(pi - s.angle_between(ray)) < 0.01)):# abs(pi - s.angle_between(ray)) < 0.01):# ( ray.distance(s.p1) < 0.1): #< 0.1 contains(s)
            endpoint = s.p1
            if endpoint == point:
                debug_print("BAD CASE")
                endpoint = s.p2
            debug_print("SKIPPING SEGMENT", s)
            return s, endpoint

    #Truncate ray using convex hull
    # queue_hull = convex_hull(*self.pointQueue, point, polygon=True)
    ray_hull_intersection = self.find_ray_hull_intersection(ray, point)
    
    # [p for p in ray.intersection(self.pointQueueHull.scale(*(1.01,)*2)) if p != point][0]
    # if type(ray_hull_intersection) == Segment2D: #Occurs when tipping segment is an edge of the convex hull. 
    #     ray_hull_intersection = ray_hull_intersection.p2 if ray_hull_intersection.p2 != point else ray_hull_intersection.p1

    #Segment the ray to find tipping point
    seg_hull_score = self.nntm.vertex_oracle(ray_hull_intersection[0], self.bVal, ray_hull_intersection[1], self.dVal)
    endpoint = self.find_segment_endpoint(point, score_l, ray_hull_intersection, seg_hull_score, score_r)

    #Check if endpoint is within roudning error of visited point
    for p in self.visited:
        if p.taxicab_distance(endpoint) < 5*(10**-_rounding):
            endpoint = p

    endpoint = Point(round(endpoint[0],_rounding), round(endpoint[1],_rounding))
    s = Segment(point, endpoint)
    return s, endpoint

def find_ray_hull_intersection(self, ray, point):
    ray_hull_intersections = [p for p in ray.intersection(self.pointQueueHull) if p != point]
    
    if len(ray_hull_intersections) == 0:
        for i in range(len(self.pointQueueHull.vertices)):
            p1 = self.pointQueueHull.vertices[i]
            p2 = self.pointQueueHull.vertices[(i+1)%len(self.pointQueueHull.vertices)]
            #Sort the points so that we construct the segment with acute angle to ray
            sorted_points = sorted((p1,p2), key=lambda p: p.taxicab_distance(point))
            segment = Segment(sorted_points[0], sorted_points[1])

            if (segment.distance(ray.p1) < 0.01 and abs(ray.angle_between(segment)) < .1):
                debug_print("CLOSE SEGMENT", segment, p1, p2, sorted_points, segment.p2)
                ray_hull_intersections = [segment.p2]
                break
                
    ray_hull_intersection = ray_hull_intersections[0]
    if type(ray_hull_intersection) == Segment2D: #Occurs when tipping segment is an edge of the convex hull. 
        ray_hull_intersection = ray_hull_intersection.p2 if ray_hull_intersection.p2 != point else ray_hull_intersection.p1
    
    return ray_hull_intersection


# Finds the direction of a segment given its left and right score vector.
# Returns a ray in the correct direction.
def find_segment_direction(self, point, score_r, score_l):
    #Variables for tipping line equation
    dx = score_r[0] - score_l[0]
    dz = score_r[2] - score_l[2]

    slope = (-dx)/dz if dz != 0 else (zoo)
    angle = atan(slope) if slope != zoo else pi/2
    if dz < 0 or (dz == 0 and dx > 0): 
        angle += pi
    
    return Ray(point, angle=angle)

# Finds the direction of a segment given its left and right score vector.
# Returns a segment that intersects the frame in the correct direction.
# def find_segment_direction(self, point, score_r, score_l):
#     #Variables for tipping line equation
#     dx = score_r[0] - score_l[0]
#     dz = score_r[2] - score_l[2]
#     a1 = point[0]
#     c1 = point[1]
#     longSeg = None

#     vSegments = []
#     hSegments = []
#     if (dz != 0):
#         hSegments = [Segment(point, Point(self.aB, (-dx/dz)*(self.aB-a1) + c1)),  Segment(point, Point(self.ab, (-dx/dz)*(self.ab-a1) + c1))]
#     if (dx != 0):
#         vSegments = [Segment(point, Point((-dz/dx)*(self.cB-c1) + a1, self.cB)), Segment(point, Point((-dz/dx)*(self.cb-c1) + a1, self.cb))]

#     #Determing the direction of the ray
#     vertical = (hSegments == [])
#     horizontal = (vSegments == [])
#     if dx <= 0 and dz <= 0:
#         #north west 
#         if vertical or ((not horizontal) and abs(vSegments[0].p2[0]) <= self.aB and abs(vSegments[0].p2[1]) <= self.cB): 
#             longSeg = vSegments[0]
#         else:
#             longSeg = hSegments[1]
#     elif dx > 0 and dz <= 0:
#         #south west
#         if vertical or ((not horizontal) and abs(vSegments[1].p2[0]) <= self.aB and abs(vSegments[1].p2[1]) <= self.cB): 
#             longSeg = vSegments[1]
#         else:
#             longSeg = hSegments[1]
#     elif dx <= 0 and dz > 0:
#         #north east
#         if vertical or ((not horizontal) and abs(vSegments[0].p2[0]) <= self.aB and abs(vSegments[0].p2[1]) <= self.cB): 
#             longSeg = vSegments[0]
#         else:
#             longSeg = hSegments[0]
#     elif dx > 0 and dz > 0:
#         #south east
#         if vertical or ((not horizontal) and abs(vSegments[1].p2[0]) <= self.aB and abs(vSegments[1].p2[1]) <= self.cB): 
#             longSeg = vSegments[1]
#         else:
#             longSeg = hSegments[0]
    
#     return longSeg

# Find the endpoint of segmnent given its base vertex
def find_segment_endpoint(self, basePoint, baseScore, endPoint, endScore, altScore):
    # debug_print("P1", basePoint, baseScore, endPoint, endScore, altScore)
    intersection, _ = self.find_tipping_line_intersection(basePoint, endPoint, baseScore, endScore)

    # debug_print("INTERSECTION", basePoint, baseScore, endPoint, endScore, altScore, intersection)
    if type(intersection) == Line2D:
        # debug_print("INTERSECTION", basePoint, baseScore, endPoint, endScore, altScore, intersection)
        intersection, _ = self.find_tipping_line_intersection(basePoint, endPoint, altScore, endScore)
    
    if intersection == None or type(intersection) == Line2D or (intersection.distance(endPoint) < 0.01):
        return endPoint

    interScore = self.nntm.vertex_oracle(intersection[0], self.bVal, intersection[1], self.dVal)
    return self.find_segment_endpoint(basePoint, baseScore, intersection, interScore, altScore)

def distance_to_intersection(self, seg1, seg2):
    inter = seg1.intersection(seg2)
    if len(inter) > 0:
        if type(inter[0]) is Segment2D:
            inter[0] = min([inter[0].p1, inter[0].p2], key=lambda t: t.distance(seg2.p1))
        dist = inter[0].distance(seg1.p1)
        if dist > 0:
            return dist
        else:
            return 10*max(self.aB, self.cB)
    else:
        return 10*max(self.aB, self.cB)

# Shorten a given segment by finding the intersection with the closest segment already found.
def shorten_segment(self, seg):
    intersections = []
    for s in self.tippingSegments:
        inter = seg.intersection(s)
        if len(inter) > 0:
            if type(inter[0]) is Segment2D:
                inter[0] = min([inter[0].p1, inter[0].p2], key=lambda t: t.distance(seg.p1))
            
            dist = inter[0].distance(seg.p1)
            if dist > 0:
                intersections.append((inter[0], dist))
    
    if len(intersections) == 0:
        return seg
  
    new_seg = Segment(seg.p1, min(intersections, key=lambda t: t[1])[0])
    return new_seg

def shorten_segment_2(self, seg):
    min_segement = min(self.tippingSegments, key=lambda t: self.distance_to_intersection(seg, t))
    intersection = seg.intersection(min_segement)
    if intersection == [] or intersection[0] == seg.p1:
        return seg

    if type(intersection[0]) is Segment2D:
        intersection[0] = min([intersection[0].p1, intersection[0].p2], key=lambda t: t.distance(seg.p1))

    new_seg = Segment(seg.p1, intersection[0])
    
    return new_seg

# Computes the intersection with a tipping line given 2 points their scores.
# Returns intersection point, endpoints of tipping line
def find_tipping_line_intersection(self, p1, p2, s1, s2):
    # debug_print(f"{(p1[0], p1[1])}, {(p2[0], p2[1])}")
    paramLine = Line(p1, p2)
    
    x1, y1, z1, w1 = s1
    x2, y2, z2, w2 = s2
    
    k1 = self.bVal * y1 + self.dVal * w1
    k2 = self.bVal * y2 + self.dVal * w2

    # debug_print(f"({x1 - x2})/({z2 - z1})x+({k1}-{k2})/({z2-z1})") #TIPPING LINE BETWEEN {(p1[0], p1[1])}, {(p2[0], p2[1])}: 
        # debug_print(f"SCORES: {[s for s in s1]}, {[s for s in s2]}")
        # debug_print(f"PARAMS: {[s for s in p1]}, {[s for s in p2]}")

    if ((z2 - z1) == 0 and (x1-x2) == 0):
        return None, None

    point1, point2 = None, None
    if ((z2 - z1) == 0): 
        #VERTICAL LINE
        a = (k2 - k1) / (x1 - x2)
        point1 = Point(a, self.cB)
        point2 = Point(a, self.cb)

    else:
        x = (x1 - x2)
        const = (k1 - k2)
        point1 = Point(self.aB, (self.aB * x + const) / (z2 - z1))
        point2 = Point(self.ab, (self.ab * x + const) / (z2 - z1))
    
    #Lines are parallel when we need to check alt signature
    #THIS CAN BE SIMPLIFIED
    tipLine = Line(point1, point2)
    # if tipLine.is_parallel(paramLine):
    #     return paramLine, (point1, point2)
    if tipLine.smallest_angle_between(paramLine) < 0.1:
        debug_print("SLOPES", tipLine.slope, paramLine.slope)
        return paramLine, (point1, point2)
    
    interPoint = Line(point1, point2).intersection(paramLine)[0]
    # debug_print("INTERPOINT", tuple(interPoint), tuple(p1), tuple(p2), sep=", ")
    return interPoint, (point1, point2)

#p1, p2 and s1, s2 are left and right parameters and scores respectively.
def find_tipping_line(self, s1, s2):
    x1, y1, z1, w1 = s1
    x2, y2, z2, w2 = s2
    
    k1 = self.bVal * y1 + self.dVal * w1
    k2 = self.bVal * y2 + self.dVal * w2

    if ((z2 - z1) == 0 and (x1-x2) == 0):
        return None, None

    point1, point2 = None, None
    if ((z2 - z1) == 0): 
        #VERTICAL LINE
        da = (k2 - k1) / (x1 - x2)
        eq_c = lambda c: da
        eq_a = None
        slope = zoo
        # point1 = Point(a, self.cB)
        # point2 = Point(a, self.cb)
    elif ((x2 - x1) == 0):
        dc = (k1 - k2) / (z2 - z1)
        eq_c = None
        eq_a = lambda c: dc
        slope = 0
    else:
        dx = (x1 - x2)
        dz = (z2 - z1)
        const = (k1 - k2)
        eq_c = lambda c: (c * dz - const) / dx 
        eq_a = lambda a: (a * dx + const) / dz
        slope = dx/dz
        # point1 = Point(self.aB, (self.aB * x + const) / (z2 - z1))
        # point2 = Point(self.ab, (self.ab * x + const) / (z2 - z1))

    #eq_a is equation outputs c given a, eq_c outputs a given c
    return eq_a, eq_c, slope
#Line(point1, point2)