"""
An attempt to optimize by generating ascending-order digit sequences directly,
rather than going through all numbers in the range and checking each.
"""

from input import data
from collections import Counter
from timeit import default_timer

start = default_timer()

def gen_ascending(start):

    # turn start value into a list of its digits
    digits = [int(d) for d in str(start)]
    n_digits = len(digits)
    while True:

        # find the first digit smaller than the previous (if any)
        for i, (prev, digit) in enumerate(zip(digits, digits[1:]), 1):

            # if descending anywhere, replace all digits from that point with
            # with the last ascending digit (prev)
            if prev > digit:
                tail_len = n_digits - i
                digits[i:] = [prev] * tail_len
                break

        # digits are now in ascending order, so yield them
        yield digits

        # finally, increment the number
        for i, n in enumerate(reversed(digits), 1):
            digits[n_digits - i] = (n + 1) % 10
            if n != 9:
                break


def sol(data):
    start, stop = data.split('-')
    stop = [int(n) for n in stop]
    part1, part2 = 0, 0
    for digit_seq in gen_ascending(start):
        if digit_seq > stop:
            break
        counts = Counter(digit_seq)
        if max(counts.values()) >= 2:
            part1 += 1
        if 2 in counts.values():
            part2 += 1
    print(part1)
    print(part2)

sol(data)
print(default_timer() - start)