from sympy import convex_hull
import json

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
    
    with open("sig_file.txt", "w") as f:
        final_data = {}
        for s, p in polygons:
            try:
                vertices = [str((x[0],x[1])) for x in p.vertices]
            except AttributeError:
                print("Not a polygon", s, p)
                continue
            
            for v in vertices:
                try:
                    final_data[v].append((s[0],s[1],s[2],s[3]))
                except KeyError:
                    final_data[v] = [(s[0],s[1],s[2],s[3]),]

        for k, vs in final_data.items():
            f.write(f"{k}: {';'.join(str(v) for v in vs)}\n")  
    
    with open(visitedFile, "w") as f:
        for v in [*self.visited]:
            f.write(f"{(v[0],v[1])}\n")
    
    # with open(segmentFile, "w") as f:
    #     for s in self.tippingSegments:
    #         f.write(f"{(s.p1[0],s.p1[1]), (s.p2[0],s.p2[1])}\n")

def save_signatures(self, save_file="temp_sigs.json"):
    flattened_sigs = {str(tuple(k)):[tuple(int(y) for y in x) for x in v] for k,v in self.signatures.items()}
    with open(save_file, "w") as f:
        json.dump(flattened_sigs,f)

def save_segments(self, save_file="temp_segments.json"):
    flattened_segments = [(tuple(float(round(x, 2)) for x in s.p1), tuple(float(round(x, 2)) for x in s.p2)) for s in self.tippingSegments]
    with open(save_file, "w") as f:
        json.dump(flattened_segments,f)