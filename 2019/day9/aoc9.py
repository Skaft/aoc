from input import data
from helpers import Computer


def sol(data, input=0):
    program = [int(n) for n in data.split(',')]
    comp = Computer(program, input=input)
    comp.run()
    print(comp.collect())


sol(data, input=1)
sol(data, input=2)
