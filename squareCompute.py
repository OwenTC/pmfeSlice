from fanSlice import fanSlice


points = []
for i in range(1, 50):
    print(i, "!!!!!!!!!!!!!!!!!THIS IS i!!!!!!!!!!!!!!!!!!!!!!!!!:", i)
    s = fanSlice(i, i)
    s.build()
    points.extend(s.searched.keys())

print(points)