import re

import pytest

from helpers import AoCSolution


DAY = 19


class Blueprint:
    def __init__(self, id_, ore_cost, clay_cost, obs_cost1, obs_cost2, geo_cost1, geo_cost2, mins=24):
        self._id = id_
        self.costs = [
            (ore_cost, 0, 0, 0),
            (clay_cost, 0, 0, 0),
            (obs_cost1, obs_cost2, 0, 0),
            (geo_cost1, 0, geo_cost2, 0),
        ]
        self.mins = mins

    @property
    def quality_level(self):
        return self._id * self.max_geodes()

    def max_geodes(self):
        best = 0
        best_times = {}
        best_geodes = {}
        def inner(resources, robots, minleft):
            if minleft == 0:
                nonlocal best
                if resources[3] > best:
                    best = resources[3]
                return

            if best_geodes.get(robots[3] + 1, -1) > minleft:
                return

            options = []
            for i, cost in enumerate(self.costs):
                if all(c <= r for c, r in zip(cost, resources)):
                    options.append(i)
            for i, n in enumerate(robots):
                resources[i] += n
            for option in reversed(options):
                rest = resources.copy()
                robs = robots.copy()
                for i, c in enumerate(self.costs[option]):
                    rest[i] -= c
                robs[option] += 1
                if best_times.get(tuple(robs), -1) > minleft:
                    continue
                if option == 3:
                    best_geodes[robs[3]] = minleft
                best_times[tuple(robs)] = minleft
                inner(rest, robs, minleft - 1)
            inner(resources, robots, minleft - 1)

        inner([0, 0, 0, 0], [1, 0, 0, 0], self.mins)
        return best


class PartOne(AoCSolution):
    def clean_input(self, raw_input):
        blueprints = []
        for line in raw_input.splitlines():
            id_, ore_cost, clay_cost, obs_cost1, obs_cost2, geo_cost1, geo_cost2 = map(int, re.findall(r"\d+", line))
            blueprints.append(Blueprint(id_, ore_cost, clay_cost, obs_cost1, obs_cost2, geo_cost1, geo_cost2))
        return blueprints

    def main(self, blueprints):
        total = 0
        for bp in blueprints:
            q = bp.quality_level
            total += q
        return total


class PartTwo(PartOne):
    def main(self, blueprints):
        blueprints = blueprints[:3]
        maxes = []
        for bp in blueprints:
            bp.mins = 32
            m = bp.max_geodes()
            print(m)
            maxes.append(m)
        return maxes


if __name__ == "__main__":
    print(PartOne(DAY).run(0))
    # print(PartTwo(DAY).run(0))


# TESTS

# @pytest.mark.skip
def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1) == 33

# @pytest.mark.skip
def test_part1_quality():
    sol = PartOne(DAY)
    blueprints = sol.clean_input(sol.raw_test_inputs[0])
    assert blueprints[0].quality_level == 9
    assert blueprints[1].quality_level == 24

@pytest.mark.skip
def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1) == [56, 62]
