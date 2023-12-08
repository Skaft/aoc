import re
from itertools import cycle
import math


with open("inputs/day8.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:

    def __init__(self, raw_input):
        path, node_sections = raw_input.split("\n\n")
        self.path = path
        pattern = re.compile(r"(\w+) = \((\w+), (\w+)\)")
        self.network = {}
        for line in node_sections.splitlines():
            node, left, right = pattern.search(line).groups()
            self.network[node] = {
                "L": left,
                "R": right
            }

    def steps_to(self, start, *ends):
        node = start
        for step, direction in enumerate(cycle(self.path), 1):
            node = self.network[node][direction]
            if node in ends:
                return step

    def main(self):
        return self.steps_to("AAA", "ZZZ")


class PartTwo(PartOne):

    def main(self):
        starts = [node for node in self.network if node.endswith("A")]
        ends = [node for node in self.network if node.endswith("Z")]

        intervals = [self.steps_to(start, *ends) for start in starts]

        return math.lcm(*intervals)
            


if __name__ == "__main__":

    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())



# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 2
    assert PartOne(test_inputs[1]).main() == 6

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[2]).main() == 6
