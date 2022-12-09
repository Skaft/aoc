import re
from collections import Counter

import pytest

from helpers import AoCSolution


DAY = 7


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        return raw_input.splitlines()

    def calc_dir_sizes(self, lines):
        cwd = []
        dir_sizes = Counter()
        dirnames = []
        for line in lines:
            if line.startswith("$ cd"):
                _, target = line.rsplit(" ", maxsplit=1)
                if target == "/":
                    cwd.append("/")
                elif target == "..":
                    cwd.pop()
                else:
                    cwd.append(target)
            elif line.startswith("$ ls"):
                pass
            elif line.startswith("dir"):
                _, dirname = line.split()
                dirnames.append(dirname)
            else:
                size, filename = line.split()
                for i in range(1, len(cwd)+1):
                    dir_sizes["/".join(cwd[:i])] += int(size)
        return dir_sizes

    def main(self, lines):
        dir_sizes = self.calc_dir_sizes(lines)
        total = sum(size for size in dir_sizes.values() if size <= 100000)
        return total


class PartTwo(PartOne):
    def main(self, lines):
        dir_sizes = self.calc_dir_sizes(lines)
        used_space = dir_sizes["/"]
        surplus = used_space - 40_000_000
        smallest = min(size for size in dir_sizes.values() if size >= surplus)
        return smallest


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 95437

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 24933642