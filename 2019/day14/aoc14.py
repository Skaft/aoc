from input import data, sample, sample2

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
        amt = int(amt)
        dct[name] = [amt, needed]
    return dct

def sum(product, amt_want):
    if product == 'ORE':
        return amt_want
    amt_get, reqs = dct[product]
    from_before = leftovers[product]
    needed = max(amt_want - from_before, 0)
    leftovers[product] -= amt_want - needed
    if needed % amt_get == 0:
        make_n = needed // amt_get
        rem = amt_get*make_n - needed
    else:
        round_up = needed + amt_get - needed % amt_get
        make_n = round_up // amt_get
        rem = round_up - needed
    leftovers[product] += rem
    ores = 0
    for amt, name in reqs:
        ores += sum(name, amt * make_n)
    return ores

dct = parse(data)

#part1
leftovers = defaultdict(int)
print(sum('FUEL', 1))

#part2
low = 1
high = 20000000
tril = 1000000000000
while high - low > 1:
    mid = (low + high) // 2
    leftovers = defaultdict(int)
    cost = sum('FUEL', mid)
    if cost <= tril:
        low = mid
    else:
        high = mid
print(low)
