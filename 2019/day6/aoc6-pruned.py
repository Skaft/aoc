from input import data
from collections import defaultdict


def parse_input(string):
    """
    Turn the string input into a dict describing the orbits.

    Each object is mapped to a list of its closest (outer) orbiting objects.
    """

    orbits = defaultdict(list)
    for line in string.split('\n'):
        inner, outer = line.split(')')
        orbits[inner].append(outer)

    return dict(orbits)


def fill_paths(orbits, start='COM'):
    """Return a dict with the path from start to each object in orbits."""

    def recurse(planet, path, paths={}):
        for outer in orbits.get(planet, []):
            paths[outer] = path
            recurse(outer, path + [outer])
        return paths

    return recurse(start, [start])


orbits = parse_input(data)
paths = fill_paths(orbits)

# part 1
print(sum(len(path) for path in paths.values()))

# part 2
unique_nodes = set(paths['SAN']) ^ set(paths['YOU'])
print(len(unique_nodes))
