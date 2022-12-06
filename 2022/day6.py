from collections import deque

import pytest

from helpers import AoCSolution



DAY = 6


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        return raw_input.strip()

    def steps_to_n_unique(self, string, n):
        window = deque([], maxlen=n)
        for step, letter in enumerate(string, 1):
            window.append(letter)
            if len(set(window)) == n:
                return step

    def main(self, cleaned_input):
        return self.steps_to_n_unique(cleaned_input, 4)


class PartTwo(PartOne):
    def main(self, cleaned_input):
        return self.steps_to_n_unique(cleaned_input, 14)


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS
@pytest.mark.parametrize("test_nr,expected",
    [(1, 7), (2, 5), (3, 6), (4, 10), (5, 11)]
)
def test_part1_main(test_nr, expected):
    sol = PartOne(DAY)
    assert sol.run(test_nr) == expected

@pytest.mark.parametrize("test_nr,expected",
    [(1, 19), (2, 23), (3, 23), (4, 29), (5, 26)]
)
def test_part2_main(test_nr, expected):
    sol = PartTwo(DAY)
    assert sol.run(test_nr) == expected
