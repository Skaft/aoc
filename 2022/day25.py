from collections import defaultdict

import pytest

from helpers import AoCSolution


DAY = 25


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        snafu_ints = []
        str_to_int = {
            "2": 2,
            "1": 1,
            "0": 0,
            "-": -1,
            "=": -2
        }
        for snafu_str in raw_input.splitlines():
            num = [str_to_int[d] for d in snafu_str]
            snafu_ints.append(num)
        return snafu_ints

    def power_dict_to_dec(self, dct):
        total = 0
        for power, value in dct.items():
            total += value * 5 ** power
        return total

    def power_dict_to_snafu(self, dct):
        chars = []
        for power, value in sorted(dct.items(), reverse=True):
            if value == -2:
                chars.append("=")
            elif value == -1:
                chars.append("-")
            elif 0 <= value <= 2:
                chars.append(str(value))
            else:
                raise ValueError("Invalid digit:", value)
        return "".join(chars)

    def simplify(self, dct):
        changes = defaultdict(int)
        for power, value in dct.items():
            if -2 <= value <= 2:
                continue
            full, rem = divmod(value, 5)
            if full:
                changes[power + 1] += full
                dct[power] = rem
            if rem > 2:
                changes[power + 1] += 1
                dct[power] -= 5
        if changes:
            for power, val in changes.items():
                dct[power] += val
            return self.simplify(dct)
        return dct

    def main(self, snafu_ints):
        digit_counts = defaultdict(int)
        for snafu in snafu_ints:
            for power, value in enumerate(reversed(snafu)):
                digit_counts[power] += value
        reduced = self.simplify(digit_counts)
        return self.power_dict_to_snafu(reduced)


class PartTwo(PartOne):
    pass


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
#     print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == "2=-1=0"
