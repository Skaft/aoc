
def parse(data):
    numbers = [int(n) for n in data.strip().split()]

    return numbers

def step(value):
    if value == 0:
        return 1
    str_val = str(value)
    if len(str_val) % 2 == 0:
        mid = len(str_val) // 2
        a = int(str_val[:mid])
        b = int(str_val[mid:])
        return a, b
    return value * 2024

def evolve(n, generations, cache={}):
    if generations == 0:
        return 1

    if (n, generations) in cache:
        return cache[n, generations]

    next_gen = step(n)
    if isinstance(next_gen, tuple):
        result = sum(evolve(r, generations - 1) for r in next_gen)
    else:
        result = evolve(next_gen, generations - 1)
    cache[n, generations] = result

    return result

def part1(data):
    numbers = parse(data)

    return sum(evolve(n, generations=25) for n in numbers)


def part2(data):
    numbers = parse(data)

    return sum(evolve(n, generations=75) for n in numbers)


if __name__ == "__main__":
    from common import get_input

    data = get_input(day=11)

    print(part1(data))
    print(part2(data))
