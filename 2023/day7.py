from collections import Counter


with open("inputs/day7.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class Hand:

    def __init__(self, cards, bid, joker=None):
        self.joker = joker
        self.type = self._determine_type(cards)
        self.cards = cards
        self.bid = bid

    def _determine_type(self, hand_str):
        counts = Counter(hand_str)

        # if there are jokers, turn them into the most common non-joker card
        if self.joker and self.joker in counts:
            num_jokers = counts.pop(self.joker)
            if num_jokers == 5:
                return 6
            popular_card, _ = counts.most_common(1)[0]
            counts[popular_card] += num_jokers

        uniques = len(counts)
        most_repeats = max(counts.values())

        if uniques == 5:  # high card
            type = 0
        elif uniques == 4:  # pair
            type = 1
        elif uniques == 3 and most_repeats == 2:  # two pair
            type = 2
        elif uniques == 3 and most_repeats == 3:  # three of a kind
            type = 3
        elif uniques == 2 and most_repeats == 3:  # full house
            type = 4
        elif uniques == 2 and most_repeats == 4:  # four of a kind
            type = 5
        elif uniques == 1:  # five of a kind
            type = 6
        else:
            raise AssertionError(f"Couldn't determine hand type: {hand_str}")
        return type

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        return self.cards < other.cards


class PartOne:
    card_conversion_table = str.maketrans("23456789TJQKA", "abcdefghijklm")
    joker = None

    def __init__(self, raw_input):
        self.hands = []
        for line in raw_input.splitlines():
            hand_str, bid_str = line.split()
            bid = int(bid_str)
            cards = hand_str.translate(self.card_conversion_table)
            hand = Hand(cards, bid, joker=self.joker)
            self.hands.append(hand)

    def main(self):
        winnings = 0
        for rank, hand in enumerate(sorted(self.hands), 1):
            winnings += hand.bid * rank
        return winnings


class PartTwo(PartOne):
    card_conversion_table = str.maketrans("J23456789TQKA", "abcdefghijklm")
    joker = "a"  # because I translate to J to a, might need to unuglify


if __name__ == "__main__":

    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())



# TESTS

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 6440

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 5905
