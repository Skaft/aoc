from input import data, sample, sample2, sample3
from collections import defaultdict
import itertools as it

from fractions import Fraction


def parse(data):
    asts = set()
    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                asts.add((x, y))
    return asts

def sees(a, asts):
    in_sight = defaultdict(lambda: defaultdict(list))
    x1, y1 = a
    for b in asts:
        if a == b:
            continue
        x2, y2 = b
        above = y2 < y1
        right = x2 >= x1
        if x1 == x2:
            f = (y2 - y1) // abs(y2 - y1), 0
        else:
            f = Fraction((y2 - y1), (x2 - x1))
            f = (f.numerator, f.denominator)
        in_sight[above, right][f].append(b)

    return in_sight

def sort_by_dist(a, lst):
    x, y = a
    lst.sort(key=lambda p: ((p[0] - x)**2 + (p[1] - y)**2)**0.5, reverse=True)

def sort_clockwise(quad, keys):

    if quad == (True, True):
        return sorted(keys, key=lambda a: float('inf') if a[1] == 0 else abs(a[0]/a[1]), reverse=True)
    if quad == (False, True):
        return sorted(keys, key=lambda a: float('inf') if a[1] == 0 else a[0]/a[1])
    if quad == (False, False):
        return sorted(keys, key=lambda a: a[0]/a[1])
    if quad == (True, False):
        return sorted(keys, key=lambda a: a[0]/a[1])


def part1(asts):
    in_sight = defaultdict(lambda :defaultdict(set))

    for a, b in it.permutations(asts, 2):
        x1, y1 = a
        x2, y2 = b
        above = y2 < y1
        right = x2 > x1
        if x1 == x2:
            fa = (y2 - y1) // abs(y2 - y1), 0
        else:
            fa = Fraction((y2 - y1), (x2 - x1))
        in_sight[a][above, right].add(fa)

    num_in_sight = {ast: sum(len(v) for v in sees.values())
                    for ast, sees in in_sight.items()}
    base_pos, base_sees = max(num_in_sight.items(), key=lambda a: a[1])
    print(base_sees)
    return base_pos

def part2(start, asts):
    in_sight = sees(start, asts)

    for direction in in_sight.values():
        for asteroids in direction.values():
            sort_by_dist(start, asteroids)

    quad_order = ((True, True), (False, True), (False, False), (True, False))
    dir_order = {quad : sort_clockwise(quad, list(in_sight[quad]))
                 for quad in quad_order}

    for quadrant in it.cycle(quad_order):
        for direction in dir_order[quadrant]:
            asteroids = in_sight[quadrant][direction]
            if asteroids:
                yield asteroids.pop()


asteroids = parse(data)
base_ast = part1(asteroids)
gen = part2(base_ast, asteroids)
for _ in range(200):
    ast = next(gen)
print(ast[0] * 100 + ast[1])
