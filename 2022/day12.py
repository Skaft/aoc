from collections import deque

import pytest

from helpers import AoCSolution


DAY = 12


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        self.grid = grid = {}
        for r, row in enumerate(raw_input.splitlines()):
            for c, value in enumerate(row):
                if value == "a" and c > 0:
                    continue
                if value == "S":
                    start = r, c
                    value = "a"
                elif value == "E":
                    end = r, c
                    value = "z"
                grid[r, c] = ord(value) - 97
        return start, end, grid

    def neighbors(self, pos):
        r, c = pos
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in dirs:
            if (nb := (r + dr, c + dc)) in self.grid:
                yield nb

    def allowed_move(self, from_, to):
        if 0 <= self.grid[to] - self.grid[from_] <= 1:
            return True
        if self.grid[from_] == ord("r") - 97 and self.grid[to] == ord("p") - 97:
            return True
        return False 

    def dijkstra(self, start, end):
        steplog = {start: 0}
        queue = deque([start])
        steps = 0
        while queue:
            pos = queue.popleft()
            steps = steplog[pos]
            for nb in self.neighbors(pos):
                if nb in steplog:
                    continue
                if not self.allowed_move(pos, nb):
                    continue
                steplog[nb] = steps + 1
                queue.append(nb)
        return steplog[end]

    def main(self, inputs):
        start, end, grid = inputs
        steps = self.dijkstra(start, end)
        return steps


class PartTwo(PartOne):
    def main(self, inputs):
        _, end, grid = inputs
        best = float("inf")
        for start in grid:
            if start[1] == 0:
                steps = self.dijkstra(start, end)
                if steps < best:
                    best = steps
        return best


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 31

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 29