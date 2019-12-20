from collections import deque

DIRECTIONS = [(0,-1), (-1,0), (1,0), (0,1)]

def dijkstra(pos, goal, nodes, leads_to):
    def iter_neighbors(x, y):
        """Generate neighboring nodes of (x, y)"""
        for i, j in DIRECTIONS:
            neighbor = (x + i, y + j)
            if neighbor in nodes:
                yield neighbor
        if (x, y) in leads_to:
            yield leads_to[x, y]

    visited = set()
    queue = deque([(pos, 0)])
    while len(queue) != 0:
        pos, steps = queue.popleft()
        visited.add(pos)
        for neighbor in iter_neighbors(*pos):
            if neighbor in visited:
                continue
            if neighbor == goal:
                return steps + 1
            queue.append((neighbor, steps + 1))

def dijkstra2(pos, goal, nodes, out_to_in, in_to_out):
    def iter_neighbors(x, y, z):
        """Generate neighboring nodes of (x, y)"""
        for i, j in DIRECTIONS:
            neighbor = (x + i, y + j)
            if neighbor in nodes:
                yield (*neighbor, z)
        if (x, y) in in_to_out:
            yield (*in_to_out[x, y], z + 1)
        elif z != 0 and (x, y) in out_to_in:
            yield (*out_to_in[x, y], z - 1)

    visited = set()
    queue = deque([((*pos, 0), 0)])
    goal = (*goal, 0)
    while len(queue) != 0:
        pos, steps = queue.popleft()
        visited.add(pos)
        for neighbor in iter_neighbors(*pos):
            if neighbor in visited:
                continue
            if neighbor == goal:
                return steps + 1
            queue.append((neighbor, steps + 1))