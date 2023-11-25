import re
from dataclasses import dataclass
from collections import deque
from itertools import combinations

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

    def find_combo_scores(self, valves, start_mins):
        paths = self.get_all_paths(valves)
        combos = {}
        def search(pos, mins_left, on=(), score=0):
            if mins_left <= 0:
                return
            orderless = frozenset(on)
            if score > combos.get(orderless, 0):
                combos[orderless] = score
            for destination, cost in paths[pos].items():
                if destination in on:
                    continue
                remains = mins_left - cost - 1
                valve_score = valves[destination].rate * remains
                search(destination, remains, on + (destination,), score + valve_score)
        search("AA", start_mins)
        return combos

    def main(self, valves):
        combos = self.find_combo_scores(valves, start_mins=30)
        return max(combos.values())

class PartTwo(PartOne):
    def main(self, valves):
        combos = self.find_combo_scores(valves, start_mins=26)
        openable = [name for name, valve in valves.items() if valve.rate]
        best_combined = 0
        for combo1, score in combos.items():
            unused = [valve for valve in openable if valve not in combo1]
            best_other = 0
            for num in range(1, len(unused) + 1):
                for combo2 in combinations(unused, num):
                    score2 = combos.get(frozenset(combo2), 0)
                    if score2 > best_other:
                        best_other = score2
            combined = score + best_other
            if combined > best_combined:
                best_combined = combined
        return best_combined


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

def test_part2_combos():
    sol = PartTwo(DAY)
    valves = sol.clean_input(sol.raw_test_inputs[0])
    combos = sol.find_combo_scores(valves, 26)
    i_open = combos[frozenset(("JJ", "BB", "CC"))]
    e_open = combos[frozenset(("DD", "HH", "EE"))]
    assert i_open + e_open == 1707