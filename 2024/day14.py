import re
import math

def parse(data):
    coordinates = re.compile(r"-?\d+")
    robots = [list(map(int, re.findall(coordinates, line))) for line in data.splitlines()]

    max_x = max(x for x, _, _, _ in robots)
    max_y = max(y for _, y, _, _ in robots)

    return robots, (max_x, max_y)


def part1(data):
    seconds = 100

    robots, (max_x, max_y) = parse(data)

    quadrant_populations = [0,0,0,0]

    for x, y, vx, vy in robots:
        final_x = (x + seconds * vx) % (max_x + 1)
        final_y = (y + seconds * vy) % (max_y + 1)

        if final_x == max_x // 2 or final_y == max_y // 2:
            continue
        if final_x < max_x / 2:
            if final_y < max_y / 2:
                quadrant_populations[0] += 1
            else:
                quadrant_populations[2] += 1
        else:
            if final_y < max_y / 2:
                quadrant_populations[1] += 1
            else:
                quadrant_populations[3] += 1

    return math.prod(quadrant_populations)

def draw(robots, grid_dims):
    max_x, max_y = grid_dims
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y, _, _ in robots:
        grid[y][x] = '█'
    for row in grid:
        print(''.join(row))

def part2(data):
    robots, (max_x, max_y) = parse(data)

    seconds = 0

    # horizontal_neighbors_max = 0

    while True:
        new_robots = set()
        horizontal_neighbors = 0
        for x, y, vx, vy in robots:

            new_x = (x + vx) % (max_x + 1)
            new_y = (y + vy) % (max_y + 1)

            new_robots.add((new_x, new_y, vx, vy))


        for x, y, *_ in new_robots:
            for nx, ny , *_ in new_robots:
                if nx == x - 1 and ny == y:
                    horizontal_neighbors += 1
                    break

        seconds += 1
        if horizontal_neighbors > 100:
            # horizontal_neighbors_max = horizontal_neighbors
            draw(new_robots, (max_x, max_y))
            # print(seconds, horizontal_neighbors_max)
            # if input("Stop? ") == "q":
            return seconds
            # print("searching...")
        robots = new_robots

if __name__ == "__main__":
    from common import get_input

    data = get_input(day=14)

    print(part1(data))
    print(part2(data))