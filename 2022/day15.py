import re
from dataclasses import dataclass

import pytest

from helpers import AoCSolution


DAY = 15

@dataclass
class Sensor:
    x : int
    y : int
    range : int


class PartOne(AoCSolution):
    @staticmethod
    def manhattan(pointA, pointB):
        dx = abs(pointA[0] - pointB[0])
        dy = abs(pointA[1] - pointB[1])
        return dx + dy

    def clean_input(self, raw_input):
        pattern = r"Sensor at x=(-?\d+), y=(-?\d+): "\
                  r"closest beacon is at x=(-?\d+), y=(-?\d+)"
        sensor_data = re.findall(pattern, raw_input)
        sensors = []
        beacons = []
        for data in sensor_data:
            sx, sy, bx, by = map(int, data)
            beacon = (bx, by)
            dist = self.manhattan((sx, sy), beacon)
            sensors.append(Sensor(sx, sy, dist))
            beacons.append(beacon)
        return sensors, beacons

    def count_no_beacons(self, xranges, y, beacons):
        beacon_xs = set(b[0] for b in beacons if b[1] == y)
        xs = set()
        for minx, maxx in xranges:
            xrange = range(minx, maxx + 1)
            xs.update(xrange)
        return len(xs - beacon_xs)

    def main(self, sensors, beacons, row=None):
        xranges = []
        for sensor in sensors:
            ydist = abs(sensor.y - row)
            if ydist > sensor.range:
                continue
            steps_left = sensor.range - ydist
            xrange = (sensor.x - steps_left, sensor.x + steps_left)
            xranges.append(xrange)
        return self.count_no_beacons(xranges, row, beacons)


class PartTwo(PartOne):
    def tuning_frequency(self, x, y):
        return 4_000_000 * x + y

    def find_possible(self, xranges):
        x_right = x_left = 0
        for minx, maxx in sorted(xranges):
            if x_left <= minx <= x_right:
                if maxx > x_right:
                    x_right = maxx
            else:
                return x_right + 1
        return None

    def main(self, sensors, beacons, maxX=None):
        for row in range(0, maxX + 1):
            xranges = []
            for sensor in sensors:
                ydist = abs(sensor.y - row)
                if ydist > sensor.range:
                    continue
                steps_left = sensor.range - ydist
                range_min = max(sensor.x - steps_left, 0)
                range_max = min(sensor.x + steps_left, maxX)
                xrange = (range_min, range_max)
                xranges.append(xrange)
            if (x := self.find_possible(xranges)) is not None:
                return self.tuning_frequency(x, row)
        return

if __name__ == "__main__":
    print(PartOne(DAY).run(0, row=2000000))
    print(PartTwo(DAY).run(0, maxX=4_000_000))


# TESTS

def test_part1_main():
    sol = PartOne(DAY)
    assert sol.run(1, row=10) == 26

def test_part2_main():
    sol = PartTwo(DAY)
    assert sol.run(1, maxX=20) == 56_000_011