import pytest

from helpers import AoCSolution


DAY = 8


W = (0, -1)
E = (0, 1)
N = (-1, 0)
S = (1, 0)

class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        grid = {}
        self.checked = set()

        for r, row in enumerate(raw_input.splitlines()):
            for c, height in enumerate(row):
                grid[int(r), int(c)] = int(height)
        self.max_row = r
        self.max_col = c
        return grid

    def is_visible_from(self, pos, direction, height_grid):
        dr, dc = direction
        cell_height = height_grid[pos]
        r, c = pos
        while True:
            neighbor = r + dr, c + dc
            if neighbor not in height_grid:
                return True
            if cell_height <= height_grid[neighbor]:
                return False
            r, c = neighbor

    def main(self, grid):
        dirs = [N, E, S, W]
        count = 0
        for pos in grid:
            if any(self.is_visible_from(pos, dir, grid) for dir in dirs):
                count += 1
        return count


class PartTwo(PartOne):
    def scenic_score(self, pos, grid):
        score = 1
        stop_height = grid[pos]
        for direction in [N, E, S, W]:
            neighbors = self.generate_neighbors(pos, direction)
            steps = 0
            for steps, nb in enumerate(neighbors, 1):
                if grid[nb] >= stop_height:
                    break
            if steps == 0:
                return 0
            score *= steps
        return score

    def generate_neighbors(self, pos, dir):
        r, c = pos
        dr, dc = dir
        while True:
            r, c = r + dr, c + dc
            if (0 <= r <= self.max_row) and (0 <= c <= self.max_col):
                yield r, c
            else:
                break

    def main(self, grid):
        best = -1
        for pos in grid:
            score = self.scenic_score(pos, grid)
            if score > best:
                best = score
        return best


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS
def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 21

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 8