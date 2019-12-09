from enum import Enum
from functools import wraps
from itertools import zip_longest
from collections import deque, defaultdict


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
    SHIFT_BASE = 9
    EXIT = 99


class ParameterMode(Enum):
    """Parameter modes recognized by the Computer"""
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2
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
            pruned_params = []
            prm_mode_pairs = zip_longest(params, modes, fillvalue=Mode.DEFAULT)
            for i, (prm, mode) in enumerate(prm_mode_pairs):
                if mode == Mode.RELATIVE:
                    prm += comp_inst._relative_base
                if i in skip or mode == Mode.IMMEDIATE:
                    pass
                else:
                    prm = comp_inst.get(prm)
                pruned_params.append(prm)

            return method(comp_inst, *pruned_params)

        # The number of parameters needs to be known before calling, so that
        # the parameters can be read properly. Reading it from the decorated
        # function and sticking it on the wrapper (subtracting 1 to account for
        # the "self" arg) to avoid redundant storage, though a bit hacky
        wrapper.param_count = method.__code__.co_argcount - 1
        return wrapper
    return deco


class Computer:

    def __init__(self, program, input=0, pointer=0):
        if isinstance(input, int):
            input = [input]

        self._input_queue = deque(input)
        self._output_queue = deque()
        self._program = program.copy()
        self._extra_memory = defaultdict(int)
        self._mem_limit = len(program)
        self.pointer = pointer
        self._relative_base = 0

    def send(self, value):
        self._input_queue.append(value)

    def collect(self, last=False):
        return self._output_queue[-1]
        # if last:
        #     return self._output_queue.pop()
        # return self._output_queue.popleft()

    def set(self, index, value):
        if index < self._mem_limit:
            mem = self._program
        else:
            mem = self._extra_memory
        mem[index] = value

    def get(self, index):
        if index < self._mem_limit:
            mem = self._program
        else:
            mem = self._extra_memory
        return mem[index]

    @moded()
    def _jump_true(self, n, index):
        if n != 0:
            self.pointer = index

    @moded()
    def _jump_false(self, n, index):
        if n == 0:
            self.pointer = index

    @moded(skip=2)
    def _add(self, a, b, index):
        self.set(index, a + b)

    @moded(skip=2)
    def _mul(self, a, b, index):
        self.set(index, a * b)

    @moded(skip=0)
    def _input(self, index):
        value = self._input_queue.popleft()
        self.set(index, value)

    @moded()
    def _output(self, value):
        self._output_queue.append(value)

    @moded(skip=2)
    def _less_than(self, a, b, index):
        self.set(index, a < b)

    @moded(skip=2)
    def _equals(self, a, b, index):
        self.set(index, a == b)

    @moded()
    def _shift_base(self, shift):
        self._relative_base += shift

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
            if opcode == Opcode.INPUT and not self._input_queue:
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

            # if opcode == Opcode.OUTPUT:
            #     return False