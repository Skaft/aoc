import pytest

from helpers import AoCSolution


DAY = 24


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        grid = {}
        rows = raw_input.splitlines()
        for r, row in enumerate(rows, -1):
            for c, item in enumerate(row, -1):
                if item in ".E":
                    grid[r, c] = []
                elif item in "<>^v":
                    grid[r, c] = [item]
        self.dims = r, c
        return grid

    def display(self, grid):
        maxr, maxc = self.dims
        rows = [["."] * (maxc + 2) for _ in range(maxr + 2)]

        for r in range(maxr + 2):
            rows[r][0] = "#"
            rows[r][maxc + 1] = "#"
        for c in range(2, maxc + 1):
            rows[0][c] = "#"
        for c in range(1, maxc):
            rows[maxr + 1][c] = "#"

        for (r, c), items in grid.items():
            if len(items) == 1:
                rows[r + 1][c + 1] = items[0]
            elif len(items) > 1:
                rows[r + 1][c + 1] = str(len(items))
        rows = ["".join(row) for row in rows]
        return "\n".join(rows)

    def move_blizzards(self, grid):
        maxr, maxc = self.dims
        next_grid = {
            (r, c): []
            for r in range(maxr)
            for c in range(maxc)
        }
        next_grid[-1, 0] = []
        next_grid[maxr, maxc - 1] = []

        dirs = {
            ">": (0, 1),
            "<": (0, -1),
            "v": (1, 0),
            "^": (-1, 0),
        }

        for (r, c), items in grid.items():
            for item in items:
                dr, dc = dirs[item]
                r2 = (r + dr) % maxr
                c2 = (c + dc) % maxc
                next_grid[r2, c2].append(item)

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
        start = (-1, 0)
        maxr, maxc = self.dims
        goal = maxr, maxc - 1
        steps, grid = self.find_path(start, goal, grid)
        return steps


class PartTwo(PartOne):
    def main(self, grid):
        start = (-1, 0)
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

def test_display():
    sol = PartOne(DAY)
    raw_grid = sol.raw_test_inputs[0]
    grid = sol.clean_input(raw_grid)
    display = sol.display(grid)
    assert display == raw_grid

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 18 + 23 + 13
