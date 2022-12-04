import pytest

from helpers import AoCSolution


DAY = 1


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        group_list = [[]]
        for line in raw_input.splitlines():
            if not line:
                group_list.append([])
            else:
                group_list[-1].append(int(line))
        return group_list

    def main(self, group_list):
        calory_sums = [sum(group) for group in group_list]
        return max(calory_sums)


class PartTwo(PartOne):
    def main(self, group_list):
        calory_sums = [sum(group) for group in group_list]
        calory_sums.sort()
        return sum(calory_sums[-3:])


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 24000

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 45000
