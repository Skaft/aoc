import re

import pytest

from helpers import AoCSolution


DAY = 4


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        pairs = []
        for line in raw_input.splitlines():
            numbers = re.split("[,-]", line)
            a, b, c, d = map(int, numbers)
            range_pair = ((a, b), (c, d))
            pairs.append(range_pair)
        return pairs

    def overlaps(self, pair):
        (a, b), (A, B) = pair

        if (A <= a <= B) and (A <= b <= B):
            return True
        if (a <= A <= b) and (a <= B <= b):
            return True

        return False

    def main(self, cleaned_input):
        total = 0
        for pair in cleaned_input:
            if self.overlaps(pair):
                total += 1

        return total


class PartTwo(PartOne):
    def overlaps(self, pair):
        (a, b), (A, B) = pair

        if (A <= a <= B) or (A <= b <= B):
            return True
        if (a <= A <= b) or (a <= B <= b):
            return True

        return False


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 2

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 4
