from sympy import convex_hull

def save_data(self, ploygonFile : str = "polygons.txt", visitedFile : str = "visited.txt", segmentFile : str = "segments.txt"):
    # Construct Polygons
    polygons = []
    for s in self.signatures.keys():
        polygons.append((s, convex_hull(*self.signatures[s])))
    
    with open(ploygonFile, "w") as f:
        for s, p in polygons:
            try:
                f.write(f"{(s[0],s[1],s[2],s[3])}: {','.join(str((x[0],x[1])) for x in p.vertices)}\n")
            except AttributeError:
                print("Not a polygon", s, p)
    
    with open(visitedFile, "w") as f:
        for v in [*self.visited]:
            f.write(f"{(v[0],v[1])}\n")
    
    with open(segmentFile, "w") as f:
        for s in self.tippingSegments:
            f.write(f"{(s.p1[0],s.p1[1]), (s.p2[0],s.p2[1])}\n")