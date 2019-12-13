from input import data

from computer import Computer
from collections import Counter

class Breakout:
    CHARS = ' █▒‾•'

    def __init__(self):
        program = [int(n) for n in data.split(',')]
        self.comp = Computer(program)
        self.score = 0
        self.board = None
        self.setup()

    def read_frame(self):
        output = self.comp.collect()
        xvals = output[::3]
        yvals = output[1::3]
        ids = output[2::3]
        return xvals, yvals, ids

    def setup(self):
        self.comp.set(0, 2)
        self.comp.run()
        xvals, yvals, ids = self.read_frame()
        width = max(xvals) + 1
        height = max(yvals) + 1
        self.board = [[' '] * width for _ in range(height)]
        self.update((xvals, yvals, ids))

    def update(self, frame_data):
        for x, y, id in zip(*frame_data):
            if id == 3:
                self.paddle_pos = x, y
            elif id == 4:
                self.ball_pos = x, y
            if x == -1:
                self.score = id
            else:
                self.board[y][x] = id

    def run_manual(self):
        exit = False
        while not exit:
            self.draw()
            move = input()
            if move == 'q':
                return
            self.comp.send(int(move))
            exit = self.comp.run()
            frame_data = self.read_frame()
            self.update(frame_data)

    def run_auto(self):
        exit = False
        while not exit:
            ball_x, ball_y = self.ball_pos
            pad_x, pad_y = self.paddle_pos

            if pad_x < ball_x:
                move = 1
            elif pad_x > ball_x:
                move = -1
            else:
                move = 0

            self.comp.send(move)
            exit = self.comp.run()
            frame_data = self.read_frame()
            self.update(frame_data)

    def draw(self):
        for row in self.board:
            print(''.join(Breakout.CHARS[id] for id in row))
        print("Score:", self.score)


def part1():
    id_counts = Counter(id for row in game.board for id in row)
    print(id_counts[2])


def part2():
    game.run_auto()
    print(game.score)


game = Breakout()
part1()
part2()
