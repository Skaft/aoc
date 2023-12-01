import re


class PartOne:
    """
    For each line in input,
        extract all digits,
        concatenate first and last,
        cast to int and add it to total.
    """
    number_pattern = re.compile(r"\d")

    def __init__(self, raw_input):
        self.input_lines = raw_input.splitlines()

    def main(self):
        calibration_sum = 0
        for line in self.input_lines:
            digits = self.extract_digits(line)
            calibration_sum += int(digits[0] + digits[-1])
        return calibration_sum

    def extract_digits(self, line):
        return self.number_pattern.findall(line)


class PartTwo(PartOne):
    """
    Same process as PartOne, but with a more complicated regex to allow
    word matches, and then a conversion step to translate word matches
    to digits, so that the same main method can be used.
    """
    num_words = "one|two|three|four|five|six|seven|eight|nine"

    # regex lookahead to avoid consuming matches, permitting word overlaps
    number_pattern = re.compile(rf"(?=(\d|{num_words}))")

    def extract_digits(self, line):
        word_to_digit = dict(zip(self.num_words.split("|"), "123456789"))

        matches = self.number_pattern.findall(line)
        return [word_to_digit.get(num, num) for num in matches]


with open("inputs/day1.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 142

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[1]).main() == 281

def test_part2_handles_overlapping_words():
    assert PartTwo("2abcdoneight").main() == 28
