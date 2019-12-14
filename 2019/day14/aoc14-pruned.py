from input import data, sample, sample2

from math import ceil
from collections import defaultdict


def parse(data):
    dct = {}
    for line in data.split('\n'):
        reactants, product = line.split(' => ')
        needed = []
        for thing in reactants.split(', '):
            amt, name = thing.split()
            needed.append((int(amt), name))
        amt, name = product.split()
        dct[name] = [int(amt), needed]
    return dct

def count_ores(product: str, amt_want: int):
    """
    Recursively count how many ores are needed to make amt_want of product.

    Leftovers from previous reactions are used to not make more than needed.
    """
    if product == 'ORE':
        return amt_want
    amt_get, reqs = dct[product]
    amt_need = max(amt_want - leftovers[product], 0)
    leftovers[product] -= amt_want - amt_need
    make_n = ceil(amt_need / amt_get)
    leftovers[product] += make_n * amt_get - amt_need
    return sum(count_ores(name, amt * make_n) for amt, name in reqs)


dct = parse(data)

#part1
leftovers = defaultdict(int)
print(count_ores('FUEL', 1))

#part2
coffins = 1000000000000
low = 1
high = coffins

while high - low > 1:
    mid = (low + high) // 2
    leftovers = defaultdict(int)
    cost = count_ores('FUEL', mid)
    if cost <= coffins:
        low = mid
    else:
        high = mid
print(low)
