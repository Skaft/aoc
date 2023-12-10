with open("inputs/day10.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.tiles = {}
        charmap = {
            "L": "NE",
            "|": "NS",
            "J": "NW",
            "F": "ES",
            "-": "EW",
            "7": "SW",
        }
        for r, line in enumerate(raw_input.splitlines()):
            for c, char in enumerate(line):
                if char == ".":
                    continue
                if char == "S":
                    self.start = (r, c)
                else:
                    self.tiles[r, c] = charmap[char]

        # connect start
        r,c = self.start
        dirs = ""
        if "S" in self.tiles.get((r - 1, c), ""):
            dirs += "N"
        if "W" in self.tiles.get((r, c + 1), ""):
            dirs += "E"
        if "N" in self.tiles.get((r + 1, c), ""):
            dirs += "S"
        if "E" in self.tiles.get((r, c - 1), ""):
            dirs += "W"
        self.tiles[self.start] = dirs

    def is_connected(self, node1, node2):
        if node1 not in self.tiles or node2 not in self.tiles:
            return False

        diff_r = node2[0] - node1[0]
        diff_c = node2[1] - node1[1]
        if abs(diff_c) + abs(diff_r) != 1:
            return False

        c1 = self.tiles[node1]
        c2 = self.tiles[node2]

        if diff_r == 1 and "S" in c1 and "N" in c2:
            return True
        if diff_r == -1 and "N" in c1 and "S" in c2:
            return True
        if diff_c == 1 and "E" in c1 and "W" in c2:
            return True
        if diff_c == -1 and "W" in c1 and "E" in c2:
            return True

        return False

    def neighbors_of(self, node):
        r, c = node
        yield r + 1, c
        yield r - 1, c
        yield r, c + 1
        yield r, c - 1

    def find_path(self):
        self.path = [self.start]
        visited = set()

        while True:
            node = self.path[-1]
            visited.add(node)
            for nb in self.neighbors_of(node):
                if nb == self.start:
                    if len(self.path) < 3:
                        continue
                    if self.is_connected(node, self.start):
                        return
                if nb in visited:
                    continue
                if self.is_connected(node, nb):
                    self.path.append(nb)
                    break

    def main(self):
        self.find_path()
        return len(self.path) // 2


class PartTwo(PartOne):
    def flood_fill(self):
        self.height = len(self.raw_input.splitlines())
        self.width = len(self.raw_input.splitlines()[0])
        cells = {(r, c) for r in range(self.height) for c in range(self.width)}

        for cell in self.path:
            cells.remove(cell)
        
        areas = []
        while cells:
            origin = cells.pop()
            q = {origin}
            area = {origin}
            while q:
                node = q.pop()
                for nb in self.neighbors_of(node):
                    if nb in cells:
                        cells.remove(nb)
                        area.add(nb)
                        q.add(nb)
            areas.append(area)
        return areas

    def count_layers(self, area):
        R, c = min(area)

        pipe_cells_above = [(r, c) for r in range(R, -1, -1) if (r, c) in self.path]
        dirs_above = "".join(self.tiles[r, c] for r, c in pipe_cells_above)

        return min(dirs_above.count("E"), dirs_above.count("W"))

    def main(self):
        self.find_path()
        areas = self.flood_fill()

        total = 0

        for area in areas:
            if self.count_layers(area) % 2 == 1:
                total += len(area)

        return total

if __name__ == "__main__":

    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS


def test_part1_main():
    assert PartOne(test_inputs[0]).main() == 8

def test_part2_main():
    assert PartTwo(test_inputs[1]).main() == 4
    assert PartTwo(test_inputs[2]).main() == 8
    assert PartTwo(test_inputs[3]).main() == 10

def test_find_areas():
    sol = PartTwo(test_inputs[2])
    sol.find_path()
    areas = sol.flood_fill()
    sizes = sorted([len(area) for area in areas])
    assert sizes == [1,1,1,1,1,2,2,3,5,7,15,21]
