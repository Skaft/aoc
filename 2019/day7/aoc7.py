from input import data
from enum import Enum
from functools import wraps
import itertools as it


class Opcode(Enum):
    """Names of the opcode methods"""
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    EXIT = 99


class ParameterMode(Enum):
    """Parameter modes recognized by the Computer"""
    POSITION = 0
    IMMEDIATE = 1
    DEFAULT = 0


# Just an alias
Mode = ParameterMode


def moded(skip=None):
    """
    Decorator for replacing Computer method params according to their mode.

    The optional 'skip' argument can be an int or an iterable of ints, marking
    (by index) parameters that should not be replaced regardless of their mode.
    """

    if skip is None:
        skip = []
    elif isinstance(skip, int):
        skip = [skip]

    def deco(method):

        @wraps(method)
        def wrapper(comp_inst, *params, modes=None):
            if modes is None:
                modes = []
            params = list(params)
            prm_mode_pairs = it.zip_longest(params, modes, fillvalue=Mode.DEFAULT)

            for i, (prm, mode) in enumerate(prm_mode_pairs):
                if i in skip or mode == Mode.IMMEDIATE:
                    pass
                elif mode == Mode.POSITION:
                    params[i] = comp_inst.get(prm)
                else:
                    raise ValueError(f'Unknown parameter mode: {mode}')

            return method(comp_inst, *params)

        # The number of parameters needs to be known before calling, so that
        # the parameters can be read properly. Reading it from the decorated
        # function and sticking it on the wrapper (subtracting 1 to account for
        # the "self" arg) to avoid redundant storage, though a bit hacky
        wrapper.param_count = method.__code__.co_argcount - 1
        return wrapper
    return deco


class Computer:

    def __init__(self, program, phase=0, pointer=0):
        self.program = program
        self.output_signal = None
        self.pointer = pointer
        self.used_phase = False
        self.waiting = False
        self.phase = phase

    def send_signal(self, value):
        self.input_signal = value
        self.waiting = False

    def set(self, position, value):
        self.program[position] = value

    def get(self, position):
        return self.program[position]

    @moded()
    def _jump_true(self, n, position):
        if n != 0:
            self.pointer = position

    @moded()
    def _jump_false(self, n, position):
        if n == 0:
            self.pointer = position

    @moded(skip=2)
    def _add(self, a, b, position):
        self.set(position, a + b)

    @moded(skip=2)
    def _mul(self, a, b, position):
        self.set(position, a * b)

    @moded(skip=0)
    def _input(self, position):

        if not self.used_phase:
            self.set(position, self.phase)
            self.used_phase = True
        else:
            self.set(position, self.input_signal)
            self.waiting = True

    @moded()
    def _output(self, value):
        self.output_signal = value

    @moded(skip=2)
    def _less_than(self, a, b, position):
        self.set(position, a < b)

    @moded(skip=2)
    def _equals(self, a, b, position):
        self.set(position, a == b)

    @staticmethod
    def parse_opcode(value):
        """Split a number into opcode and parameter mode components"""
        modes_int, codepoint = divmod(value, 100)
        opcode = Opcode(codepoint)

        param_modes = []
        while modes_int:
            modes_int, mode = divmod(modes_int, 10)
            param_modes.append(Mode(mode))

        return opcode, param_modes

    def run(self):
        while True:
            # read and parse the value at the pointer
            points_to = self.get(self.pointer)
            opcode, param_modes = self.parse_opcode(points_to)

            if opcode == Opcode.EXIT:
                return True
            elif opcode == Opcode.INPUT and self.waiting:
                return False

            # collect the method matching the opcode
            method = getattr(self, f"_{opcode.name.lower()}")

            # collect parameters
            param_start = self.pointer + 1
            next_instr_start = param_start + method.param_count
            params = map(self.get, range(param_start, next_instr_start))

            # moving pointer before calling to not overwrite jump instructions
            self.pointer = next_instr_start

            method(*params, modes=param_modes)

            if opcode == Opcode.OUTPUT:
                return False


# part1
best = -float('inf')
for seq in it.permutations(range(5)):
    last_out = 0
    for phase in seq:
        c = Computer(data.copy(), phase=phase)
        c.send_signal(last_out)
        c.run()
        last_out = c.output_signal
    result = last_out
    if result > best:
        best = result
print(best)
#part2
def loop(phase_settings, program):
    a,b,c,d,e = phase_settings
    ca = Computer(program.copy(), phase=a)
    cb = Computer(program.copy(), phase=b)
    cc = Computer(program.copy(), phase=c)
    cd = Computer(program.copy(), phase=d)
    ce = Computer(program.copy(), phase=e)
    last_out = 0
    laps = 0
    for comp in it.cycle((ca, cb, cc, cd, ce)):
        if last_out is not None:
            comp.send_signal(last_out)
        if comp.run():
            break
        last_out = comp.output_signal
        laps += 1
    return ce.output_signal


best = -float('inf')


#loop((9,8,7,6,5), program)
for seq in it.permutations(range(5, 10)):
    result = loop(seq, data)
    if result > best:
#        print(result)
        best = result
print(best)