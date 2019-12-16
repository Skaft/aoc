from input import data
from itertools import cycle, accumulate, islice

def parse(input):
    return [int(n) for n in input]

def next_phase(lst):
    out = []
    L = len(lst)
    for i in range(1, L + 1):
        res = 0
        for slice_start in range(i - 1, L, 4*i):
            res += sum(lst[slice_start:slice_start + i])
        for slice_start in range(3*i - 1, L, 4*i):
            res -= sum(lst[slice_start:slice_start + i])
        out.append(abs(res) % 10)
    return out

def part1(string):
    digits = parse(string)
    for _ in range(100):
        digits = next_phase(digits)
    print(''.join(str(d) for d in digits[:8]))

def part2(string):
    digits = reversed(parse(string))
    msg_start = int(string[:7])
    tail_len = len(string) * 10_000 - msg_start
    for _ in range(100):
        last_n = islice(cycle(digits), tail_len)
        digits = list(accumulate(last_n, lambda a, b: (a + b) % 10))
    print(''.join(str(d) for d in digits[:-9:-1]))

part1(data)
part2(data)
