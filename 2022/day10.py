from functools import partial

import pytest

from helpers import AoCSolution


DAY = 10


class CPU:
    def __init__(self):
        self.value = 1
        self.blocked = 0

    def addx(self, val):
        self.value += val

    def tick(self):
        if self.blocked:
            self.blocked -= 1
            if self.blocked == 0:
                self.stored_instr()

    def exec(self, line):
        if line == "noop":
            self.blocked = 1
            self.stored_instr = lambda: None
        elif line.startswith("addx"):
            _, addnum = line.split()
            self.blocked = 2
            self.stored_instr = partial(self.addx, int(addnum))
        else:
            raise ValueError("unknown instruction:", line)


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        return iter(raw_input.splitlines())

    def main(self, instructions):
        cpu = CPU()
        checkpoints = [20, 60, 100, 140, 180, 220]

        strength_sum = 0
        for cycle in range(1, 221):
            if not cpu.blocked:
                cpu.exec(next(instructions))
            if cycle in checkpoints:
                strength_sum += cycle * cpu.value
            cpu.tick()

        return strength_sum


class CRT:
    def __init__(self):
        self.pos = 0
        self.array = ["."] * 240

    def draw_pixel(self, char="#"):
        self.array[self.pos] = char

    def display(self):
        rows = []
        for i in range(0, 240, 40):
            rows.append("".join(self.array[i:i+40]))
        return "\n".join(rows)

    def tick(self):
        self.pos = self.pos + 1


class PartTwo(PartOne):
    def main(self, instructions):
        cpu = CPU()
        crt = CRT()

        for cycle in range(1, 241):
            if not cpu.blocked:
                cpu.exec(next(instructions))
            if abs(cpu.value - crt.pos % 40) <= 1:
                crt.draw_pixel()

            crt.tick()
            cpu.tick()

        return crt.display()


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 13140

def test_part2_main():
    import textwrap
    expected = textwrap.dedent("""
        ##..##..##..##..##..##..##..##..##..##..
        ###...###...###...###...###...###...###.
        ####....####....####....####....####....
        #####.....#####.....#####.....#####.....
        ######......######......######......####
        #######.......#######.......#######.....
        """).strip()
    sol = PartTwo(DAY)
    output = sol.run(1)
    assert output == expected
