import argparse
import itertools
import math


def parse(data):
    antennas = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == ".":
                continue
            if char in antennas:
                antennas[char].append((x, y))
            else:
                antennas[char] = [(x, y)]

    return antennas, (x, y)


def part1(data):
    antennas, (max_x, max_y) = parse(data)

    antinodes = set()

    for freq, positions in antennas.items():
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):

            x3 = x1 - (x2 - x1)
            x4 = x2 - (x1 - x2)
            y3 = y1 - (y2 - y1)
            y4 = y2 - (y1 - y2)

            if 0 <= x3 <= max_x and 0 <= y3 <= max_y:
                antinodes.add((x3, y3))

            if 0 <= x4 <= max_x and 0 <= y4 <= max_y:
                antinodes.add((x4, y4))

    return len(antinodes)

        

def part2(data):
    antennas, (max_x, max_y) = parse(data)

    antinodes = set()

    for freq, positions in antennas.items():
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            dx = x2 - x1
            dy = y2 - y1
            gcd = math.gcd(dx, dy)
            dx = dx // gcd
            dy = dy // gcd

            x = x1
            y = y1
            while 0 <= x <= max_x and 0 <= y <= max_y:
                antinodes.add((x, y))
                x += dx
                y += dy

            x = x1
            y = y1
            while 0 <= x <= max_x and 0 <= y <= max_y:
                antinodes.add((x, y))
                x -= dx
                y -= dy
    
    return len(antinodes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run with test data")
    args = parser.parse_args()

    if args.test:
        data_path = "test_data/day8.txt"
    else:
        data_path = "inputs/day8.txt"

    with open(data_path) as file:
        data = file.read()

    print(part1(data))
    print(part2(data))
