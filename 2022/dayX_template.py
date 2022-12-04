import pytest

from helpers import AoCSolution


DAY = ...


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        pass

    def main(self, cleaned_input):
        pass


class PartTwo(PartOne):
    pass


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == ...

# def test_part2_main():
#     sol = PartTwo(DAY)
#     assert sol.run(1) == ...