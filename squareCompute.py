def computeSquare(FS, size = 50, step = 1):
    points = []
    # Static Computation
    for i in range(step, size, step):
        print("Iteration:", i)
        FS.build(i, i)
        points.extend(FS.searched.items())

    scores = {}
    for p, s in points:
        if s in scores.keys():
            scores[s].append(p)
        else:
            scores[s] = [p]

    return scores

# with open(args.output, 'w') as f:
#     f.write("score, points\n")
#     for s in scores.keys():
#         f.write(f"{s}, {scores[s]}\n")


# print(*[str(p[0])[7:] for p in points], sep=",")