import pytest

from helpers import AoCSolution

import re

DAY = 22


class PartOne(AoCSolution):
    dirs = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    def clean_input(self, raw_input):
        grid_input, moves_input = raw_input.rsplit("\n\n", maxsplit=1)
        grid = self.parse_grid(grid_input)
        moves = self.parse_moves(moves_input)
        return grid, moves

    def parse_grid(self, grid_input):
        grid = {}
        rows = grid_input.splitlines()
        for r, row in enumerate(rows, 1):
            for c, val in enumerate(row, 1):
                if val not in "#.":
                    continue
                grid[r, c] = val
        return grid

    @staticmethod
    def parse_moves(moves_input):
        pattern = r"(\d+|\w)"
        raw_moves = re.findall(pattern, moves_input)
        moves = [int(m) if m.isdigit() else m for m in raw_moves]
        return moves

    @staticmethod
    def password(row, col, facing):
        facing_score = ">v<^".index(facing)
        return 1000 * row + 4 * col + facing_score

    @staticmethod
    def turn(facing, turn_dir):
        dirs = ">v<^"
        i = dirs.index(facing)
        if turn_dir == "R":
            i = (i + 1) % 4
        else:
            i = (i - 1) % 4
        return dirs[i]

    @staticmethod
    def wrap_around(pos, facing, grid):
        dirs = ">v<^"
        i = dirs.index(facing)
        opposite = dirs[(i + 2) % 4]
        dr, dc = PartOne.dirs[opposite]
        r, c = pos
        while True:
            nb = r + dr, c + dc
            if nb not in grid:
                return (r, c), facing
            r, c = nb

    def walk(self, pos, facing, steps, grid):
        dr, dc = PartOne.dirs[facing]
        for _ in range(steps):
            r, c = pos
            nb = r + dr, c + dc
            if nb not in grid:
                nb, facing = self.wrap_around(pos, facing, grid)
            if grid[nb] == "#":
                break
            pos = nb
            grid[pos] = facing

        return pos, facing

    def main(self, grid, moves):
        pos = min(grid.keys())
        facing = ">"
        grid[pos] = facing

        for move in moves:
            if isinstance(move, str):
                facing = self.turn(facing, move)
                grid[pos] = facing
            else:
                pos, facing = self.walk(pos, facing, move, grid)

        return self.password(*pos, facing)


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    # print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 6032

def test_part1_password():
    assert PartOne.password(6, 8, ">") == 6032

def test_part1_turn():
    assert PartOne.turn("^", "R") == ">"
    assert PartOne.turn("^", "L") == "<"
    assert PartOne.turn("<", "R") == "^"
    assert PartOne.turn("<", "L") == "v"

def test_part1_moves():
    inpt = "10R5L5R10L4R5L5"
    exp = [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]
    assert PartOne.parse_moves(inpt) == exp

@pytest.mark.skip
def test_part2_cubewrap():
    sol = PartTwo(DAY)
    grid, _ = sol.clean_input(sol.raw_test_inputs[0])
    A = 6, 12
    B = 9, 15
    C = 12, 11
    D = 8, 2
    assert PartTwo.wrap_around(A, ">", grid) == (B, "v")
    assert PartTwo.wrap_around(B, "^", grid) == (A, "<")
    assert PartTwo.wrap_around(C, "v", grid) == (D, "^")
    assert PartTwo.wrap_around(D, "v", grid) == (C, "^")

# def test_part2_main():
#     sol = PartTwo(DAY)
#     assert sol.run(1) == ...