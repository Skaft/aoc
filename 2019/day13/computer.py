from enum import IntEnum
from functools import wraps
from itertools import zip_longest
from collections import deque, defaultdict


class Opcode(IntEnum):
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


class ParameterMode(IntEnum):
    """Parameter modes recognized by the Computer"""
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2
    DEFAULT = 0


# Just an alias
Mode = ParameterMode


def moded(write=None):
    """
    Decorator for replacing Computer method params according to their mode.

    The optional 'write' argument can be an int or an iterable of ints, marking
    (by index) parameters that intend to write to the program or extra memory.
    Such parameters are always treated as positions by their methods and
    therefore do not need replacing here.
    """

    if write is None:
        write = []
    elif isinstance(write, int):
        write = [write]

    def deco(method):

        @wraps(method)
        def wrapper(comp_inst, *params, modes=None):
            if modes is None:
                modes = []
            pruned_params = []
            param_mode_pairs = zip_longest(
                params,
                modes,
                fillvalue=Mode.DEFAULT.value
            )

            for i, (param, mode) in enumerate(param_mode_pairs):
                if mode == Mode.RELATIVE:
                    param += comp_inst._relative_base
                if mode != Mode.IMMEDIATE and i not in write:
                    param = comp_inst.get(param)
                pruned_params.append(param)

            return method(comp_inst, *pruned_params)

        # The number of parameters needs to be known before calling, so that
        # the parameters can be read properly. Reading it from the decorated
        # function and sticking it on the wrapper (subtracting 1 to account for
        # the "self" arg) to avoid redundant storage, though a bit hacky
        wrapper.param_count = method.__code__.co_argcount - 1
        return wrapper
    return deco


log = []

class Computer:

    def __init__(self, program, input=None, pointer=0):
        if isinstance(input, int):
            input = [input]
        elif input is None:
            input = []
        self._input_queue = deque(input)
        self._output_queue = deque()
        self._program = program.copy()
        self._extra_memory = defaultdict(int)
        self._mem_limit = len(program)
        self.pointer = pointer
        self._relative_base = 0

        mappings = [(op.value, f"_{op.name.lower()}") for op in Opcode]
        self._methods = {
            code: getattr(self, method_name)
            for code, method_name in mappings
            if hasattr(self, method_name)
        }

    def send(self, value):
        self._input_queue.append(value)

    def collect(self, n=None):
        if n is None:
            n = len(self._output_queue)
        if n == 1:
            return self._output_queue.popleft()
        return [self._output_queue.popleft() for _ in range(n)]

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

    def read(self):
        value = self._program[self.pointer]
        self.pointer += 1
        return value

    @moded()
    def _jump_true(self, n, index):
        if n != 0:
            self.pointer = index
            # log.append(f"JUMP_TRUE: Jumping to {index} ({n} != 0)")

    @moded()
    def _jump_false(self, n, index):
        if n == 0:
            self.pointer = index
            # log.append(f"JUMP_FALSE: Jumping to {index} ({n} == 0)")

    @moded(write=2)
    def _add(self, a, b, index):
        self.set(index, a + b)
        # log.append(f"ADD: Setting {index} to {a} + {b} = {a+b}")

    @moded(write=2)
    def _mul(self, a, b, index):
        self.set(index, a * b)
        # log.append(f"MUL: Setting {index} to {a} * {b} = {a*b}")

    @moded(write=0)
    def _input(self, index):
        value = self._input_queue.popleft()
        self.set(index, value)
        # log.append(f"INPUT: Setting {index} to {value}")

    @moded()
    def _output(self, value):
        self._output_queue.append(value)
        # log.append(f"OUTPUT: Outputting {value}")

    @moded(write=2)
    def _less_than(self, a, b, index):
        self.set(index, int(a < b))
        # log.append(f"LESS_THAN: Setting {index} to {int(a < b)}")

    @moded(write=2)
    def _equals(self, a, b, index):
        self.set(index, int(a == b))
        # log.append(f"EQUALS: Setting {index} to {int(a == b)}")

    @moded()
    def _shift_base(self, shift):
        self._relative_base += shift
        # log.append(f"SHIFT_BASE: Shifting base by {shift}")

    @staticmethod
    def parse_opcode(value):
        """Split a number into opcode and parameter mode components"""
        modes_int, opcode = divmod(value, 100)
        param_modes = [int(n) for n in reversed(str(modes_int))]
        return opcode, param_modes

    def run(self, release_on_output=False):
        """
        Run the loaded program.

        Stops either by a halting opcode (True exit) or when requiring missing
        input (False exit). If release_on_output is True, generating output
        also prompts a False exit. A False exit indicates that the program is
        expecting to resume later.
        """
        while True:
            opcode, param_modes = self.parse_opcode(self.read())

            if opcode == Opcode.EXIT:
                return True
            if opcode == Opcode.INPUT and not self._input_queue:
                self.pointer -= 1  # move back to retry opcode later
                return False

            method = self._methods[opcode]
            params = [self.read() for _ in range(method.param_count)]
            # log.append(f"{self.pointer - 1 - len(params)} {params} {param_modes[::-1]}")
            method(*params, modes=param_modes)

            if release_on_output and opcode == Opcode.OUTPUT:
                # for line in log:
                #     print(line)
                # log.clear()
                return False
