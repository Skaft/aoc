from input import data

from collections import deque
from computer import Computer


DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
N,S,W,E = DIRECTIONS
WALL = '█'
OPEN = '.'
GOAL = '¤'
board = {(0,0): OPEN}

def parse(string):
    return [int(n) for n in string.split(',')]

def map_neighbors():
    new_moves = []
    for d in (1,2,3,4):
        out, nb = move(d)
        if out == 0:
            board[nb] = WALL
            continue
        if nb not in board:
            new_moves.append(d)
        if out == 1:
            board[nb] = OPEN
        elif out == 2:
            board[nb] = GOAL
        if d % 2 == 0:
            rev = d - 1
        else:
            rev = d + 1
        move(rev)
    return new_moves

def move(i):
    if isinstance(i, str):
        i = 'nswe'.index(i.lower()) + 1
    comp.send(i)
    comp.run()
    o = comp.collect()
    dx, dy = DIRECTIONS[i - 1]
    nb = position[0] + dx, position[1] + dy
    return o, nb

def follow_path(path):
    global position
    for i in path:
        o, nb = move(i)
        if o:
            position = nb

def part1(string):
    global comp, position
    program = parse(string)
    paths = deque([[]])
    while paths:
        path = paths.popleft()
        position = [0, 0]
        comp = Computer(program)
        follow_path(path)
        while True:
            new_moves = map_neighbors()
            if not new_moves:
                break
            take, *others = new_moves
            for other_choice in others:
                paths.append(path + [other_choice])
            o, nb = move(take)
            path.append(take)
            position = nb
            if board[nb] == GOAL:
                print(len(path))

def draw():
    xvals = [x for x, y in board]
    yvals = [y for x, y in board]
    xmin, xmax = min(xvals), max(xvals)
    ymin, ymax = min(yvals), max(yvals)
    wid = xmax - xmin + 1
    hei = ymax - ymin + 1
    rows = [[' '] * wid for _ in range(hei)]
    for (x, y), char in board.items():
        rows[y - ymin][x - xmin] = char
    x, y = position
    rows[y - ymin][x - xmin] = 'o'
    for row in rows:
        print(''.join(row))

def neighbors(x, y):
    for i, j in (N,W,S,E):
        neighbor = (x + i, y + j)
        if neighbor in nodes:
            yield neighbor

def dijkstra(nodes, pos):
    dists = {pos: 0}
    queue = deque([pos])
    while len(queue) != 0:
        pos = queue.popleft()
        dist = dists[pos]
        for neighbor in neighbors(*pos):
            if neighbor in dists:
                continue
            dists[neighbor] = dist + 1
            queue.append(neighbor)
    print(max(dists.values()))

#part 1
part1(data)

#part 2
nodes = set()
for k, v in board.items():
    if v == GOAL:
        oxygen = k
    elif v == OPEN:
        nodes.add(k)
dijkstra(nodes, oxygen)
