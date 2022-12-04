from string import ascii_letters

import pytest

from helpers import AoCSolution


DAY = 3

class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        return raw_input.split()

    def find_common_item(self, rucksack):
        middle = len(rucksack) // 2
        half1, half2 = rucksack[:middle], rucksack[middle:]
        common_item = set(half1).intersection(half2)
        assert len(common_item) == 1
        return common_item.pop()

    @staticmethod
    def priority(item):
        return ascii_letters.index(item) + 1

    def main(self, rucksacks):
        prio_sum = 0

        for rucksack in rucksacks:
            item = self.find_common_item(rucksack)
            prio_sum += self.priority(item)

        return prio_sum


class PartTwo(PartOne):
    def clean_input(self, raw_input):
        rucksacks = raw_input.split()

        groups = []
        for i in range(0, len(rucksacks), 3):
            group = rucksacks[i: i+3]
            groups.append(group)

        return groups

    def find_common_item(self, group):
        a, b, c = group
        common = set(a).intersection(b).intersection(c)
        assert len(common) == 1
        return common.pop()


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# Tests:

@pytest.mark.parametrize("item,expected", [
    ("a", 1), ("z", 26), ("A", 27), ("Z", 52)
])
def test_priority(item, expected):
    assert PartOne.priority(item) == expected

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 157

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 70
