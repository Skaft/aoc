import re


class PartOne:
    pull_pattern = re.compile(r"(?:(\d+) (red|green|blue))")

    def __init__(self, raw_input):
        self.input_lines = raw_input.splitlines()

    def parse_line(self, line):
        return [(int(amt), color) for amt, color in self.pull_pattern.findall(line)]

    def main(self):
        id_totals = 0

        for game_id, line in enumerate(self.input_lines, 1):
            pulls = self.parse_line(line)
            max_red, max_green, max_blue = self.max_vals(pulls)
            game_valid = max_red <= 12 and max_green <= 13 and max_blue <= 14
            if game_valid:
                id_totals += game_id

        return id_totals

    def max_vals(self, pulls):

        red = max(amount for amount, color in pulls if color == "red")
        green = max(amount for amount, color in pulls if color == "green")
        blue = max(amount for amount, color in pulls if color == "blue")

        return red, green, blue


class PartTwo(PartOne):

    def main(self):
        power_sum = 0

        for line in self.input_lines:
            pulls = self.parse_line(line)
            red, green, blue = self.max_vals(pulls)
            power_sum += red * green * blue

        return power_sum


with open("inputs/day2.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 8

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 2286
