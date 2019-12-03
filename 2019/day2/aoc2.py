from input import data
import itertools as it


def sol(data, noun=12, verb=2):
    arr = [int(n) for n in data.split(',')]
    arr[1] = noun
    arr[2] = verb
    i = 0
    while True:
        n, a, b, c = arr[i:i+4]
        if n == 99:
            break
        elif n == 1:
            arr[c] = arr[a] + arr[b]
        elif n == 2:
            arr[c] = arr[a] * arr[b]
        else:
            print('weird', n)
        i += 4
    return arr[0]

# part1
print(sol(data))

# part2
for n, v in it.product(range(100), range(100)):
    if sol(data, n, v) == 19690720:
        print(100*n+v)
