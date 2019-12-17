from input import data
from computer import Computer


def parse(string):
    return [int(n) for n in string.split(',')]


def part1(string):
    program = parse(string)
    comp = Computer(program)
    comp.run()
    output = ''.join(chr(c) for c in comp.collect())
    lines = output.split('\n')
    scaffolds = {
        (x, y)
        for y, row in enumerate(lines)
        for x, char in enumerate(row)
        if char == '#'
    }
    s = 0
    for x, y in scaffolds:
        neighbors = (x-1,y), (x+1,y), (x,y-1), (x,y+1)
        if all(n in scaffolds for n in neighbors):
            s += x*y
    print(s)

def to_code(chars):
    s = ','.join(chars) + '\n'
    s = s.replace('W', '12')
    s = s.replace('T', '10')
    return [ord(c) for c in s]

def part2(string):
    program = parse(string)
    comp = Computer(program)
    comp.set(0, 2)
    main = to_code('ABBCCABBCA')
    A = to_code('R4RWRTLW')
    B = to_code('LWR4RW')
    C = to_code('LWL8RT')
    video = to_code('n')
    comp.send(main + A + B + C + video)
    comp.run()
    output = comp.collect()
    print(output[-1])

part1(data)
part2(data)
