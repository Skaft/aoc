import pytest

from helpers import AoCSolution


DAY = 24


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        grid = {}
        rows = raw_input.splitlines()
        for r, row in enumerate(rows):
            for c, item in enumerate(row):
                if item in ".":
                    grid[r, c] = []
                elif item == "#":
                    continue
                else:
                    grid[r, c] = [item]
        self.dims = r, c
        return grid

    def display(self, grid):
        maxr, maxc = self.dims
        rows = [["."] * (maxc + 1) for _ in range(maxr + 1)]

        for r in range(maxr + 1):
            rows[r][0] = "#"
            rows[r][maxc] = "#"
        for c in range(2, maxc + 1):
            rows[0][c] = "#"
        for c in range(1, maxc - 1):
            rows[maxr][c] = "#"

        for (r, c), items in grid.items():
            if len(items) == 0:
                rows[r][c] = "."
            elif len(items) == 1:
                rows[r][c] = items[0]
            else:
                rows[r][c] = str(len(items))
        rows = ["".join(row) for row in rows]
        return "\n".join(rows)

    def move_blizzards(self, grid):
        maxr, maxc = self.dims
        next_grid = {
            (r, c): []
            for r in range(1, maxr)
            for c in range(1, maxc)
        }
        next_grid[0, 1] = []
        next_grid[maxr, maxc - 1] = []

        LEFT = 1
        RIGHT = maxc - 1
        TOP = 1
        BOTTOM = maxr - 1

        for (r, c), items in grid.items():
            for item in items:
                if item == ">":
                    if c == RIGHT:
                        nb = r, LEFT
                    else:
                        nb = r, c + 1
                elif item == "<":
                    if c == LEFT:
                        nb = r, RIGHT
                    else:
                        nb = r, c - 1
                elif item == "^":
                    if r == TOP:
                        nb = BOTTOM, c
                    else:
                        nb = r - 1, c
                elif item == "v":
                    if r == BOTTOM:
                        nb = TOP, c
                    else:
                        nb = r + 1, c
                else:
                    continue
                next_grid[nb].append(item)

        return next_grid

    def find_path(self, start, goal, grid):
        q = {start}
        count = 0
        while True:
            grid = self.move_blizzards(grid)
            new_q = set()
            for (r, c) in q:
                if (r, c) == goal:
                    return count, grid
                for dr, dc in [(-1, 0), (1, 0), (0, 0), (0, 1), (0, -1)]:
                    nb = r + dr, c + dc
                    if len(grid.get(nb, [1])) == 0:
                        new_q.add(nb)
            count += 1
            q = new_q

    def main(self, grid):
        start = (0, 1)
        if grid[start]:
            grid[start].pop()
        maxr, maxc = self.dims
        goal = maxr, maxc - 1
        steps, grid = self.find_path(start, goal, grid)
        return steps


class PartTwo(PartOne):
    def main(self, grid):
        start = (0, 1)
        if grid[start]:
            grid[start].pop()
        maxr, maxc = self.dims
        goal = maxr, maxc - 1
        steps_to, grid = self.find_path(start, goal, grid)
        steps_back, grid = self.find_path(goal, start, grid)
        steps_to_2, grid = self.find_path(start, goal, grid)
        return steps_to + steps_back + steps_to_2 + 2


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 18

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 18 + 23 + 13
