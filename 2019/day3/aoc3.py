from input import data


def sol(data):
    dirs = {'R': (1, 0),
            'L': (-1, 0),
            'U': (0, -1),
            'D': (0, 1),}
    sets = []
    for wire in data.split('\n'):
        if wire:
            pts = {}
            sets.append(pts)
            x, y = 0, 0
            c = 0
            for d, *steps in wire.split(','):
                steps = int(''.join(steps))
                dx, dy = dirs[d]
                for _ in range(steps):
                    x += dx
                    y += dy
                    c += 1
                    pts[x, y] = c
    intsect = set(sets[0]).intersection(sets[1])
    # part 1
    print(min(abs(x) + abs(y) for x, y in intsect))

    # part 2
    print(min(sets[0][pt] + sets[1][pt] for pt in intsect))


sol(data)
