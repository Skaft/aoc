with open("inputs/day9.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:
    def __init__(self, raw_input):
        self.histories = []
        for line in raw_input.splitlines():
            self.histories.append([int(n) for n in line.split()])

    def generate_diffs(self, values):
        diff_lines = []
        while len(set(values)) > 1:
            values = [b - a for a, b in zip(values, values[1:])]
            diff_lines.append(values)
        return diff_lines

    def extrapolate(self, history, diff_lines):
        last_column = (line[-1] for line in diff_lines)
        return history[-1] + sum(last_column)

    def main(self):
        total = 0
        for history in self.histories:
            diff_lines = self.generate_diffs(history)
            total += self.extrapolate(history, diff_lines)
        return total


class PartTwo(PartOne):
    def extrapolate(self, history, diff_lines):
        first_column = (line[0] for line in diff_lines)
        column_diff = sum(diff * (-1) ** i for i, diff in enumerate(first_column))
        return history[0] - column_diff


if __name__ == "__main__":

    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS


def test_part1_main():
    assert PartOne(test_inputs[0]).main() == 114


def test_part2_main():
    assert PartTwo(test_inputs[0]).main() == 2
