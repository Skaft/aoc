import re


with open("inputs/day3.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:

    def __init__(self, raw_input):
        self.symbols = self.locate_all(r"[^\d\.]", raw_input)
        self.part_numbers = self.locate_all(r"\d+", raw_input, int)


    @staticmethod
    def locate_all(pattern, string, conv_to=None):
        pattern = re.compile(pattern)

        matches = {}

        for line_num, line in enumerate(string.splitlines()):
            for match in pattern.finditer(line):
                value = match[0]

                if conv_to is not None:
                    value = conv_to(value)

                matches[line_num, match.start()] = value

        return matches


    @staticmethod
    def neighbors_of(pos, width=1):
        row, col = pos
        for dif_r in (-1, 0, 1):
            for dif_c in range(-1, width + 1):
                yield row + dif_r, col + dif_c

    def main(self):

        total = 0

        for position, part_num in self.part_numbers.items():
            neighbors = self.neighbors_of(position, width=len(str(part_num)))
            if any(neighbor in self.symbols for neighbor in neighbors):
                total += part_num

        return total


class Gear(str):

    def __init__(self, arg):
        super().__init__()
        self.part_numbers = []

    def ratio(self):
        assert len(self.part_numbers) == 2
        return self.part_numbers[0] * self.part_numbers[1]


class PartTwo(PartOne):
    def __init__(self, raw_input):
        self.gears = self.locate_all(r"\*", raw_input, Gear)
        self.part_numbers = self.locate_all(r"\d+", raw_input, int)

    def main(self):
        
        # connect gears to neighboring part numbers
        for position, part_num in self.part_numbers.items():
            neighbors = self.neighbors_of(position, width=len(str(part_num)))
            for pos in neighbors:
                if pos in self.gears:
                    gear: Gear = self.gears[pos]
                    gear.part_numbers.append(part_num)

        total = 0

        for gear in self.gears.values():
            if len(gear.part_numbers) == 2:
                total += gear.ratio()
        
        return total


if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 4361

def test_numbers_are_found_with_line_number():
    input_ = "..12.\n.4.23"
    output = PartOne.locate_all(r"\d+", input_, int)

    assert len(output) == 3
    exp = {
        (0, 2): 12,
        (1, 1): 4,
        (1, 3): 23,
    }
    assert output == exp

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 467835
