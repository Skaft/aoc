import collections

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
EMPTY = "."
WALL = "#"
BOX = "O"
PLAYER = "@"
BOX_L = "["
BOX_R = "]"

def parse(data):
    grid = {}

    start = None
    top, bottom = data.split("\n\n")

    for y, line in enumerate(top.splitlines()):
        for x, char in enumerate(line):
            if char == PLAYER:
                start = (x, y)
            grid[(x, y)] = char

    movechars = dict(zip("^v<>", [UP, DOWN, LEFT, RIGHT]))

    moves = [movechars[d] for line in bottom.splitlines() for d in line]

    return  grid, start, moves


def draw(grid):
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    for y in range(max_y + 1):
        print("".join(grid[(x, y)] for x in range(max_x + 1)))

    print("-" * 40)

def scale_grid(grid):
    new_grid = {}

    for (x, y), object in grid.items():
        pos_l = (x * 2, y)
        pos_r = (x * 2 + 1, y)

        if object == BOX:
            new_obj = "[]"
        elif object == PLAYER:
            new_obj = "@."
        else:
            new_obj = object * 2
        
        new_grid[pos_l] = new_obj[0]
        new_grid[pos_r] = new_obj[1]
    
    return new_grid


def part1(data):
    grid, player_pos, moves = parse(data)

    for dx, dy in moves:
        x, y = player_pos

        boxes = []

        gap = None

        while True:
            new_pos = (x + dx, y + dy)

            if new_pos not in grid:
                raise ValueError(f"Invalid position: {new_pos}, {x}, {y}, {dx}, {dy}")

            if grid[new_pos] == EMPTY:
                gap = new_pos
                break
            elif grid[new_pos] == WALL:
                break
            elif grid[new_pos] == BOX:
                boxes.append(new_pos)
                x, y = new_pos

        # blocked by wall
        if gap is None:
            continue

        # move boxes
        while boxes:
            grid[gap] = BOX
            gap = boxes.pop()

        # move player
        grid[gap] = PLAYER
        grid[player_pos] = EMPTY
        player_pos = gap

    return sum(100*y + x for (x, y), v in grid.items() if v == BOX)

def shiftables_in_line(position, direction, grid):
    x, y = position
    dx, dy = direction

    shiftables = []

    while True:
        shiftables.append((x, y))

        x += dx
        y += dy

        if grid[(x, y)] == WALL:
            return None

        if grid[(x, y)] == EMPTY:
            return shiftables

def part2(data):
    grid, player_pos, moves = parse(data)

    grid = scale_grid(grid)
    player_pos = (player_pos[0] * 2, player_pos[1])
    assert grid[player_pos] == "@"

    for dx, dy in moves:

        blocked = False

        # new_pos = (x + dx, y + dy)
        lines_to_shift = []

        spawn_from = collections.deque([player_pos])

        while spawn_from:
            
            sequence = shiftables_in_line(spawn_from.popleft(), (dx, dy), grid)
            if sequence is None:
                blocked = True
                break

            # locate branching points (unless moving sideways)
            if dy != 0:
                for x, y in sequence[1:]:
                    if grid[x, y] == BOX_L:
                        spawn_from.append((x + 1, y))
                    elif grid[x, y] == BOX_R:
                        spawn_from.append((x - 1, y))
            
            if sequence not in lines_to_shift:
                if lines_to_shift and sequence[0] == lines_to_shift[-1][-1]:
                    assert len(sequence) == 1
                    continue
                lines_to_shift.append(sequence)

        # blocked by wall
        if blocked:
            continue

        # move boxes
        while lines_to_shift:
            seq = lines_to_shift.pop()
            empties = [i for i, pos in enumerate(seq) if grid[pos] == EMPTY]
            if empties:
                seq = seq[:empties[0]]

            for x, y in reversed(seq):
                grid[x + dx, y + dy] = grid[x, y]
            
            if seq:
                grid[seq[0]] = EMPTY
        
        # move player
        player_pos = (player_pos[0] + dx, player_pos[1] + dy)

        # debug broken boxes
        # for (x, y), char in grid.items():
        #     if char == BOX_L and grid[(x + 1, y)] != BOX_R:
        #         breakpoint()
        #     if char == BOX_R and grid[(x - 1, y)] != BOX_L:
        #         breakpoint()

    return sum(100*y + x for (x, y), v in grid.items() if v == BOX_L)



if __name__ == "__main__":
    from common import get_input

    data = get_input(day=15)

    print(part1(data))
    print(part2(data))