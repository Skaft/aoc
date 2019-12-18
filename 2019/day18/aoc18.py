"""
Future me might clean this.
"""


from input import data, data2
from pathfind import dijkstra, iter_neighbors
from collections import deque, defaultdict
from itertools import combinations


def parse(string):
    keys = {}
    doors = {}
    nodes = set()
    positions = []
    for y, line in enumerate(string.split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                continue
            if char == '.':
                nodes.add((x, y))
            elif char == '@':
                positions.append((x, y))
                nodes.add((x, y))
            elif char.islower():
                keys[char] = (x, y)
            elif char.isupper():
                doors[char] = (x, y)
    return positions, keys, doors, nodes

def key_paths(keys, nodes, doors):
    pair_paths = defaultdict(dict)
    nodes = {*nodes, *doors.values(), *keys.values()}
    for k1, k2 in combinations(sorted(keys), 2):
        shortest = dijkstra(keys[k1], nodes, keys[k2])
        pair_paths[k1, k2] = shortest
        pair_paths[k2, k1] = shortest
    return pair_paths

def key_paths2(pos, keys, nodes, doors):
    pair_paths = defaultdict(int)
    nodes = {*nodes, *doors.values(), *keys.values()}
    for k1, k2 in combinations(sorted(keys), 2):
        shortest = dijkstra(keys[k1], nodes, keys[k2])
        if shortest:
            pair_paths[k1, k2] = shortest
            pair_paths[k2, k1] = shortest
    for k, keypos in keys.items():
        for p in pos:
            shortest = dijkstra(p, nodes, keypos)
            if shortest:
                pair_paths['@', k] = shortest
                break
    return pair_paths

def identify_blockers(pos, keys, doors, nodes):
    pos_to_key = {p:k for k, p in keys.items()}
    pos_to_door = {p:d for d, p in doors.items()}
    all_nodes = {*nodes, *pos_to_key, *pos_to_door}
    visited=set()
    queue = deque([(pos, [])])
    blocked_by = {}
    while queue:
        pos, blockers = queue.popleft()
        visited.add(pos)
        for nb in iter_neighbors(*pos, all_nodes):
            if nb in visited:
                continue
            if nb in pos_to_door:
                queue.append((nb, blockers + [pos_to_door[nb].lower()]))
            elif nb in pos_to_key:
                blocked_by[pos_to_key[nb]] = blockers.copy()
                queue.append((nb, blockers + [pos_to_key[nb]]))
            else:
                queue.append((nb, blockers))
    blocked_by = {k:list(set(blockers)) for k, blockers in blocked_by.items()}
    return blocked_by


def part1(string):
    pos, keys, doors, nodes = parse(string)
    pos = pos[0]
    blocked_by = identify_blockers(pos, keys, doors, nodes)
    pair_dists = key_paths({**keys, '@':pos}, nodes, doors)

    order = ['@']
    options = [[k for k, b in blocked_by.items() if not b]]
    keycount = len(blocked_by) + 1
    states_found = {}
    best = float('inf')
    while options:
        options_for_next_key = options[-1]
        if not options_for_next_key:
            if len(order) == keycount:
                dist = sum(pair_dists[pair] for pair in zip(order, order[1:]))
                if dist < best:
                    best = dist
            options.pop()
            order.pop()
            continue
        next_key = options_for_next_key.pop()

        state = (frozenset(order[1:]), next_key)
        order.append(next_key)
        distance = sum(pair_dists[pair] for pair in zip(order, order[1:]))
        if state in states_found:
            if distance >= states_found[state]:
                order.pop()
                continue

        states_found[state] = distance
        available_keys = [
            k
            for k, blockers in blocked_by.items()
            if k not in order
            and all(b in order for b in blockers)
        ]
        options.append(available_keys)
    print(best)


def part2(string):
    global pair_dists
    pos, keys, doors, nodes = parse(string)

    blocked_by_list = [
        identify_blockers(pos[0], keys, doors, nodes),
        identify_blockers(pos[1], keys, doors, nodes),
        identify_blockers(pos[2], keys, doors, nodes),
        identify_blockers(pos[3], keys, doors, nodes),
    ]
    pair_dists = key_paths2(pos, keys, nodes, doors)

    order = ['@']
    suborders = [['@'] for _ in range(4)]

    get_suborder = {
        k: suborders[i]
        for i, keys in enumerate(blocked_by_list)
        for k in keys
    }
    get_suborder['@'] = ['@']
    options = [[k
                for blocked_by in blocked_by_list
                for k, b in blocked_by.items() if not b]]
    keycount = len(keys) + 1

    states_found = {}
    best = float('inf')

    while options:
        options_for_next_key = options[-1]
        if not options_for_next_key:

            if len(order) == keycount:
                distance = sum(pair_dists[pair]
                       for sub in suborders
                       for pair in zip(sub, sub[1:])
                       )
                if distance < best:
                    best = distance
            options.pop()
            k = order.pop()
            get_suborder[k].pop()
            continue
        next_key = options_for_next_key.pop()
        suborder = get_suborder[next_key]
        suborder.append(next_key)
        state = (frozenset(order[1:]), *(sub[-1] for sub in suborders))
        distance = sum(pair_dists[pair]
                       for sub in suborders
                       for pair in zip(sub, sub[1:])
                       )
        if state in states_found:
            if distance >= states_found[state]:

                suborder.pop()
                continue
        order.append(next_key)
        states_found[state] = distance
        available_keys = [
            k
            for blocked_by in blocked_by_list
            for k, blockers in blocked_by.items()
            if k not in order
            and all(b in order for b in blockers)
        ]
        options.append(available_keys)
    print(best)

part1(data)
part2(data2)
