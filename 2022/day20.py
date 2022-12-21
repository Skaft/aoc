from collections import deque

import pytest

from helpers import AoCSolution


DAY = 20


class Number:
    """Wrapper for numbers to give them ID's, distinguishing between different instances of equal numbers"""
    def __init__(self, n):
        self.value = int(n)


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        numbers = [Number(n) for n in raw_input.splitlines()]
        return numbers

    def move_number(self, num_deque, n):
        i = num_deque.index(n)

        # take number out
        num_deque.rotate(-i)
        num_deque.popleft()

        # put back n steps away
        num_deque.rotate(-n.value)
        num_deque.appendleft(n)

    def mix_once(self, numbers, order=None):
        mixed = deque(numbers)
        if order is None:
            order = numbers
        for n in order:
            self.move_number(mixed, n)
        return list(mixed)

    def get_indicators(self, numbers):
        for i, n in enumerate(numbers):
            if n.value == 0:
                zero = i
                break
        indicators = []
        for i in (1000, 2000, 3000):
            n = numbers[(zero + i) % len(numbers)]
            indicators.append(n.value)
        return indicators

    def main(self, numbers):
        numbers = self.mix_once(numbers)
        return sum(self.get_indicators(numbers))


class PartTwo(PartOne):
    key = 811589153

    def main(self, numbers):
        for n in numbers:
            n.value *= PartTwo.key
        order = numbers.copy()
        for _ in range(10):
            numbers = self.mix_once(numbers, order=order)
        return sum(self.get_indicators(numbers))
        

if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 3

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 1623178306