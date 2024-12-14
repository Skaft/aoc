
N, S, E, W = 0, 1, 2, 3


def parse(data):
    plots = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            plots[x, y] = char
    return plots

def neighbors_of(pos):
    x, y = pos
    return [(x, y - 1), (x, y + 1), (x + 1, y), (x - 1, y)]


def get_regions(plots):
    regions = []
    unchecked_plots = set(plots.keys())
    while unchecked_plots:
        region = set()
        queue = [unchecked_plots.pop()]
        while queue:
            plot = queue.pop()
            region.add(plot)

            for neighbor in neighbors_of(plot):
                if neighbor in unchecked_plots and plots.get(neighbor) == plots[plot]:
                    queue.append(neighbor)
                    unchecked_plots.remove(neighbor)

        regions.append(region)
    return regions

def part1(data):
    plots = parse(data)

    regions = get_regions(plots)

    total = 0

    for region in regions:
        area = len(region)
        perimeter = 0
        for plot in region:
            for neighbor in neighbors_of(plot):
                if plots.get(neighbor) != plots[plot]:
                    perimeter += 1
        total += area * perimeter

    return total

def get_walls(region, plots):
    walls = set()

    for plot in region:
        for direction, neighbor in zip((N, S, E, W), neighbors_of(plot)):
            if plots.get(neighbor) != plots[plot]:
                walls.add((*neighbor, direction))
    
    return walls

def merge(wall_segments):
    walls = []
    for x, y, direction in wall_segments:

        if direction in (N, S):
            neighbors = [(x - 1, y), (x + 1, y)]
        else:
            neighbors = [(x, y + 1), (x, y - 1)]
        matched_walls = []
        for (nx, ny) in neighbors:
            nb = (nx, ny, direction)
            if nb in wall_segments:
                for wall in walls:
                    if nb in wall:
                        wall.add((x, y, direction))
                        matched_walls.append(wall)
        if len(matched_walls) > 1:
            for w in matched_walls:
                walls.remove(w)
            walls.append(set.union(*matched_walls))
        elif not matched_walls:
            walls.append({(x, y, direction)})
    return walls

def part2(data):
    plots = parse(data)

    regions = get_regions(plots)
    total = 0
    for region in regions:
        area = len(region)
        wall_segments = get_walls(region, plots)

        sides = len(merge(wall_segments))

        total += area * sides
    
    return total



if __name__ == "__main__":
    from common import get_input

    data = get_input(day=12)

    print(part1(data))
    print(part2(data))
