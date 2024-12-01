import collections
import re


digits = re.compile(r"\d+")


with open("inputs/day1.txt") as file:
    numbers = [int(n) for n in digits.findall(file.read())]

# part 1
left = sorted(numbers[::2])
right = sorted(numbers[1::2])

sum_dist = sum(abs(a - b) for a, b in zip(left, right))

print(sum_dist)

# part 2
left_counts = collections.Counter(left)
right_counts = collections.Counter(right)


total = 0
for n, left_freq in left_counts.items():
    right_freq = right_counts[n]
    total += n * right_freq * left_freq

print(total)

def test_input_parsed_correctly():
    assert numbers[:6] == [15131, 78158, 32438, 35057, 12503, 57702]
