from input import data
from helpers import Computer
from collections import defaultdict


class Robot:
    # N, E, S, W
    DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    WHITE = '█'
    BLACK = ' '
    EMPTY = ' '

    def __init__(self, data):
        self.grid = defaultdict(int)
        program = [int(n) for n in data.split(',')]
        self.comp = Computer(program)
        self.pos = 0, 0
        self.painted = set()
        self.dir_index = 0

    def paint(self, color):
        """Paint current location with provided color"""
        self.grid[self.pos] = color
        self.painted.add(self.pos)

    def look(self):
        """Read color at current position and pass to computer"""
        color = self.grid[self.pos]
        self.comp.send(color)

    def rotate(self, turn):
        """Modify direction index according to turn value"""
        if turn == 1:
            self.dir_index += 1
        else:
            self.dir_index -= 1
        self.dir_index %= 4

    def run(self):
        """Run the paint-and-move process until computer halts"""
        while True:
            self.look()
            if self.comp.run():
                break
            color, turn = self.comp.collect(2)
            self.paint(color)
            self.rotate(turn)
            self.step()

    def step(self):
        """Move one step in current direction"""
        dx, dy = Robot.DIRECTIONS[self.dir_index]
        x, y = self.pos
        self.pos = x + dx, y + dy

    @property
    def map(self):
        """Return a print-ready string of the grid state"""

        x_vals = {x for x, y in self.painted}
        y_vals = {y for x, y in self.painted}
        minx, miny = min(x_vals), min(y_vals)
        width = max(x_vals) - minx + 1
        height = max(y_vals) - miny + 1

        map = [[Robot.EMPTY] * width for _ in range(height)]

        for (x, y), col in self.grid.items():
            char = Robot.WHITE if col else Robot.BLACK
            map[y - miny][x - minx] = char

        dirchar = '^>v<'[self.dir_index]
        x, y = self.pos
        map[y - miny][x - minx] = dirchar
        out = '\n'.join(''.join(line) for line in map)
        return out


def part1():
    robot = Robot(data)
    robot.run()
    print(len(robot.painted))

def part2():
    robot = Robot(data)
    robot.paint(1)
    robot.run()
    print(robot.map)

part1()
part2()
