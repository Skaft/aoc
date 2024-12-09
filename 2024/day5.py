import argparse
import functools


def parse(data):
    top, bottom = data.split("\n\n")

    rules = []
    for line in top.splitlines():
        a, b = line.split("|")
        rules.append((int(a), int(b)))

    groups = [list(map(int, line.split(","))) for line in bottom.splitlines()]

    return rules, groups

def is_valid(group, rules):
    for a, b in rules:
        if a not in group or b not in group:
            continue
        if group.index(a) > group.index(b):
            return False
    return True


def cmp(a, b, rules):
    if a == b:
        return 0
    if (a, b) in rules:
        return -1
    return 1

def part1(data):
    rules, groups = parse(data)

    total = 0
    for group in groups:
        if is_valid(group, rules):
            middle = len(group) // 2
            total += group[middle]

    return total

def part2(data):
    rules, groups = parse(data)

    sort_cmp = functools.partial(cmp, rules=rules)
    sort_key = functools.cmp_to_key(sort_cmp)

    total = 0
    for group in groups:
        if not is_valid(group, rules):
            ordered = sorted(group, key=sort_key)
            middle = len(group) // 2
            total += ordered[middle]

    return total
    

if __name__ == "__main__":
    from common import get_input

    data = get_input(day=5)

    print(part1(data))
    print(part2(data))
