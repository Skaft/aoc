from input import data
from collections import defaultdict
import itertools as it
from fractions import Fraction
from enum import Enum, auto

from helpers import clean_nested_dicts


class Side(Enum):
    RIGHT = auto()
    LEFT = auto()

    def __repr__(self):
        return self.name

RIGHT, LEFT = Side
Fraction.__repr__ = Fraction.__str__


def parse(lines):
    asteroids = set()
    for y, line in enumerate(lines.split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                asteroids.add((x, y))
    return asteroids

def get_sight_lines(asts: set) -> dict:
    sight_lines = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    inf = float('inf')
    for a, b in it.permutations(asts, 2):
        x1, y1 = a
        x2, y2 = b
        dif_y = y2 - y1
        dif_x = x2 - x1
        side = RIGHT if dif_x >= 0 else LEFT
        slope = Fraction(dif_y, dif_x) if dif_x else dif_y // abs(dif_y) * inf
        sight_lines[a][side][slope].append(b)
    return clean_nested_dicts(sight_lines)

def sort_by_dist(base, sight_lines):
    x, y = base
    dist = lambda p: ((p[0] - x)**2 + (p[1] - y)**2)**0.5
    for directions in sight_lines.values():
        for asteroids in directions.values():
            asteroids.sort(key=dist, reverse=True)

def count_visibles(ast):
    dirs_per_side = all_sight_lines[ast].values()
    return sum(len(dirs) for dirs in dirs_per_side)

def lasered_asteroids(base, sight_lines):
    sort_by_dist(base, sight_lines)
    for side in it.cycle((RIGHT, LEFT)):
        dct = sight_lines[side]
        clockwise_order = sorted(dct.items(), key=lambda p:p[0])
        for direction, asteroids in clockwise_order:
            yield asteroids.pop()
            if not asteroids:
                dct.pop(direction)

asteroids = parse(data)
all_sight_lines = get_sight_lines(asteroids)
base = max(all_sight_lines, key=count_visibles)

# part 1
print(count_visibles(base))

# part 2
sight_lines = all_sight_lines[base]
asteroid_queue = lasered_asteroids(base, sight_lines)

for _ in range(199):
    next(asteroid_queue)
x, y = next(asteroid_queue)
print(100 * x + y)
