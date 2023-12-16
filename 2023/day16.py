import re
from dataclasses import dataclass

with open("inputs/day16.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:
    dirs = {
        "N": (-1, 0),
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
    }

    def __init__(self, raw_input):
        self.grid = {}
        for r, line in enumerate(raw_input.splitlines()):
            for c, char in enumerate(line):
                if char == ".":
                    continue
                if char == "/":
                    fro_ = "NWSE"
                    to = "ESWN"
                elif char == "\\":
                    fro_ = "NWSE"
                    to = "WNES"
                elif char == "-":
                    fro_ = "NS"
                    to = ("EW", "EW")
                elif char == "|":
                    fro_ = "EW"
                    to = ("NS", "NS")
                else:
                    raise ValueError(char)
                self.grid[r, c] = dict(zip(fro_, to))
        self.width = c + 1
        self.height = r + 1

    def count_energized(self, start_r, start_c, dir):
        def step(r, c, dir):
            dr, dc = self.dirs[dir]
            return r + dr, c + dc

        visited = set()
        q = [(start_r, start_c, dir)]
        while q:
            pos_w_dir = q.pop()

            # cycle
            if pos_w_dir in visited:
                continue
            visited.add(pos_w_dir)

            r, c, dir = pos_w_dir
            rotate = self.grid.get((r, c), {})
            newdirs = rotate.get(dir, dir)
            for next_dir in newdirs:
                next_r, next_c = step(r, c, next_dir)
                if (0 <= next_r < self.height) and (0 <= next_c < self.width):
                    q.append((next_r, next_c, next_dir))

        energized = set((r, c) for r, c, _ in visited)
        return len(energized)

    def main(self):
        return self.count_energized(0, 0, "E")
    
    def draw(self, cells):
        lines = [["."] * self.width for _ in range(self.height)]
        for r, c in cells:
            lines[r][c] = "#"
        for line in lines:
            print("".join(line))


class PartTwo(PartOne):

    def main(self):
        entries = []
        entries.extend([(0, c, "S") for c in range(self.width)])
        entries.extend([(r, 0, "E") for r in range(self.height)])
        entries.extend([(r, self.width - 1, "W") for r in range(self.height)])
        entries.extend([(self.height - 1, c, "N") for c in range(self.width)])

        return max(self.count_energized(r, c, dir) for r, c, dir in entries)

if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 46

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 51
