with open("inputs/day10.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:
    dir_to_diff = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }
    diff_to_dir = {diff: dir for dir, diff in dir_to_diff.items()}
    direction_opposites = dict(zip("NSEW", "SNWE"))

    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.pipe = []
        self.pipe_set = set()
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

        # fill start position with correct pipe directions
        r, c = self.start
        dirs = ""
        for dir in "NESW":
            dr, dc = self.dir_to_diff[dir]
            opposite = self.direction_opposites[dir]
            if opposite in self.tiles.get((r + dr, c + dc), ""):
                dirs += dir
        self.tiles[self.start] = dirs

    def move_along_pipe(self, node, direction):
        # take one step in given direction
        r, c = node
        dr, dc = self.dir_to_diff[direction]
        next_node = (r + dr, c + dc)

        # fetch the direction that isn't backwards
        backward_dir = self.direction_opposites[direction]
        dirs = self.tiles[next_node]
        next_direction = dirs[1 - dirs.index(backward_dir)]

        return next_node, next_direction

    def find_pipe(self):
        """Starting at start position, move one lap along the pipe and store the path taken"""
        self.pipe = [self.start]
        direction = self.tiles[self.start][0]

        while True:
            node = self.pipe[-1]
            next_node, direction = self.move_along_pipe(node, direction)

            if next_node == self.start:
                self.pipe_set = set(self.pipe)
                return

            self.pipe.append(next_node)

    def main(self):
        self.find_pipe()
        return len(self.pipe) // 2


class PartTwo(PartOne):
    def neighbors_of(self, node):
        r, c = node
        yield r + 1, c
        yield r - 1, c
        yield r, c + 1
        yield r, c - 1

    def generate_cell_groups(self):
        self.height = len(self.raw_input.splitlines())
        self.width = len(self.raw_input.splitlines()[0])
        ungrouped_cells = {
            (r, c)
            for r in range(self.height)
            for c in range(self.width)
            if (r, c) not in self.pipe_set
        }

        # build groups of adjacent cells using flood-fill
        groups = []
        while ungrouped_cells:
            group_origin = ungrouped_cells.pop()
            unexpanded_cells = {group_origin}
            group = {group_origin}

            while unexpanded_cells:
                cell = unexpanded_cells.pop()
                for neighbor in self.neighbors_of(cell):
                    if neighbor in ungrouped_cells:
                        ungrouped_cells.remove(neighbor)
                        group.add(neighbor)
                        unexpanded_cells.add(neighbor)

            groups.append(group)
        return groups

    def count_layers(self, group):
        """Count how many 'layers' of pipe pass around the group"""
        R, c = min(group)

        pipe_cells_above = [(r, c) for r in range(R, -1, -1) if (r, c) in self.pipe_set]
        dirs_above = "".join(self.tiles[cell] for cell in pipe_cells_above)

        return min(dirs_above.count("E"), dirs_above.count("W"))

    def main(self):
        self.find_pipe()
        groups = self.generate_cell_groups()

        total = 0
        for group in groups:
            if self.count_layers(group) % 2 == 1:
                total += len(group)

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
    sol.find_pipe()
    areas = sol.generate_cell_groups()
    sizes = sorted([len(area) for area in areas])
    assert sizes == [1, 1, 1, 1, 1, 2, 2, 3, 5, 7, 15, 21]
