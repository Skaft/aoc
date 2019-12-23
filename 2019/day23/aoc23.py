from input import data
from computer import Computer
from itertools import cycle


def parse(string):
    return [int(n) for n in string.split(',')]

def part1():
    comps = [Computer(program, input=i) for i in range(50)]

    for comp in cycle(comps):
        comp.run(release_always=True)
        if len(comp._output_queue) == 3:
            adr, x, y = comp.collect()
            if adr == 255:
                print(y)
                break
            comps[adr].send([x, y])

def part2():
    comps = [Computer(program, input=i) for i in range(50)]
    NAT = None
    last_sent_by_nat = None
    while True:
        for comp in comps:
            comp.run(release_always=True)
            if len(comp._output_queue) == 3:
                adr, x, y = comp.collect()
                if adr == 255:
                    NAT = x, y
                    # print("Stores", NAT)
                    for c in comps:
                        c.idle = False
                        c._idle_count = 0
                else:
                    comps[adr].send([x, y])
            elif all(comp.idle for comp in comps):
                comps[0].send(NAT)
                comps[0].idle = False
                comps[0]._idle_counter = 0
                # print("NAT sends", NAT)
                if NAT[1] == last_sent_by_nat:
                    print(last_sent_by_nat)
                    return
                last_sent_by_nat = NAT[1]
                break

program = parse(data)

part1()
part2()
