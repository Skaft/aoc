from input import data
from helpers import Computer
import itertools as it

# part1
def chain(phase_settings, program):
    comps = [Computer(program, input=phase) for phase in phase_settings]
    last_out = 0
    for comp in comps:
        comp.send(last_out)
        comp.run()
        last_out = comp.collect()
    return last_out


print(max(chain(settings, data) for settings in it.permutations(range(5))))

#part2
def loop(phase_settings, program):
    comps = [Computer(program, input=phase) for phase in phase_settings]
    last_out = 0
    for comp in it.cycle(comps):
        comp.send(last_out)
        if comp.run():
            break
        last_out = comp.collect()
    return comps[-1].collect()


print(max(loop(settings, data) for settings in it.permutations(range(5, 10))))
