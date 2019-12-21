from input import data
from computer import Computer


def parse(string):
    return [int(n) for n in string.split(',')]

def run_springscript(script):
    intcode = [ord(c) for c in ''.join(script)]
    comp = Computer(program, input=intcode)
    comp.run()
    out = comp.collect()
    if out[-1] > 128:
        print(out[-1])
    else:
        print(''.join(chr(n) for n in out))


program = parse(data)

# part1
run_springscript("""
    NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK
    """.lstrip())

# part2
run_springscript("""
    NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    NOT E T
    NOT T T
    OR H T
    AND T J
    RUN
    """.lstrip())
