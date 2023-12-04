import numpy as np


with open("inputs/day4.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:

    def __init__(self, raw_input):
        cards = []
        for line in raw_input.splitlines():
            _, numbers = line.split(":")
            winning, held = numbers.split("|")
            winning = [int(n) for n in winning.split()]
            held = [int(n) for n in held.split()]
            cards.append((winning, held))
        self.cards = cards


    def main(self):

        total = 0

        for winning, held in self.cards:
            matches = len(set(winning).intersection(held))
            if matches:
                total += 2 ** (matches - 1)

        return total


class PartTwo(PartOne):

    def main(self):

        counts = np.ones(len(self.cards))

        for card_num, (winning, held) in enumerate(self.cards):
            matches = len(set(winning).intersection(held))
            if matches:
                counts[card_num + 1: card_num + 1 + matches] += counts[card_num]

        return counts.sum()


if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 13

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 30
