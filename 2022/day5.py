import re

import pytest

from helpers import AoCSolution


DAY = 5


class PartOne(AoCSolution):
    def parse_stacks(self, stack_lines):
        num_stacks = len(stack_lines[0][1::4])
        stacks = [[] for _ in range(num_stacks)]

        for line in reversed(stack_lines):
            letters = line[1::4]
            for stack, letter in zip(stacks, letters):
                if letter != " ":
                    stack.append(letter)
        
        return stacks

    def parse_moves(self, move_lines):
        pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
        moves = []
        for line in move_lines:
            numbers = pattern.search(line)
            move = tuple(int(n) for n in numbers.groups())
            moves.append(move)
        return moves

    def clean_input(self, raw_input):
        raw_state, raw_moves = raw_input.split("\n\n")
        *stack_lines, number_line = raw_state.splitlines()
        move_lines = raw_moves.splitlines()
        stacks = self.parse_stacks(stack_lines)
        moves = self.parse_moves(move_lines)
        return stacks, moves

    def make_move(self, move, stacks):
        amount, fro, to = move
        for _ in range(amount):
            letter = stacks[fro - 1].pop()
            stacks[to - 1].append(letter)

    def main(self, stacks, moves):
        for move in moves:
            self.make_move(move, stacks)
        top_row = [stack[-1] for stack in stacks if stack != []]
        return "".join(top_row)


class PartTwo(PartOne):
    def make_move(self, move, stacks):
        amount, fro, to = move
        pile = stacks[fro - 1][-amount:]
        stacks[to - 1].extend(pile)
        stacks[fro - 1][-amount:] = []


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == "CMZ"

def test_clean_input():
    sol = PartOne(DAY)
    exp_stacks = [list("ZN"), list("MCD"), ["P"]]
    exp_moves = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]
    assert sol.clean_input(sol.raw_test_inputs[0]) == (exp_stacks, exp_moves)

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == "MCD"