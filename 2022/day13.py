import pytest

from helpers import AoCSolution


DAY = 13


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        pairs = []
        for pair in raw_input.split("\n\n"):
            a, b = pair.splitlines()
            pairs.append((eval(a), eval(b)))
        return pairs

    def in_order(self, A, B):
        a_list = isinstance(A, list)
        b_list = isinstance(B, list)
        if not a_list and not b_list:
            if A < B:
                return True
            if A > B:
                return False
            return None
        if not a_list:
            return self.in_order([A], B)
        if not b_list:
            return self.in_order(A, [B])
        if A == B:
            return None
        for a, b in zip(A, B):
            if (res := self.in_order(a, b)) is not None:
                return res
        return len(A) < len(B)

    def main(self, pairs):
        total = 0
        for i, pair in enumerate(pairs, 1):
            if self.in_order(*pair):
                total += i
        return total

class PartTwo(PartOne):
    pass


# sol = PartOne(DAY)
# assert sol.run(1) == 13

if __name__ == "__main__":
    print(PartOne(DAY).run(0))  # 6283: too low
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
    ([[]], [[[]]], True),
    ([[1, 2, 3], 1], [[1, 2, 3], 2], True),
    ([[1, 2, 3], 2], [[1, 2, 3], 1], False),
    ([[1, 2], 2], [[1, 2, 3], 1], True),
    ([[1, 2, 3], 1], [[1, 2], 2], False),
    ([[1, 2, 1], 2], [[1, 2, 3], 1], True),
    ([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9], False)
    ]
)
def test_part1_inorder(a, b, expected):
    sol = PartOne(DAY)
    assert sol.in_order(a, b) == expected

# def test_part2_main():
#     sol = PartTwo(DAY)
#     assert sol.run(1) == ...