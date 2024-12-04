import itertools
import argparse

def parse(data):
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[x, y] = char

    return grid

def check_direction(grid, pos, direction, length):
    x, y = pos
    dx, dy = direction

    chars = []
    for step in range(length):
        new_pos = (x + dx * step, y + dy * step)
        char = grid.get(new_pos, ".")
        chars.append(char)
    
    return "".join(chars)

def word_search(grid, target):
    dirs = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    start_positions = [k for k, v in grid.items() if v == target[0]]
    found = []

    for pos in start_positions:
        for direction in dirs:
            word = check_direction(grid, pos, direction, len(target))
            if word == target:
                found.append((pos, direction))

    return found

def part1(data):
    grid = parse(data)
    locations = word_search(grid, "XMAS")
    return len(locations)

def part2(data):
    grid = parse(data)

    a_locations = [pos for pos, char in grid.items() if char == "A"]

    count = 0
    for x, y in a_locations:
        opposite_m = False
        last_m = None
        m = 0
        s = 0
        for dx, dy in [(-1, 1), (-1, -1), (1, 1), (1, -1)]:
            char = grid.get((x + dx, y + dy))
            if char == "M":
                m += 1
                if last_m is None:
                    last_m = (dx, dy)
                elif dx == -last_m[0] and dy == -last_m[1]:
                    opposite_m = True
                    break
            elif char == "S":
                s += 1
            else:
                break
        if m == s == 2 and not opposite_m:
            count += 1

    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some input file.")
    parser.add_argument("--test", action="store_true", help="Run with test data")
    args = parser.parse_args()
    
    if args.test:
        data_path = "test_data/day4.txt"
    else:
        data_path = "inputs/day4.txt"
    
    with open(data_path) as file:
        data = file.read()

    print(part1(data))
    print(part2(data))
