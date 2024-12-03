import re
from operator import mul


with open("inputs/day3.txt") as file:
    data = file.read()

# part1
part1 = 0
pattern1 = re.compile(r"mul\(\d+,\d+\)")
for instr in re.findall(pattern1, data):
    part1 += eval(instr)
print(part1)

# part2
part2 = 0
pattern2 = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
do = True
for instr in re.findall(pattern2, data):
    if instr == "do()":
        do = True
    elif instr == "don't()":
        do = False
    elif do:
        part2 += eval(instr)

print(part2)
