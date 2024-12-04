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
    locations = word_search(grid, "MAS")

    count = 0
    for (pos1, dir1), (pos2, dir2) in itertools.combinations(locations, 2):
        x1, y1 = pos1
        x2, y2 = pos2
        dists = (abs(x1 - x2), abs(y1 - y2))
        if dists == (0, 2) or dists == (2, 0):
            dx1, dy1 = dir1
            dx2, dy2 = dir2
            A1 = x1 + dx1, y1 + dy1
            A2 = x2 + dx2, y2 + dy2
            if A1 == A2:
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