import itertools


def parse(data):
    files = [[i] * int(n) for i, n in enumerate(data[::2])]
    gaps = [[0] * int(n) for n in data[1::2]]

    return files, gaps


def part1(data):
    files, gaps = parse(data)

    gap_i = 0

    while gap_i < len(gaps):
        gap = gaps[gap_i]

        for i in range(len(gap)):
            if not files[-1]:
                files.pop()
                gaps.pop()
            gap[i] = files[-1].pop()
        gap_i += 1
    

    all_digits = []
    for file, gap in itertools.zip_longest(files, gaps, fillvalue=[]):
        all_digits += file + gap

    return sum(i * d for i, d in enumerate(all_digits))
        

def part2(data):
    files, gaps = parse(data)

    file_i = len(files) - 1
    while file_i >= 0:
        file = files[file_i]
        for gap in gaps[:file_i]:

            if gap.count(0) >= len(file):
                first_0 = gap.index(0)
                gap[first_0:first_0 + len(file)] = file
                file[:] = [0] * len(file)
                break

        file_i -= 1

    all_digits = []
    for file, gap in itertools.zip_longest(files, gaps, fillvalue=[]):
        all_digits += file + gap

    return sum(i * d for i, d in enumerate(all_digits))


if __name__ == "__main__":
    from common import get_input

    data = get_input(day=9)

    print(part1(data))
    print(part2(data))
