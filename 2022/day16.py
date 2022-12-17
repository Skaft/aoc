import re
from dataclasses import dataclass
from collections import deque

import pytest

from helpers import AoCSolution


DAY = 16


@dataclass
class Valve:
    name : str
    rate : int
    leads_to : list

class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        valves = {}
        pattern = r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)"
        for line in raw_input.splitlines():
            name, rate, leads_to_str = re.search(pattern, line).groups()
            rate = int(rate)
            leads_to = leads_to_str.split(", ")
            valves[name] = Valve(name, rate, leads_to)
        return valves

    @staticmethod
    def generate_paths_from(start, valves):
        steps_to = {}
        queue = deque([(start, )])
        targets = sum([valve.rate > 0 for valve in valves.values()])
        if valves[start].rate > 0:
            targets -= 1
        while len(steps_to) < targets:
            path = queue.popleft()
            for nxt in valves[path[-1]].leads_to:
                if nxt in path:
                    continue
                new_path = (*path, nxt)
                if valves[nxt].rate:
                    if nxt not in steps_to or len(new_path) < steps_to[nxt]:
                        steps_to[nxt] = len(path)
                queue.append(new_path)
        return steps_to

    @staticmethod
    def get_all_paths(valves):
        paths = {}
        for name, valve in valves.items():
            if valve.rate or name == "AA":
                paths[name] = PartOne.generate_paths_from(name, valves)
        return paths

    def main(self, valves):
        best = 0
        paths = self.get_all_paths(valves)
        def search(pos, mins_left, on=(), score=0):
            if mins_left <= 0:
                return
            nonlocal best
            if score > best:
                best = score
            for destination, cost in paths[pos].items():
                if destination in on:
                    continue
                remains = mins_left - cost - 1
                valve_score = valves[destination].rate * remains
                search(destination, remains, on + (destination,), score + valve_score)
        search("AA", 30)
        return best

class PartTwo(PartOne):
    pass


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS
def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 1651

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 1707