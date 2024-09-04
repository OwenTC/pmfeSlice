from sympy import convex_hull
import pandas as pd

def save_data(self, ploygonFile : str = "polygons.txt", visitedFile : str = "visited.txt", segmentFile : str = "segments.txt", sigstructFile: str = "sigstruct.csv", basename: str = ""):
    ploygonFile = basename + ploygonFile
    visitedFile = basename + visitedFile
    segmentFile = basename + segmentFile
    sigstructFile = basename + sigstructFile

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
        for s, p in self.tippingSegments.items():
            s1, s2 = s
            p1, p2 = p
            f.write(f"{s1},{s2}:{(p1[0],p1[1]), (p2[0],p2[1])}\n")
    
    #Save sig_struct_data
    point_sig_struct_df = pd.DataFrame(self.nntm.point_sig_structs, columns=["a","b","c","d","x","y","z","w","struct"])
    point_sig_struct_df.to_csv(sigstructFile, index=False)