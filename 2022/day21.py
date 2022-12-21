from operator import add, sub, mul, truediv

import pytest

from helpers import AoCSolution


DAY = 21


class Monkey:
    ops = {
        "/": truediv,
        "+": add,
        "-": sub,
        "*": mul,
    }
    def __init__(self, name, instruction, monkeys):
        self.name = name
        self.instruction = self.parse_instruction(instruction)
        self.monkeys = monkeys
    
    def parse_instruction(self, instr):
        if instr.isdigit():
            self.value = int(instr)
            return "value"
        a, op, b = instr.split()
        self.inputs = a, b
        self.op = self.ops[op]
        return "call"

    def output(self):
        if self.instruction == "value":
            return self.value

        a = self.monkeys[self.inputs[0]]
        b = self.monkeys[self.inputs[1]]

        return self.op(a.output(), b.output())

class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        monkeys = {}
        for line in raw_input.splitlines():
            name, instruction = line.split(": ")
            monkeys[name] = Monkey(name, instruction, monkeys)
        return monkeys

    def main(self, monkeys):
        return int(monkeys["root"].output())


class PartTwo(PartOne):
    def try_run(self, monkeys, humn_val):
        monkeys["humn"].value = humn_val
        a, b = monkeys["root"].inputs
        return monkeys[a].output() - monkeys[b].output()

    def main(self, monkeys):
        left_high = self.try_run(monkeys, 1) > self.try_run(monkeys, 10 ** 16)
        left, right = 1, 10**16
        while True:
            mid = (left + right) // 2
            res = self.try_run(monkeys, mid)
            if res == 0:
                return mid
            if (left_high and res > 0) or (not left_high and res < 0):
                left = mid
            else:
                right = mid


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 152

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 301

def test_part2_unique():
    sol = PartTwo(DAY)
    monkeys = sol.clean_input(sol.raw_true_input)
    res = sol.main(monkeys)
    results = [sol.try_run(monkeys, val) for val in range(res-10, res+11)]
    assert results.count(0) == 1
