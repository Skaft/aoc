import pytest

from helpers import AoCSolution


DAY = 18


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        cubes = set()
        for line in raw_input.splitlines():
            cube = tuple(map(int, line.split(",")))
            cubes.add(cube)
        return cubes

    @staticmethod
    def neighbors(cube):
        x, y, z = cube
        yield x + 1, y, z
        yield x - 1, y, z
        yield x, y + 1, z
        yield x, y - 1, z
        yield x, y, z + 1
        yield x, y, z - 1

    def empty_neighbors(self, cubes):
        for cube in cubes:
            for nb in self.neighbors(cube):
                if nb not in cubes:
                    yield nb

    def main(self, cubes):
        return len(list(self.empty_neighbors(cubes)))

class PartTwo(PartOne):
    def get_boundaries(self, cube_set):
        minX = minY = minZ = float("inf")
        maxX = maxY = maxZ = -float("inf")

        for x, y, z in cube_set:
            if x < minX:
                minX = x
            elif x > maxX:
                maxX = x
            if y < minY:
                minY = y
            elif y > maxY:
                maxY = y
            if z < minZ:
                minZ = z
            elif z > maxZ:
                maxZ = z

        return minX, maxX, minY, maxY, minZ, maxZ

    def flood_fill(self, boundaries, cubes):
        minX, maxX, minY, maxY, minZ, maxZ = boundaries
        start = minX, minY, minZ
        flooded = set()
        unvisited = [start]
        while unvisited:
            pos = unvisited.pop()
            flooded.add(pos)
            for nb in self.neighbors(pos):
                if nb in flooded:
                    continue
                if nb in cubes:
                    continue
                x, y, z = nb
                if not (minX <= x <= maxX):
                    continue
                if not (minY <= y <= maxY):
                    continue
                if not (minZ <= z <= maxZ):
                    continue
                unvisited.append(nb)
        return flooded

    def main(self, cubes):
        empty = set(self.empty_neighbors(cubes))
        boundaries = self.get_boundaries(empty)
        flooded = self.flood_fill(boundaries, cubes)
        exterior_sides = sum(nb in flooded for nb in self.empty_neighbors(cubes))
        return exterior_sides


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 64

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 58
