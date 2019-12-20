from input import data
from collections import defaultdict
from pathfind import dijkstra, dijkstra2


def parse(string):
    maxy = 104
    maxx = 108
    thickness = 27

    nodes = set()
    inners = defaultdict(list)
    outers = defaultdict(list)
    for y, line in enumerate(string.split('\n'), -3):
        for x, char in enumerate(line, -2):
            if char == '.':
                nodes.add((x, y))
            elif 'A' <= char <= 'Z':

                # outer portals
                if x < 0:
                    outers[0, y].append(char)
                elif y < 0:
                    outers[x, 0].append(char)
                elif x > maxx:
                    outers[maxx, y].append(char)
                elif y > maxy:
                    outers[x, maxy].append(char)

                # inner portals
                elif x < thickness + 2:
                    inners[thickness - 1, y].append(char)
                elif y < thickness + 2:
                    inners[x, thickness - 1].append(char)
                elif x > maxx - thickness - 2:
                    inners[maxx - thickness + 1, y].append(char)
                elif y > maxy - thickness - 2:
                    inners[x, maxy - thickness + 1].append(char)

    inners = {''.join(name): pos for pos, name in inners.items()}
    outers = {''.join(name): pos for pos, name in outers.items()}

    start = outers.pop('AA')
    end = outers.pop('ZZ')

    out_to_in = {}
    in_to_out = {}
    for name, outer_pos in outers.items():
        inner_pos = inners[name]
        out_to_in[outer_pos] = inner_pos
        in_to_out[inner_pos] = outer_pos

    return start, end, nodes, out_to_in, in_to_out


start, end, nodes, out_to_in, in_to_out = parse(data)

# part 1
leads_to = {**out_to_in, **in_to_out}
print(dijkstra(start, end, nodes, leads_to))

# part2
print(dijkstra2(start, end, nodes, out_to_in, in_to_out))
