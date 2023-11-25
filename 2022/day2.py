import pytest

from helpers import AoCSolution


DAY = 2


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        data = raw_input.split()
        opponent_list = data[::2]
        you_list = data[1::2]
        return (opponent_list, you_list)

    @staticmethod
    def score(opponent, you):
        shape_score = "_XYZ".index(you)
        beats = dict(zip("ZXYCAB", "ABCXYZ"))

        if opponent == beats[you]:
            outcome_score = 0
        elif you == beats[opponent]:
            outcome_score = 6
        else:
            outcome_score = 3

        return shape_score + outcome_score

    def main(self, opponent_list, you_list):
        games = zip(opponent_list, you_list)
        total = sum(self.score(opp, you) for opp, you in games)
        return total


class PartTwo(PartOne):
    @staticmethod
    def score(opponent, you):
        opp_index = "ABC".index(opponent)

        if you == "X":
            return 0 + (opp_index - 1) % 3 + 1
        elif you == "Y":
            return 3 + opp_index + 1
        else:
            return 6 + (opp_index + 1) % 3 + 1


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 15

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 12

@pytest.mark.parametrize("opp,you,expected", [("A", "Y", 2+6)])
def test_partone_score(opp, you, expected):
    assert PartOne.score(opp, you) == expected

@pytest.mark.parametrize("opp,you,expected", [("A", "Y", 1+3), ("B", "Z", 3+6), ("C", "X", 0+2)])
def test_parttwo_score(opp, you, expected):
    assert PartTwo.score(opp, you) == expected
