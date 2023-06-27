from sympy import Point, Line, Segment, Line2D, Segment2D
from pmfeInterface import pmfeInterface

def construct_from_point(self, point, score_r, score_l):
    longSeg = self.find_segment_direction(point, score_r, score_l)

    # Check if segment has already been found
    for s in self.tippingSegments:
        if longSeg.contains(s) and (s.p1 == point or s.p2 == point):
            endpoint = s.p1
            if endpoint == point:
                endpoint = s.p2
            return s, endpoint

    longSeg = self.shorten_segment(longSeg)
    
    longSegScore = self.nntm.vertex_oracle(longSeg.p2[0], self.bVal, longSeg.p2[1], self.dVal)
    endpoint = self.find_segment_endpoint(point, score_l, longSeg.p2, longSegScore, score_r)
    s = Segment(point, endpoint)
    return s, endpoint

# Finds the direction of a segment given its left and right score vector.
# Returns a segment that intersects the frame in the correct direction.
def find_segment_direction(self, point, score_r, score_l):
    #Variables for tipping line equation
    dx = score_r[0] - score_l[0]
    dz = score_r[2] - score_l[2]
    a1 = point[0]
    c1 = point[1]
    longSeg = None

    vSegments = []
    hSegments = []
    if (dz != 0):
        hSegments = [Segment(point, Point(self.aB, (-dx/dz)*(self.aB-a1) + c1)),  Segment(point, Point(-self.aB, (-dx/dz)*(-self.aB-a1) + c1))]
    if (dx != 0):
        vSegments = [Segment(point, Point((-dz/dx)*(self.cB-c1) + a1, self.cB)), Segment(point, Point((-dz/dx)*(-self.cB-c1) + a1, -self.cB))]

    #Determing the direction of the ray
    vertical = (hSegments == [])
    horizontal = (vSegments == [])
    if dx <= 0 and dz <= 0:
        #north west 
        if vertical or ((not horizontal) and abs(vSegments[0].p2[0]) <= self.aB and abs(vSegments[0].p2[1]) <= self.cB): 
            longSeg = vSegments[0]
        else:
            longSeg = hSegments[1]
    elif dx > 0 and dz <= 0:
        #south west
        if vertical or ((not horizontal) and abs(vSegments[1].p2[0]) <= self.aB and abs(vSegments[1].p2[1]) <= self.cB): 
            longSeg = vSegments[1]
        else:
            longSeg = hSegments[1]
    elif dx <= 0 and dz > 0:
        #north east
        if vertical or ((not horizontal) and abs(vSegments[0].p2[0]) <= self.aB and abs(vSegments[0].p2[1]) <= self.cB): 
            longSeg = vSegments[0]
        else:
            longSeg = hSegments[0]
    elif dx > 0 and dz > 0:
        #south east
        if vertical or ((not horizontal) and abs(vSegments[1].p2[0]) <= self.aB and abs(vSegments[1].p2[1]) <= self.cB): 
            longSeg = vSegments[1]
        else:
            longSeg = hSegments[0]
    
    return longSeg

# Find the endpoint of segmnent given its base verte
def find_segment_endpoint(self, basePoint, baseScore, endPoint, endScore, altScore):
    intersection, _ = self.find_tipping_line_intersection(basePoint, endPoint, baseScore, endScore)

    if type(intersection) == Line2D:
        intersection, _ = self.find_tipping_line_intersection(basePoint, endPoint, altScore, endScore)
    
    if intersection == None or intersection == endPoint or type(intersection) == Line2D:
        return endPoint

    interScore = self.nntm.vertex_oracle(intersection[0], self.bVal, intersection[1], self.dVal)
    return self.find_segment_endpoint(basePoint, baseScore, intersection, interScore, altScore)

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

# Computes the intersection with a tipping line given 2 points their scores.
# Returns intersection point, endpoints of tipping line
def find_tipping_line_intersection(self, p1, p2, s1, s2):
    paramLine = Line(p1, p2)
    
    x1, y1, z1, w1 = s1
    x2, y2, z2, w2 = s2
    
    k1 = self.bVal * y1 + self.dVal * w1
    k2 = self.bVal * y2 + self.dVal * w2

    if ((z2 - z1) == 0 and (x1-x2) == 0):
        return None, None
    
    if ((z2 - z1) == 0): 
        #VERTICAL LINE
        a = (k2 - k1) / (x1 - x2)
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
        
        interPoint = Line(point1, point2).intersection(paramLine)[0]

        return interPoint, (point1, point2)