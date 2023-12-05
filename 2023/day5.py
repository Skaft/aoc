import re


with open("inputs/day5.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class Table:
    def __init__(self, number_grid):
        self._grid = number_grid
        self.source_column = [row[1] for row in number_grid]

    def convert(self, source):
        for dest_start, source_start, length in self._grid:
            diff = source - source_start
            if 0 <= diff < length:
                return dest_start + diff
        return source

    def convert_backward(self, dest):
        for dest_start, source_start, length in self._grid:
            diff = dest - dest_start
            if 0 <= diff < length:
                return source_start + diff
        return dest


class PartOne:

    def __init__(self, raw_input):
        seed_section, *table_sections = raw_input.split("\n\n")

        self.seeds = [int(n) for n in re.findall(r"\d+", seed_section)]
        self.tables = []

        for section in table_sections:
            title_line, *table_strings = section.splitlines()
            number_grid = [[int(n) for n in line.split()] for line in table_strings]
            self.tables.append(Table(number_grid))

    def go_downstream(self, number, table_index=0):
        for table in self.tables[table_index:]:
            number = table.convert(number)
        return number

    def main(self):
        min_loc = float("inf")

        for seed in self.seeds:
            location = self.go_downstream(seed)
            if location < min_loc:
                min_loc = location
        return min_loc


class PartTwo(PartOne):

    def has_seed(self, seed):
        number_pairs = zip(self.seeds[::2], self.seeds[1::2])
        for start, length in number_pairs:
            if start <= seed < start + length:
                return True
        return False

    def go_upstream(self, number, table_index):
        for table in reversed(self.tables[:table_index]):
            number = table.convert_backward(number)
        return number

    def main(self):
        min_loc = float("inf")

        for i, table in enumerate(self.tables):
            boundaries = table.source_column
            for number in boundaries:
                location = self.go_downstream(number, i)
                if location >= min_loc:
                    continue
                seed = self.go_upstream(number, i)
                if self.has_seed(seed):
                    min_loc = location

        return min_loc


if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_input_is_parsed_correctly():
    sol = PartOne(test_inputs[0])
    assert sol.seeds == [79, 14, 55, 13]
    expected_soil = [81, 14, 57, 13]
    for seed, soil in zip(sol.seeds, expected_soil):
        assert sol.convert("seed-to-soil", seed) == soil

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 35

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 46
