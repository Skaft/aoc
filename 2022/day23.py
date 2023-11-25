import pytest

from helpers import AoCSolution


DAY = 23

DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}

class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        rows = raw_input.splitlines()

        elves = set()
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                if value == "#":
                    elves.add((r, c))

        return elves

    @staticmethod
    def set_borders(points):
        minX = min(x for x, y in points)
        maxX = max(x for x, y in points)
        minY = min(y for x, y in points)
        maxY = max(y for x, y in points)
        return minX, maxX, minY, maxY

    def count_empty(self, elves):
        minX, maxX, minY, maxY = self.set_borders(elves)
        cell_count = (maxX - minX + 1) * (maxY - minY + 1)
        return cell_count - len(elves)

    def valid_dir(self, pos, direction, elves):
        r, c = pos
        if direction == "N":
            nbs = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)]
        elif direction == "S":
            nbs = [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
        elif direction == "E":
            nbs = [(r - 1, c + 1), (r, c + 1), (r + 1, c + 1)]
        elif direction == "W":
            nbs = [(r - 1, c - 1), (r, c - 1), (r + 1, c - 1)]

        return not any(nb in elves for nb in nbs)

    def find_move(self, pos, elves, order):
        first_valid = None
        all_valid = True
        for direction in order:
            if self.valid_dir(pos, direction, elves):
                if first_valid is None:
                    first_valid = direction
                if not all_valid:
                    break
            else:
                all_valid = False
                if first_valid:
                    break
        if all_valid or first_valid is None:
            return None
        r, c = pos
        dr, dc = DIRS[first_valid]
        return r + dr, c + dc

    def make_round(self, elves, order):
        proposals = {}
        collisions = set()
        new_elves = elves.copy()

        for pos in elves:
            if to := self.find_move(pos, elves, order):
                if to in proposals:
                    collisions.add(to)
                else:
                    proposals[to] = pos
        for pos in collisions:
            proposals.pop(pos)

        for to, fro in proposals.items():
            new_elves.remove(fro)
            new_elves.add(to)

        return new_elves

    @staticmethod
    def display(elves):
        minR, maxR, minC, maxC = PartOne.set_borders(elves)
        grid = [["."] * (maxC - minC + 1) for _ in range(maxR - minR + 1)]
        for r, c in elves:
            grid[r - minR][c - minC] = "#"
        display_str = "\n".join("".join(row) for row in grid)
        return display_str

    def main(self, elves):
        order = ["N", "S", "W", "E"]
        for _ in range(10):
            elves = self.make_round(elves, order)
            order.append(order.pop(0))
        return self.count_empty(elves)


class PartTwo(PartOne):
    def main(self, elves):
        order = ["N", "S", "W", "E"]
        rounds = 0
        while True:
            new_elves = self.make_round(elves, order)
            rounds += 1
            if new_elves == elves:
                break
            elves = new_elves
            order.append(order.pop(0))
        return rounds


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS


def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 110

def test_part1_count():
    sol = PartOne(DAY)
    elves = sol.clean_input(sol.raw_test_inputs[-1])
    assert sol.count_empty(elves) == 110

def test_part1_round1():
    sol = PartOne(DAY)
    elves = sol.clean_input(sol.raw_test_inputs[0])
    elves = sol.make_round(elves, list("NSWE"))
    elves2 = sol.clean_input(sol.raw_test_inputs[1])
    assert sol.display(elves) == sol.display(elves2)

def test_part1_round2():
    sol = PartOne(DAY)
    elves = sol.clean_input(sol.raw_test_inputs[1])
    elves = sol.make_round(elves, list("SWEN"))
    elves2 = sol.clean_input(sol.raw_test_inputs[2])
    assert sol.display(elves) == sol.display(elves2)

def test_part1_display():
    sol = PartOne(DAY)
    start_string = sol.raw_test_inputs[0]
    elves = sol.clean_input(start_string)
    displayed = sol.display(elves)
    assert displayed == start_string

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 20
