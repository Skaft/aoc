from itertools import cycle
from collections import deque

import pytest

from helpers import AoCSolution



DAY = 17


class Rock:
    def __init__(self, type_, peak_height):
        x = 2
        y = peak_height + 3
        if type_ == "-":
            self.cells = {(x, y), (x + 1, y), (x + 2, y), (x + 3, y)}
        elif type_ == "+":
            self.cells = {
                (x, y + 1), (x + 1, y), (x + 1, y + 1), 
                (x + 1, y + 2), (x + 2, y + 1)}
        elif type_ == "L":
            self.cells = {
                (x, y), (x + 1, y), (x + 2, y), (x + 2, y + 1), (x + 2, y + 2)
            }
        elif type_ == "I":
            self.cells = {(x, y), (x, y + 1), (x, y + 2), (x, y + 3)}
        elif type_ == "#":
            self.cells = {
                (x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)
            }
    
    def if_moved(self, dx, dy):
        return {(x + dx, y + dy) for (x, y) in self.cells}


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        return cycle(raw_input)

    def shift(self, rock, jet, grid):
        if jet == "<":
            if min(x for x, y in rock.cells) == 0:
                return
            potential_pos = rock.if_moved(-1, 0)
        elif jet == ">":
            if max(x for x, y in rock.cells) == 6:
                return
            potential_pos = rock.if_moved(1, 0)
        elif jet == "v":
            if min(y for x, y in rock.cells) == 0:
                return
            potential_pos = rock.if_moved(0, -1)
        if not grid.intersection(potential_pos):
            rock.cells = potential_pos
            return 1

    def drop(self, rock, jet_pattern, grid):
        for jet in jet_pattern:
            self.shift(rock, jet, grid)
            if not self.shift(rock, "v", grid):
                grid.update(rock.cells)
                break

    def display(self, grid):
        height = max(y for x, y in grid)
        tower = [list("." * 7) for _ in range(height + 1)]
        print()
        for x, y in grid:
            tower[-1 - y][x] = "#"
        for level in tower:
            row = "".join(level)
            print(f"|{row}|")
        print("+-------+")

    def main(self, jet_pattern):
        rock_types = cycle(["-", "+", "L", "I", "#"])
        peak = 0
        grid = set()
        for _ in range(2022):
            type_ = next(rock_types)
            rock = Rock(type_, peak)
            self.drop(rock, jet_pattern, grid)
            peak = max(peak, max(y for x, y in rock.cells) + 1)
        return peak




class PartTwo(PartOne):
    def generate_height_diffs(self, jet_pattern):
        rock_types = cycle(["-", "+", "L", "I", "#"])
        peak = 0
        prev = 0
        grid = set()
        while True:
            for _ in range(5):
                type_ = next(rock_types)
                rock = Rock(type_, peak)
                self.drop(rock, jet_pattern, grid)
                peak = max(peak, max(y for x, y in rock.cells) + 1)
            yield peak - prev
            prev = peak

    @staticmethod
    def sequence_in_list(lst, seq):
        a = seq[0]
        target = list(seq)
        for i, n in enumerate(lst):
            if n == a:
                if lst[i:i+len(seq)] == target:
                    return i

    def calc_height(self, prefix, repeating, blocks):
        pre_len = len(prefix) * 5
        rep_len = len(repeating) * 5
        prefix_height = sum(prefix)
        full_laps, remains = divmod(blocks - pre_len, rep_len)
        repeat_height = full_laps * sum(repeating)
        suffix_height = sum(repeating[:remains // 5])
        return prefix_height + repeat_height + suffix_height

    def main(self, jet_pattern):
        height_diffs = self.generate_height_diffs(jet_pattern)
        N = 30
        all_diffs = [next(height_diffs) for _ in range(N)]
        last_N = deque(all_diffs, maxlen=N)
        for diff in height_diffs:
            last_N.append(diff)
            if (i := self.sequence_in_list(all_diffs, last_N)):
                break
            all_diffs.append(diff)
        prefix = all_diffs[:i]
        repeating = all_diffs[i:-N + 1]
        return self.calc_height(prefix, repeating, 1_000_000_000_000)


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 3068

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 1514285714288