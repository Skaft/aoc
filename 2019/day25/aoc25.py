from input import data
from itertools import combinations
from computer import Computer


def parse(string):
    return [int(n) for n in string.split(',')]

def command(cmd):
    comp.send([ord(c) for c in ''.join(cmd)] + [10])
    comp.run()

def find_item_combo(items):
    """
    Inefficient bruteforce code to find the right combination of items
    to pass the weight test. Doesn't use the heavy/light hints, just tries
    everything until something works.
    """
    for item in items:
        command(f"drop {item}")
    for count in range(1, len(items) + 1):
        for comb in combinations(items, count):
            for item in comb:
                command(f"take {item}")
            comp.collect()
            command('south')
            out = ''.join(chr(n) for n in comp.collect())
            if 'ejected back' not in out:
                return comb, out
            for item in comb:
                command(f"drop {item}")

def manual_mode():
    """Used to play the game properly."""
    while True:
        comp.run()
        print(''.join(chr(n) for n in comp.collect()))
        inp = input()
        if inp == 'q':
            return
        comp.send([ord(c) for c in ''.join(inp)] + [10])


# While exploring in manual mode, I logged my input so I could just send it
# all at once on the next run to quickly get back to the same point.
# `progress` now picks up all items and moves to the room before the pressure
# pad thingy.
progress = """south
west
take shell
east
east
take space heater
west
north
west
north
take jam
east
south
take asterisk
south
take klein bottle
east
take spool of cat6
west
north
north
west
north
take astronaut ice cream
north
east
south
take space law space brochure
north
west
south
south
south
south
west
"""


items = [line[5:] for line in progress.splitlines() if line.startswith('take')]

program = parse(data)
comp = Computer(program, input=[ord(c) for c in ''.join(progress)])
c, out = find_item_combo(items)
print(out)
