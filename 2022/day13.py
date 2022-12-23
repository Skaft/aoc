from enum import IntEnum

import pytest

from helpers import AoCSolution


DAY = 13


class Ordered(IntEnum):
    FALSE = 0
    TRUE = 1
    INDECISIVE = 2


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        pairs = []
        for pair in raw_input.split("\n\n"):
            a, b = pair.splitlines()
            pairs.append((eval(a), eval(b)))
        return pairs

    def in_order(self, A, B):
        if not isinstance(A, list):
            return self.in_order([A], B)
        if not isinstance(B, list):
            return self.in_order(A, [B])

        for a, b in zip(A, B):
            if isinstance(a, list) or isinstance(b, list):
                item_order = self.in_order(a, b)
            elif a == b:
                item_order = Ordered.INDECISIVE
            elif a < b:
                item_order = Ordered.TRUE
            else:
                item_order = Ordered.FALSE
            if item_order != Ordered.INDECISIVE:
                return item_order

        if len(A) == len(B):
            return Ordered.INDECISIVE
        elif len(A) < len(B):
            return Ordered.TRUE
        else:
            return Ordered.FALSE

    def main(self, pairs):
        total = 0
        for i, pair in enumerate(pairs, 1):
            if self.in_order(*pair) == Ordered.TRUE:
                total += i
        return total


class PartTwo(PartOne):
    pass


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 13

@pytest.mark.parametrize("a,b,expected", [
    ([1,1,3,1,1],[1,1,5,1,1], True),
    ([[1],[2,3,4]], [[1],4], True),
    ([9], [[8,7,6]], False),
    ([[4,4],4,4], [[4,4],4,4,4], True),
    ([7,7,7,7], [7,7,7], False),
    ([], [3], True),
    ([[[]]], [[]], False),
    ([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9], False),
    ([[]], [[[]]], True),
    ([[1, 2, 3], 1], [[1, 2, 3], 2], True),
    ([[1, 2, 3], 2], [[1, 2, 3], 1], False),
    ([[1, 2], 2], [[1, 2, 3], 1], True),
    ([[1, 2, 3], 1], [[1, 2], 2], False),
    ([[1, 2, 1], 2], [[1, 2, 3], 1], True),
    ]
)
def test_part1_inorder(a, b, expected):
    sol = PartOne(DAY)
    assert sol.in_order(a, b) == expected


# def test_part2_main():
#     sol = PartTwo(DAY)
#     assert sol.run(1) == ...