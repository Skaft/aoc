"""A saner approach that I should have gone for first."""

from input import data
from collections import Counter
from timeit import default_timer

start = default_timer()


def sol1(data):
    a, b = map(int, data.split('-'))
    c = 0
    for n in range(a, b+1):
        n = str(n)
        if all(x<=y for x,y in zip(n, n[1:])) and len(set(n)) < 6:
            c += 1
    print(c)

def sol2(data):
    a, b = map(int, data.split('-'))
    c = 0
    for n in range(a, b+1):
        n = str(n)
        if all(x<=y for x,y in zip(n, n[1:])) and 2 in Counter(n).values():
            c += 1
    print(c)

sol1(data)
sol2(data)
print(default_timer() - start)
