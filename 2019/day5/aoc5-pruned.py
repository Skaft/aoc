"""
My attempt to tidy up the intcode computer.

The main issue was finding a consistent and clear way of handling parameter
modes. In the end I landed with a decorator. It allows me to replace parameters
according to their mode before a function gets them, as well as to bypass this
system in a flexible way by marking individual parameters as non-replaceable.

I used Enum for Opcodes and Parameter modes, mostly to try out Enum. But it
grants some extra readability, and also lets me map Computer methods to opcodes
by name. Still unsure if this is just redundant and/or silly, and that I should
be mapping integers to methods/functions using a dict or something.
"""


from input import data
from enum import Enum
from functools import wraps
from itertools import zip_longest


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
            prm_mode_pairs = zip_longest(params, modes, fillvalue=Mode.DEFAULT)

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

    def __init__(self, program, io=0, pointer=0):
        self.program = program
        self.io = io
        self.pointer = pointer

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
        self.set(position, self.io)

    @moded()
    def _output(self, value):
        self.io = value

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
                break

            # collect the method matching the opcode
            method = getattr(self, f"_{opcode.name.lower()}")

            # collect parameters
            param_start = self.pointer + 1
            next_instr_start = param_start + method.param_count
            params = map(self.get, range(param_start, next_instr_start))

            # moving pointer before calling to not overwrite jump instructions
            self.pointer = next_instr_start

            method(*params, modes=param_modes)


for start_value in (1, 5):
    comp = Computer(data.copy(), start_value)
    comp.run()
    print(comp.io)
