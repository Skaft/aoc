import pytest

from helpers import AoCSolution


DAY = 14


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        world = {}
        for line in raw_input.splitlines():
            points = [tuple(map(int, point.split(","))) for point in line.split(" -> ")]
            for start, stop in zip(points, points[1:]):
                for point in self.gen_points(start, stop):
                    world[point] = "#"

        self.minX = min(x for x, y in world)
        self.maxX = max(x for x, y in world)  
        self.minY = 0
        self.maxY = max(y for x, y in world)
        return world
    
    def gen_points(self, start, stop):
        x1, y1 = start
        x2, y2 = stop
        if x1 == x2:
            dy = 1 if y2 > y1 else -1
            dx = 0
        elif y1 == y2:
            dx = 1 if x2 > x1 else -1
            dy = 0
        x, y = start
        while (x, y) != stop:
            yield (x, y)
            x += dx
            y += dy
        yield stop

    def display(self, world):
        width = self.maxX - self.minX
        height = self.maxY - self.minY
        grid = [["."] * (width + 1) for _ in range(height + 1)]
        for (x, y), val in world.items():
            grid[y - self.minY][x - self.minX] = val
        print()
        grid[0][500 - self.minX] = "+"
        for row in grid:
            print("".join(row))

    def drop_grain(self, world):
        x, y = 500, 0
        while True:
            fall_spots = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
            at_rest = True
            for pos in fall_spots:
                if pos in world:
                    continue  # occupied
                elif (
                    not (self.minX <= pos[0] <= self.maxX) or 
                    not (self.minY <= pos[1] <= self.maxY)
                ):
                    return -1  # void
                else:
                    at_rest = False
                    x, y = pos
                    break  # fall to pos
            if at_rest:
                world[x, y] = "o"
                return

    def main(self, world):
        counts = 0
        while self.drop_grain(world) != -1:
            counts += 1
        return counts


class PartTwo(PartOne):
    def drop_grain(self, world):
        x, y = 500, 0
        while True:
            fall_spots = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
            at_rest = True
            for pos in fall_spots:
                if pos in world or pos[1] == self.maxY + 2:
                    continue  # occupied
                else:
                    at_rest = False
                    x, y = pos
                    break  # fall to pos
            if at_rest:
                world[x, y] = "o"
                if (x, y) == (500, 0):
                    return -1
                return

    def main(self, world):
        return super().main(world) + 1




if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    print(PartTwo(DAY).run(0))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 24

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == 93