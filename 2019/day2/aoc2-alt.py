"""
Solving part 2 by letting sympy analyze the intcode program. By passing noun and verb as sympy Symbols, all the additions and multiplications propagates through, finally landing an expression like 288000*x + y + 394702 in the output slot. The task then becomes to find which x and y (noun and verb) that makes that expression evaluate to the target 19690720.

With this approach, only one pass of the intcode program is needed. To solve the final equation, I just noticed that divmod could be used on the coefficients for my input - don't know if that's true in general.
"""

from input import data
from sympy.abc import x, y
from sympy import Symbol


def sol(arr, noun=12, verb=2):

    arr[1] = noun
    arr[2] = verb
    i = 0
    while True:
        op, a, b, c = arr[i:i+4]

        A = a if isinstance(a, Symbol) else arr[a]
        B = b if isinstance(b, Symbol) else arr[b]

        if op == 99:
            break
        elif op == 1:
            arr[c] = A + B
        elif op == 2:
            arr[c] = A * B
        else:
            print('weird', op)
        i += 4
    return arr[0]


arr = [int(n) for n in data.split(',')]
target = 19690720
expr = sol(arr, x, y) - target

xc = int(expr.coeff(x, 1))
yc = int(expr.coeff(y, 1))
assert yc == 1
c = abs(int(expr.coeff(x, 0).coeff(y, 0)))

verb, noun = divmod(c, xc)
print(100 * verb + noun)
