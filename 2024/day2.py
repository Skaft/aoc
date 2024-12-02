import collections
import re


digits = re.compile(r"\d+")

reports = []
with open("inputs/day2.txt") as file:
    for line in file:
        reports.append([int(n) for n in line.strip().split()])

def is_safe(report):
    pairs = list(zip(report, report[1:]))
    ascending = all(a < b for a, b in pairs)
    descending = all(a > b for a, b in pairs)
    if not (ascending or descending):
        return False

    if all(1 <= abs(a - b) <= 3 for a, b in pairs):
        return True
    return False

print(sum(is_safe(report) for report in reports))

safe = 0
for report in reports:
    indexes = range(len(report))
    variants = [list(report) for _ in indexes]
    for i in indexes:
        variants[i].pop(i)
    if any(is_safe(variant) for variant in variants):
        safe += 1

print(safe)