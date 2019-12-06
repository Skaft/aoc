from input import data, sample, sample2
from collections import defaultdict
import itertools as it


def sol(data):
    dct = defaultdict(list)
    for line in data.split('\n'):
        inr, outr = line.split(')')
        dct[inr].append(outr)

    paths = {}

    def recrs(path):
        for outr in dct[path[-1]]:
            newpath = path + [outr]
            paths[outr] = newpath
            recrs(newpath)

    recrs(['COM'])

    # part 1
    print(sum(len(p)-1 for p in paths.values()))

    # part 2
    sanpath = paths['SAN']
    mypath = paths['YOU']
    steps = 0
    for a, b in it.zip_longest(mypath[:-1], sanpath[:-1]):
        if a!=b:
            steps += bool(a) + bool(b)

    print(steps)


sol(data)