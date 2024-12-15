import re
import math

import numpy as np


def parse(data):
    digits = re.compile(r"\d+")

    specs = []
    for machine_data in data.split("\n\n"):
        numbers = [int(n) for n in re.findall(digits, machine_data)]
        specs.append(numbers)
    
    return specs

def equation_system_int(x1, y1, x2, y2, xt, yt):
    denom = x2 * y1 - x1 * y2
    if denom == 0:
        return

    A_num = x2 * yt - xt * y2
    B_num = xt * y1 - x1 * yt

    if A_num % denom == 0 and B_num % denom == 0:
        A = A_num // denom
        B = B_num // denom

        return A, B

def part1(data):
    machines = parse(data)
    cost = 0
    for x1, y1, x2, y2, xt, yt in machines:
        sol = equation_system_int(x1, y1, x2, y2, xt, yt)
        if sol is not None:
            A, B = sol
            if A >= 0 and B >= 0:
                cost += 3 * A + B
    return cost

def part2(data):

    machines = parse(data)
    cost = 0
    for x1, y1, x2, y2, xt, yt in machines:
        xt += 10000000000000
        yt += 10000000000000

        sol = equation_system_int(x1, y1, x2, y2, xt, yt)
        if sol is not None:
            A, B = sol
            if A >= 0 and B >= 0:
                cost += 3 * A + B

    return cost



if __name__ == "__main__":
    from common import get_input

    data = get_input(day=13)

    print(part1(data))
    print(part2(data))
