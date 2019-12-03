from input import data


def sol1(data):
    res = 0
    for line in data.split():
        n = int(line) // 3 - 2
        if n > 0:
            res += n

    print(res)


def sol2(data):
    res = 0
    for line in data.split():
        n = int(line) // 3 - 2
        while n > 0:
            res += n
            n = n // 3 - 2

    print(res)


sol1(data)
sol2(data)