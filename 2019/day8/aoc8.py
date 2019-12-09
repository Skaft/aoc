from input import data
from collections import Counter
import itertools as it


def segments(iterable, width):
    return [iterable[start:start + width]
            for start in range(0, len(iterable), width)]


def sol(data, wid, hei):
    layer_strings = segments(data, wid * hei)

    # part 1
    counters = [Counter(layer) for layer in layer_strings]
    layer_counts = min(counters, key=lambda x: x['0'])
    print(layer_counts['1'] * layer_counts['2'])

    # part 2
    layers = [segments(layer, wid) for layer in layer_strings]
    front = [[-1] * wid for _ in range(hei)]
    chars = {
        '0': ' ',
        '1': '█'
    }
    for row, col in it.product(range(hei), range(wid)):
        for layer in layers:
            val = layer[row][col]
            if val != '2':
                break
        front[row][col] = chars[val]

    image = '\n'.join(''.join(row) for row in front)
    print(image)


sol(data, 25, 6)