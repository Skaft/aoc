import re
from math import sqrt, floor, ceil


with open("inputs/day6.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:

    def __init__(self, raw_input):
        times, distances = raw_input.splitlines()
        self.times = [int(n) for n in re.findall(r"\d+", times)]
        self.distances = [int(n) for n in re.findall(r"\d+", distances)]

    def main(self):
        """
        Solving for s: s * (time - s) > distance
        Rearranging to: s**2 - s*time + distance < 0

        Solving with quadratic equation, then floor-ing/ceil-ing the roots
        to fulfill the inequality.
        """

        prod = 1

        for time, distance in zip(self.times, self.distances):

            a = time / 2
            b = sqrt(a**2 - distance)
            above_min = floor(1 + a - b)
            below_max = ceil(-1 + a + b)

            prod *= below_max - above_min + 1
        
        return prod


class PartTwo(PartOne):
    def __init__(self, raw_input):
        times, distances = raw_input.splitlines()
        self.times = [int("".join(re.findall(r"\d+", times)))]
        self.distances = [int("".join(re.findall(r"\d+", distances)))]


if __name__ == "__main__":

    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())



# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 288

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 71503
