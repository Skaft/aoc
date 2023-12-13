
with open("inputs/day13.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:

    def __init__(self, raw_input):
        self.patterns = raw_input.split("\n\n")

    def find_mirror_indexes(self, pattern, dim="rows"):
        indexes = []
        lines = pattern.splitlines()
        if dim == "cols":
            lines = list(zip(*lines))

        for i in range(1, len(lines)):
            above = reversed(lines[:i])
            below = lines[i:]
            if all(a == b for a, b in zip(above, below)):
                indexes.append(i)
        return indexes

    def main(self):
        total = 0

        for pattern in self.patterns:
            row_indexes = self.find_mirror_indexes(pattern, "rows")
            column_indexes = self.find_mirror_indexes(pattern, "cols")
            total += 100 * sum(row_indexes) + sum(column_indexes)

        return total


class PartTwo(PartOne):

    def find_mirror_indexes(self, pattern, dim="rows"):
        indexes = []
        lines = pattern.splitlines()
        if dim == "cols":
            lines = list(zip(*lines))

        for i in range(1, len(lines)):
            above = reversed(lines[:i])
            below = lines[i:]
            diffs = 0
            for a, b in zip(above, below):
                for c1, c2 in zip(a, b):
                    if c1 != c2:
                        diffs += 1
                        if diffs > 1:
                            break
            if diffs == 1:
                indexes.append(i)
        return indexes


if __name__ == "__main__":

    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_part1_mirror_rows():
    pattern2 = test_inputs[0].split("\n\n")[1]
    assert PartOne("").find_mirror_indexes(pattern2, "rows") == [4]

def test_part1_main():
    assert PartOne(test_inputs[0]).main() == 405

def test_part2_main():
    assert PartTwo(test_inputs[0]).main() == 400

