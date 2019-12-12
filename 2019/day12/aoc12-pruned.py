from input import data
import itertools as it
import re
from math import gcd
from functools import reduce


class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = [0] * 3
        self.history = [[c] for c in pos]  # only need to track pos

    def __repr__(self):
        return f"pos={self.pos}, vel={self.velocity}"

    def gravitate(self, other):
        coord_pairs = zip(self.pos, other.pos, self.velocity)
        new_vel = []
        for my_coord, their_coord, cur_vel in coord_pairs:
            if my_coord > their_coord:
                cur_vel -= 1
            elif my_coord < their_coord:
                cur_vel += 1
            new_vel.append(cur_vel)
        self.velocity = new_vel

    def update_pos(self):
        for i, v in enumerate(self.velocity):
            self.pos[i] += v

    def update_history(self):
        for lst, coord in zip(self.history, self.pos):
            lst.append(coord)

    @property
    def energy(self):
        return sum(abs(c) for c in self.pos) * sum(abs(c) for c in self.velocity)

def parse(txt):
    pattern = r"-?\d+"
    out = []
    for line in txt.split('\n'):
        vals = [int(n) for n in re.findall(pattern, line)]
        out.append(vals)
    return out

def part1(string, steps=1000):
    positions = parse(string)
    moons = [Moon(pos) for pos in positions]
    for _ in range(steps):
        for a, b in it.combinations(moons, 2):
            a.gravitate(b)
            b.gravitate(a)
        for moon in moons:
            moon.update_pos()
    print(sum(m.energy for m in moons))

def part2(string):
    positions = parse(string)
    moons = [Moon(pos) for pos in positions]
    for _ in range(300000):  # <- ew.
        for a, b in it.combinations(moons, 2):
             a.gravitate(b)
             b.gravitate(a)
        for moon in moons:
             moon.update_pos()
        moon.update_history()  # only need to track one moon

    periods = {find_repeat_index(coord_list) for coord_list in moon.history}
    print(reduce(lcm, periods))

def find_repeat_index(lst, length=20):
    start = lst[:length]
    for i in range(1, len(lst) - length):
        if lst[i:i+length] == start:
            return i

def lcm(a, b):
    return a * b // gcd(a, b)

part1(data)
part2(data)
