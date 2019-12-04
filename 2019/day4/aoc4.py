"""My first solution, using a ridiculous approach. My morning brain was
stuck on the idea of keeping the digits in lists, so they can be easily checked
for sorted order and counted. But that idea led me to a messy and
time-consuming incr function for stepping through the numbers. Oh well."""

from input import data
from collections import Counter
from timeit import default_timer

start = default_timer()

def incr(lst):
    last = len(lst) - 1
    for i, n in enumerate(lst[::-1]):
        lst[last - i] = str((int(n) + 1) % 10)
        if n != '9':
            return


def sol1(data):
    a, b = map(list, data.split('-'))
    c = 0
    while a < b:
        if a == sorted(a) and len(set(a)) < 6:
            c += 1
        incr(a)
    print(c)


def sol2(data):
    a, b = map(list, data.split('-'))
    c = 0
    while a < b:
        if a == sorted(a) and 2 in Counter(a).values():
            c += 1
        incr(a)
    print(c)

sol1(data)
sol2(data)
print(default_timer() - start)