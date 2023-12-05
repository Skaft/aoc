import re


with open("inputs/day5.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class PartOne:

    def __init__(self, raw_input):
        seed_section, *map_sections = raw_input.split("\n\n")

        self.seeds = [int(n) for n in re.findall(r"\d+", seed_section)]
        self.maps = {}

        for section in map_sections:
            title_line, *map_lines = section.splitlines()
            title = title_line.split()[0]
            self.maps[title] = [[int(n) for n in line.split()] for line in map_lines]
    
    def convert(self, conversion_type, source):
        for dest_start, source_start, length in self.maps[conversion_type]:
            diff = source - source_start
            if 0 <= diff < length:
                return dest_start + diff
        return source


    def main(self):
        min_loc = float("inf")

        for seed in self.seeds:
            number = seed
            for conversion_type in self.maps:
                number = self.convert(conversion_type, number)
            if number < min_loc:
                min_loc = number
        return min_loc


class PartTwo(PartOne):

    def convert_backward(self, conversion_type, source):
        for source_start, dest_start, length in self.maps[conversion_type]:
            diff = source - source_start
            if 0 <= diff < length:
                return dest_start + diff
        return source

    def has_seed(self, seed):
        for start, length in zip(self.seeds[::2], self.seeds[1::2]):
            if start <= seed < start + length:
                return True
        return False

    def go_downstream(self, map_index, number):
        conversion_types = list(self.maps.keys())
        for type in conversion_types[map_index:]:
            number = self.convert(type, number)
        return number

    def go_upstream(self, map_index, number):
        conversion_types = list(self.maps.keys())
        for type in reversed(conversion_types[:map_index]):
            number = self.convert_backward(type, number)
        return number

    def main(self):
        min_loc = PartOne(true_input).main()

        maps = list(self.maps.values())
        for index, map in enumerate(maps):
            for _, source, _ in map:
                loc = self.go_downstream(index, source)
                if loc < min_loc:
                    seed = self.go_upstream(index, source)
                    if self.has_seed(seed):
                        min_loc = loc
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
