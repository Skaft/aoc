from collections import deque

DIRECTIONS = [(0,-1), (-1,0), (1,0), (0,1)]

def iter_neighbors(x, y, nodes):
    """Generate neighboring nodes of (x, y)"""
    for i, j in DIRECTIONS:
        neighbor = (x + i, y + j)
        if neighbor in nodes:
            yield neighbor

def dijkstra(pos, nodes, goal):
    """
    Given a set of valid nodes (x,y) to step on, a starting position (x, y) and
    a goal node, return the shortest path from pos to goal.
    """
    visited = set()
    queue = deque([(pos, 0)])
    while len(queue) != 0:
        pos, steps = queue.popleft()
        visited.add(pos)
        for neighbor in iter_neighbors(*pos, nodes):
            if neighbor in visited:
                continue
            if neighbor == goal:
                return steps + 1
            queue.append((neighbor, steps + 1))
