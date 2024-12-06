import argparse


char_to_dir = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0)
}

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def parse(data):
    global MIN_X, MAX_X, MIN_Y, MAX_Y

    blocks = set()
    guard_pos = None
    guard_dir = None
    
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                blocks.add((x, y))
            elif char != ".":
                guard_pos = (x, y)
                guard_dir = char_to_dir[char]
    
    MIN_Y = 0
    MIN_X = 0
    MAX_X = x
    MAX_Y = y

    return blocks, guard_pos, guard_dir


def get_path(pos, dir, blocks):
    path = {(pos, dir)}

    x, y = pos
    dx, dy = dir
    dir_i = dirs.index(dir)

    while True:

        # move forward until blocked or out of bounds
        while True:
            new_pos = (x + dx, y + dy)
            if new_pos in blocks:
                break

            x, y = new_pos
            if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y:
                return path

            if (new_pos, (dx, dy)) in path:
                raise ValueError("Loop detected")

            path.add((new_pos, (dx, dy)))

        # turn right
        dir_i = (dir_i + 1) % 4
        dx, dy = dirs[dir_i]

def part1(data):
    blocks, guard_pos, guard_dir = parse(data)
    path = get_path(guard_pos, guard_dir, blocks)
    positions = {pos for pos, _ in path}
    return len(positions)


def part2(data):
    blocks, guard_pos, guard_dir = parse(data)
    path = get_path(guard_pos, guard_dir, blocks)
    visited_cells = {pos for pos, _ in path}

    possible_placements = visited_cells - {guard_pos}
    loops = 0
    for pos in possible_placements:
        try:
            get_path(guard_pos, guard_dir, blocks | {pos})
        except ValueError:
            loops += 1

    return loops
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some input file.")
    parser.add_argument("--test", action="store_true", help="Run with test data")
    args = parser.parse_args()

    if args.test:
        data_path = "test_data/day6.txt"
    else:
        data_path = "inputs/day6.txt"

    with open(data_path) as file:
        data = file.read()

    print(part1(data))
    print(part2(data))
