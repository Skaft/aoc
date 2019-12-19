from input import data
from computer import Computer

def parse(string):
    return [int(n) for n in string.split(',')]

def part1(string):
    program = parse(string)
    c = 0
    # map = [['.'] * 50 for _ in range(50)]
    for y in range(50):
        for x in range(50):
            comp = Computer(program, input=(x, y))
            comp.run()
            if comp.collect():
                # map[y][x] = 'X'
                c += 1
        # print(''.join(map[y]))
    print(c)

def run_until(x, y, target_output, program):
    while True:
        comp = Computer(program, input=(x, y))
        comp.run()
        if comp.collect() == target_output:
            return x
        x += 1

def part2(string):
    startx = 0
    stopx = 5
    y = 4
    program = parse(string)
    rowranges = [range(0, 1), range(0,0), range(0,0), range(0,0)]
    while True:
        startx = run_until(startx, y, 1, program)
        stopx = run_until(stopx, y, 0, program)
        rowranges.append(range(startx, stopx))
        if y > 100:
            if startx + 99 in rowranges[y - 99]:
                print(startx*10_000 + (y - 99))
                break
        y += 1

part1(data)
part2(data)
