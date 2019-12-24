from input import data
from collections import defaultdict


def parse(string):
    bugs = set()
    for y, line in enumerate(string.splitlines()):
        for x, char in enumerate(line):
            if char == '#':
                bugs.add((x, y))
    return bugs


def part1(string):
    bugs = parse(string)
    coords = set((x, y) for x in range(5) for y in range(5))
    states = set()
    while True:
        state = frozenset(bugs)
        if state in states:
            break
        states.add(state)
        next_state = set()
        for x, y in coords:
            nbs = 0
            for nb in ((x+1, y), (x-1,y), (x,y+1), (x,y-1)):
                if nb in bugs:
                    nbs += 1
            if (x, y) in bugs:
                if nbs == 1:
                    next_state.add((x, y))
            elif nbs in (1, 2):
                next_state.add((x, y))
        bugs = next_state
    biodiv = 0
    for x, y in bugs:
        n = y*5 + x
        biodiv += 2**n
    print(biodiv)

def neighbors(x, y, z):
    L, R, U, D = (x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z)

    if (x, y) == (2, 1):
        yield from [L, R, U]
        for xr in range(5):
            yield (xr, 0, z + 1)
    elif (x, y) == (2, 3):
        yield from [L, R, D]
        for xr in range(5):
            yield (xr, 4, z + 1)
    elif (x, y) == (1, 2):
        yield from [L, U, D]
        for yr in range(5):
            yield (0, yr, z + 1)
    elif (x, y) == (3, 2):
        yield from [R, U, D]
        for yr in range(5):
            yield (4, yr, z + 1)
    else:
        if x == 0:
            L = (1, 2, z - 1)
        elif x == 4:
            R = (3, 2, z - 1)
        if y == 0:
            U = (2, 1, z - 1)
        elif y == 4:
            D = (2, 3, z - 1)
        yield from (L, R, U, D)


def part2(string):
    bugs = parse(string)
    bugs = {(x, y, 0) for x, y in bugs}
    for _ in range(200):
        adjacent_bugs = defaultdict(int)
        for x, y, z in bugs:
            for nb in neighbors(x, y, z):
                adjacent_bugs[nb] += 1
        next_state = set()
        for pos, count in adjacent_bugs.items():
            if pos in bugs:
                if count == 1:
                    next_state.add(pos)
            elif count in (1, 2):
                next_state.add(pos)
        bugs = next_state
    print(len(bugs))


part1(data)
part2(data)
