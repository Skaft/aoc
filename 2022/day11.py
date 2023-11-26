import re
from functools import partial
from math import prod

import pytest

from helpers import AoCSolution


DAY = 11
PART_ONE = False

class Monkey:
    def __init__(self, index):
        self.index = index
        self.items = None
        self.operation = None
        self.divby = None
        self.true_target = None
        self.false_target = None
        self.inspections = 0
        self.inspection_pattern = []

    def take_turn(self):
        self.inspections += len(self.items)
        # self.inspection_pattern.append(len(self.items))
        for worry in self.items:
            self.operation(worry)

            if PART_ONE:
                worry //= 3

            if worry % self.divby == 0:
                target = self.true_target
            else:
                target = self.false_target

            target.items.append(worry)
            # worry.monkeys.append((self.index, worry % self.divby))
        self.items.clear()


class PartOne(AoCSolution):
    def set_items(self, monkey, items):
        monkey.items = items

    def clean_input(self, raw_input):
        input_blocks = raw_input.split("\n\n")
        monkeys = [Monkey(i) for i in range(len(input_blocks))]

        numbers = re.compile(r"\d+")

        for monkey, block in zip(monkeys, input_blocks):
            lines = iter(block.splitlines())
            # line 1: monkey id
            next(lines)
            self.set_items(monkey, [int(n) for n in numbers.findall(next(lines))])
            data_str = next(lines).split("=")[-1]

            if data_str.count("old") == 2:
                monkey.operation = partial(lambda a: a.__ipow__(2))
            elif "*" in data_str:
                value = int(numbers.findall(data_str)[0])
                monkey.operation = partial(lambda b, a: a.__imul__(b), value)
            else:
                value = int(numbers.findall(data_str)[0])
                monkey.operation = partial(lambda b, a: a.__iadd__(b), value)

            monkey.divby = int(numbers.findall(next(lines))[0])
            true_index = int(numbers.findall(next(lines))[0])
            false_index = int(numbers.findall(next(lines))[0])
            monkey.true_target = monkeys[true_index]
            monkey.false_target = monkeys[false_index]

        return monkeys

    def do_round(self, monkeys):
        for monkey in monkeys:
            monkey.take_turn()

    def main(self, monkeys):
        for _ in range(20):
            self.do_round(monkeys)

        inspections = sorted(monkey.inspections for monkey in monkeys)
        monkey_business = prod(inspections[-2:])

        return monkey_business

class Item:
    def __init__(self, worry):
        self.starting_level = worry
        self.worry_mods = {}
        

    def split_worry(self, divbys):
        for d in divbys:
            self.worry_mods[d] = self.starting_level % d

    def __iadd__(self, other):
        new_dict = {}
        while self.worry_mods:
            k, v = self.worry_mods.popitem()
            new_dict[k] = (v + other) % k
        self.worry_mods = new_dict
        return self

    def __imul__(self, other):
        new_dict = {}
        while self.worry_mods:
            k, v = self.worry_mods.popitem()
            new_dict[k] = (v * other) % k
        self.worry_mods = new_dict
        return self
    
    def __ipow__(self, other):
        new_dict = {}
        while self.worry_mods:
            k, v = self.worry_mods.popitem()
            new_dict[k] = (v ** other) % k
        self.worry_mods = new_dict
        return self

    def __mod__(self, other):
        return self.worry_mods[other]


class PartTwo(PartOne):
    def clean_input(self, raw_input):
        monkeys = super().clean_input(raw_input)

        divbys = {m.divby for m in monkeys}
        for m in monkeys:
            for item in m.items:
                item.split_worry(divbys)
        return monkeys

    def set_items(self, monkey, items):
        monkey.items = [Item(n) for n in items]

    def main(self, monkeys):

        for _ in range(10_000):
            self.do_round(monkeys)
        
        inspections = sorted(monkey.inspections for monkey in monkeys)
        monkey_business = prod(inspections[-2:])

        return monkey_business


if __name__ == "__main__":
    if PART_ONE:
        print(PartOne(DAY).run(0))
    else:
        print(PartTwo(DAY).run(0))


# TESTS

@pytest.mark.skipif(not PART_ONE)
def test_part1_one_round():
    sol = PartOne(DAY)
    monkeys = sol.test_inputs[0]
    sol.do_round(monkeys)
    
    assert monkeys[0].items == [20, 23, 27, 26]
    assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]
    assert monkeys[2].items == []
    assert monkeys[3].items == []

@pytest.mark.skipif(not PART_ONE)
def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 10605

@pytest.mark.skipif(PART_ONE, reason="")
def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 2713310158

@pytest.mark.skipif(PART_ONE, reason="")
@pytest.mark.parametrize("rounds,expected", [
    (1, [2, 4, 3, 6]),
    (20, [99, 97, 8, 103]),
    (1000, [5204, 4792, 199, 5192]),
    ])
def test_part2_inspections(rounds, expected):
    sol = PartTwo(DAY)
    monkeys = sol.test_inputs[0]
    for _ in range(rounds):
        sol.do_round(monkeys)
    inspections = [m.inspections for m in monkeys]
    assert inspections == expected
