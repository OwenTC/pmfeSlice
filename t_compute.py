# Score and parameter vectors scores as tuples (x,y,z,w) or (a,b,c,d)
from turtle import up
from sympy import Point, Polygon

from fsWithoutSubopt import fanSlice

from pmfeInterface import pmfeInterface
from tippingPoint import tippingPoint

class T_compute(fanSlice):
    def __init__(self, pmfe, rna_file, aB, cB, lB):
        super().__init__(pmfe, rna_file, True)
        self.aB = aB
        self.cB = cB
        self.lB = lB

    # def __init__(self):
    #      self().__init__(Fraction(50),Fraction(50))
    
    def build(self):
        # Initialize
        self.compute()
        #return starting queue with all the 

    def compute(self):
        p1, p2 = Point(self.aB, self.cB), Point(-self.aB, self.cB)
        s2 = self.nntm.vertex_oracle(p2[0], self.bVal, p2[1], self.dVal)
        s1 = self.nntm.vertex_oracle(p1[0], self.bVal, p1[1], self.dVal)

        #(p1,p2)
        self.addBoundryPointToQueue(self.findIntersections(p1, p2, s1, s2))

        #Find left edge of (0,0) region: (It will be the last list element???)
        region = self.bordersRemaining[-1].point
        score = self.bordersRemaining[-1].score1
        lp = Point(region[0], -self.cB)
        lp_score = self.nntm.vertex_oracle(lp[0], self.bVal, lp[1], self.dVal)
        self.addBoundryPointToQueue(self.findIntersections(region, lp, score, lp_score))

        print(self.bordersRemaining)
        for t in self.bordersRemaining:
            print(t.score1, t.score2)
    
    def create_polygons():
        #Lines at the top of the
        pass
        #Turn endpoints into polygons.