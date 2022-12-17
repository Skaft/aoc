from collections import Counter
import re

import pytest

from helpers import AoCSolution


DAY = 11


class Monkey:

    def __init__(self, items, expr, divby, target_true, target_false, monkeys):
        self.items = items
        self.operation = lambda old: eval(expr)
        self.divby = divby
        self.target_true = target_true
        self.target_false = target_false
        self.monkeys = monkeys
        monkeys.append(self)

    def take_turn(self):
        for item in self.items:
            worry = self.operation(item) // 3
            if worry % self.divby == 0:
                target = self.target_true
            else:
                target = self.target_false

            self.monkeys[target].items.append(worry)
        self.items.clear()


class PartOne(AoCSolution):
    def extract_monkey_data(self, raw_input):
        input_groups = [
            re.findall(r"Starting items: (.*)", raw_input),
            re.findall(r"Operation: new = (.*)", raw_input),
            re.findall(r"divisible by (\d+)", raw_input),
            re.findall(r"true: throw to monkey (\d+)", raw_input),
            re.findall(r"false: throw to monkey (\d+)", raw_input)
        ]

        data_groups = []
        for items, expr, divby, true, false in zip(*input_groups):
            items = [int(n) for n in items.split(", ")]
            data_groups.append(
                (items, expr, int(divby), int(true), int(false))
            )

        return data_groups

    def clean_input(self, raw_input):
        monkeys = []
        for data in self.extract_monkey_data(raw_input):
            Monkey(*data, monkeys)
        return monkeys

    def do_round(self, monkeys):
        inspections = []
        for monkey in monkeys:
            inspections.append(len(monkey.items))
            monkey.take_turn()
        return inspections

    def display_inventories(self, monkeys):
        lines = []
        for i, monkey in enumerate(monkeys):
            num_string = ", ".join(str(n) for n in monkey.items)
            lines.append(f"Monkey {i}: {num_string}")
        return "\n".join(lines)

    def main(self, monkeys):
        total_inspections = Counter()
        for _ in range(20):
            inspects = self.do_round(monkeys)
            for monkey, count in enumerate(inspects):
                total_inspections[monkey] += count
        a, b, *_ = sorted(total_inspections.values(), reverse=True)
        return a * b


class Monkey2(Monkey):
    def take_turn(self):
        for item in self.items:
            worry = self.operation(item)
            if worry % self.divby == 0:
                target = self.target_true
            else:
                target = self.target_false

            self.monkeys[target].items.append(worry)
        self.items.clear()

class PartTwo(PartOne):
    def clean_input(self, raw_input):
        monkeys = []
        for data in self.extract_monkey_data(raw_input):
            Monkey2(*data, monkeys)
        return monkeys

    def main(self, monkeys):
        total_inspections = Counter()
        for _ in range(1000):
            inspects = self.do_round(monkeys)
            for monkey, count in enumerate(inspects):
                total_inspections[monkey] += count
        a, b, *_ = sorted(total_inspections.values(), reverse=True)
        print(total_inspections)
        return a * b

if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    # print(PartTwo(DAY).run(0))


# TESTS

def test_part1_setup():
    sol = PartOne(DAY)
    monkeys = sol.clean_input(sol.raw_test_inputs[0])
    expected = [
        [79, 98],
        [54, 65, 75, 74],
        [79, 60, 97],
        [74]
    ]
    for monkey, exp in zip(monkeys, expected):
        assert monkey.items == exp

def test_part1_round():
    sol = PartOne(DAY)
    monkeys = sol.clean_input(sol.raw_test_inputs[0])
    sol.do_round(monkeys)
    expected = [
        [20, 23, 27, 26],
        [2080, 25, 167, 207, 401, 1046],
        [],
        []
    ]
    for monkey, exp in zip(monkeys, expected):
        assert monkey.items == exp

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 10605

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 2713310158