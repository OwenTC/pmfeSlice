from sympy import ceiling, floor, Point
from math import copysign
class GridPoint:
    def __init__(self, a:int, c:int):
        self.a = a
        self.c = c
    
    def __add__(self, other):
        try:
            return GridPoint(self.a + other.a, self.c + other.c)
        except AttributeError:
            print(f"Sum with non GridPoint of type {type(other)}")
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    
    def __sub__(self, other):
        try:
            return GridPoint(self.a - other.a, self.c - other.c)
        except AttributeError:
            raise ValueError(f"Subtract with non GridPoint of type {type(other)}")

    def __mul__(self, other):
        try:
            if other is int:
                return GridPoint(self.a * otherself.a * other, self.c * other)
            else:
                return (self.a * other, self.c * other)
        except ValueError:
            raise ValueError(f"Multiply GridPoint with {type(other)}")
    
    def __rmul__(self, other):
        return self.__mul__(self, other)

    def __iter__(self):
        yield self.a
        yield self.c
    
    def __repr__(self) -> str:
        return str(tuple(self))

    def __str__(self):
        return str(tuple(self))
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, GridPoint):
            return tuple(self) == tuple(__value)
        else:
            raise ValueError(f"Cannot compare GridPoint with {type(__value)}")
        
    def __getitem__(self, key):
        key_to_attribute = {0:"a",1:"c"}
        return self.__getattribute__(key_to_attribute[0])
 
    def __hash__(self):
        return tuple(self)

class TippingPoint:
    def __init__(self, q1, q2, q3, q4, frame_point=0, corner_point=0):
        
        self.frame_point = frame_point
        self.corner_point = corner_point
        self.defining_points = tuple(GridPoint(*p) for p in (q1, q2, q3, q4))
        self.scores = [None]*4
        self.adjacentPoints = [None,]*4 #Adjacent points to (north, west, south, east)
    
    def add_adjacency(self, other, out_direction, in_direction):
        if self.adjacentPoints[out_direction] != None or other.adjacentPoints[in_direction] != None:
            print(f"Warning, multiple adjacencies in same direction. Replacing with\n{self}---{other}\n{out_direction}---{in_direction}")
        
        self.adjacentPoints[out_direction] = other
        other.adjacentPoints[in_direction] = self

        
    def add_scores(self, scores, start=1):
        #Add checks on length of score (maybe switch to adding structures)
        for i,s in enumerate(scores):
            self.scores[i+(start-1)] = s
    
    def center(self):
        a = (self.defining_points[2].a + .5)
        c = (self.defining_points[2].c + .5)
        return Point(a,c)

    def __str__(self):
        return ";".join(str(p) for p in self.defining_points)
    
    def __repr__(self):
        return self.__str__()

    def __key__(self):
        return (self.defining_points)

    def location_equal(self, other):
        return (self.defining_points == other.defining_points)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TippingPoint):
            return (self.__key__() == __value.__key__())
        else:
            return False
    
    # def __hash__(self) -> int:
        return self.__key__()

    @classmethod
    def tp_from_float_point(cls, point: tuple, frame_point=0, corner_point=0):
        if (ceiling(point[0]) == point[0]) or ceiling(point[1]) == point[1]:
            raise ValueError(f"Points must not have integer cordinates. Input was {point}")
        try:
            q1 = (ceiling(point[0]), ceiling(point[1]))
            q2 = (floor(point[0]), ceiling(point[1]))
            q3 = (floor(point[0]), floor(point[1]))
            q4 = (ceiling(point[0]), floor(point[1]))
        except IndexError:
            raise(f"Error, point must be 2D, input was {len(point)}D")
        return cls(q1, q2, q3, q4, frame_point, corner_point)
    
    @classmethod
    def tp_from_grid_point(cls, point: tuple, loc = 1, frame_point=0, corner_point=0):
        try:
            point = GridPoint(*point)
        except ValueError:
            raise(f"Error, point must be 2D, input was {len(point)}D")
        
        loc_switch = {1:GridPoint(1,1), 2:GridPoint(0,1), 3:GridPoint(0,0), 4:GridPoint(1,0)}
        
        q_points = []
        for i in range(1,5):
            q_points.append(tuple(point + (loc_switch[i] - loc_switch[loc])))

        return cls(*q_points, frame_point, corner_point)
    
    @classmethod 
    def tps_from_segment(cls, p1:tuple, p2:tuple):
        if (p1[0] != p2[0] and p1[1] != p2[1]) or p1 == p2:
            raise ValueError(f"{p1},{p2} not a grid segment")
        
        #Sort girdpoints so gps[0] is lower or furhter left
        gps = sorted([(p1), (p2)], key=sum)

        if gps[0][0] == gps[1][0]:
            #Vertical
            return (cls.tp_from_grid_point(gps[0],4),cls.tp_from_grid_point(gps[0],3))

        elif gps[1][1] == gps[1][1]:
            #Horizontal
            return (cls.tp_from_grid_point(gps[0],2),cls.tp_from_grid_point(gps[0],3))

        raise ValueError(f"{p1},{p2} not a grid segment")


