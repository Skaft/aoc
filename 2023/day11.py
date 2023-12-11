from itertools import combinations


with open("inputs/day11.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")

class Universe:
    def __init__(self, raw_input):
        self.input_lines = lines = raw_input.splitlines()

        self.empty_rows = {i for i, col in enumerate(lines) if len(set(col)) == 1}
        self.empty_cols = {i for i, col in enumerate(zip(*lines)) if len(set(col)) == 1}

    def expand(self, padding):
        expanded_rows = 0
        galaxies = []

        for r, line in enumerate(self.input_lines):
            if r in self.empty_rows:
                expanded_rows += padding
                continue

            expanded_cols = 0
            for c, char in enumerate(line):
                if c in self.empty_cols:
                    expanded_cols += padding
                    continue

                if char == "#":
                    galaxies.append((r + expanded_rows, c + expanded_cols))
        
        return galaxies

    def sum_distances(self, expansion_rate=2):
        galaxies = self.expand(padding=expansion_rate - 1)
        total = 0
        for (r1, c1), (r2, c2) in combinations(galaxies, 2):
            dist = abs(r2 - r1) + abs(c2 - c1)
            total += dist
        return total


if __name__ == "__main__":

    print(Universe(true_input).sum_distances())
    print(Universe(true_input).sum_distances(expansion_rate=1_000_000))


# TESTS


def test_part1_main():
    assert Universe(test_inputs[0]).sum_distances() == 374


def test_part2_main():
    assert Universe(test_inputs[0]).sum_distances(expansion_rate=10) == 1030
    assert Universe(test_inputs[0]).sum_distances(expansion_rate=100) == 8410
