import pytest

from helpers import AoCSolution


DAY = 9


class PartOne(AoCSolution):

    def clean_input(self, raw_input):
        moves = []
        for line in raw_input.splitlines():
            direction, steps = line.split()
            moves.extend(direction * int(steps))
        return moves

    def move(self, node, direction):
        x, y = node
        if direction == "U":
            return x, y + 1
        if direction == "D":
            return x, y - 1
        if direction == "L":
            return x - 1, y
        if direction == "R":
            return x + 1, y
    
    def follow(self, node, target):
        x, y = node
        tx, ty = target
        dx = tx - x
        dy = ty - y
        if max(abs(dx), abs(dy)) <= 1:
            return node
        if dx == 0:
            return x, y + dy / abs(dy)
        if dy == 0:
            return x + dx / abs(dx), y
        return x + dx / abs(dx), y + dy / abs(dy)

    def main(self, moves):
        head = tail = (0, 0)
        visited = {tail}
        for direction in moves:
            head = self.move(head, direction)
            tail = self.follow(tail, head)
            visited.add(tail)
        return len(visited)


class PartTwo(PartOne):
    def main(self, moves):
        head = (0, 0)
        tails = [(0, 0) for _ in range(9)]
        visited = {head}
        for direction in moves:
            head = self.move(head, direction)
            prev = head
            new_tails =[]
            for tail in tails:
                prev = self.follow(tail, prev)
                new_tails.append(prev)
            visited.add(prev)
            tails = new_tails
        return len(visited)


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 13

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 1
    assert sol.run(2) == 36