class GridSegment:
    def __init__(self, p1:tuple, p2:tuple, direction:str, s1=None, s2=None):
        self.p1 = p1
        self.p2 = p2
        
        if direction in ("v","h"):
            self.direction = direction
        else:
            raise ValueError(f"Direction {direction} not v or h.")
        self.s1 = s1
        self.s2 = s2
    
    def endpoints(self):
        return (self.p1, self.p2)
    
    def midpoint(self):
        return (GridPoint(*self.p1) + GridPoint(*self.p2)) * 0.5
    
    @classmethod
    def gs_from_inter_point(cls, inter_p: tuple, p1:tuple, p2:tuple):
        try:
            a, c = int(inter_p[0]), int(inter_p[1])
        except IndexError:
            raise(f"Input point {inter_p} not of format (a,c).")
        
        if (p1[0] == p2[0]) and (inter_p[0] == a) and (inter_p[0] == p1[0]):
            return cls(*sorted([(a, c),(a,int(c+copysign(1,c)))], key=lambda p: abs(p[1]-p1[1])),direction="h")
        if (p1[1] == p2[1]) and (inter_p[1] == c) and (inter_p[1] == p1[1]):
            print(sorted([(a, c),(int(a+copysign(1,a)),c)], key=lambda p: abs(p[0]-p1[0])))
            return cls(*sorted([(a, c),(int(a+copysign(1,a)),c)], key=lambda p: abs(p[0]-p1[0])),direction="v")
        else:
            raise ValueError(f"Input point {inter_p} not on grid segment between {p1}, {p2}.")
    
    @classmethod
    def alt_gs_from_grid_point(cls, grid_p: tuple, p1:tuple, p2:tuple):
        a, c = grid_p[0], grid_p[1]
        if a != int(a) or c != int(c):
            raise ValueError(f"Input point {grid_p} not a gridpoint." )

        if (p1[0] == p2[0]) and (grid_p[0] == a) and (grid_p[0] == p1[0]):
            # seg_1 = cls(*sorted([(a, c),(a,c+1)], key=lambda p: abs(p[1]-p1[1])) ,"h")
            seg = cls(*sorted([(a, c),(a,int(c-copysign(1,c)))], key=lambda p: abs(p[1]-p1[1])) ,"h")
            return seg
        
        if (p1[1] == p2[1]) and (grid_p[1] == c) and (grid_p[1] == p1[1]):
            # seg_1 = cls(*sorted([(a, c),(a+1,c)], key=lambda p: abs(p[0]-p1[0])),"v")
            seg = cls(*sorted([(a, c),(int(a-copysign(1,a)),c)], key=lambda p: abs(p[0]-p1[0])),"v")
            return seg
        
        else:
            raise ValueError(f"Input point {grid_p} not on grid segment between {p1}, {p2}.")  


if __name__ == "__main__":
    s = GridSegment.gs_from_inter_point((-5000, -10690/3),(-5000,4000),(-5000,-4000))

    t = TippingPoint.tp_from_grid_point(s.p1, 1)
    print(t.center())
