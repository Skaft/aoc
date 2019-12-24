from input import data
from collections import deque


def parse(string):
    cmds = []
    for line in string.splitlines():
        cmd, n = line.rsplit(maxsplit=1)
        if n == 'stack':
            cmds.append(('rev', None))
        else:
            n = int(n)
            cmds.append((cmd, n))
    return cmds

def part1():
    """
    Perform one shuffle of the deck, including every number. Return the
    index of number 2019.

    Uses deque for the reverse and rotate methods.
    """
    cards = 10_007
    nums = deque(range(cards))
    for cmd, n in instructions:
        if cmd == 'rev':
            nums.reverse()
        elif cmd == 'cut':
            nums.rotate(-n)
        else:
            i = 0
            newnums = nums.copy()
            for k in range(cards):
                newnums[i % cards] = nums[k]
                i += n
            nums = newnums
    print(nums.index(2019))

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """This code for the modular inverse (including the egcd function) was found
    on the interwebs : https://stackoverflow.com/a/9758173

    Since python 3.8, the pow builtin can be used for this, so I don't feel bad
    about not writing this myself.
    """
    g, x, y = egcd(a, m)
    return x % m

def analyse_shuffle(cards):
    """
    One shuffle is a sequence of reorderings, which come in three types. In order
    to reverse one shuffle, we need to be able to reverse each of these types.

    The cut and "deal into new stack" (I renamed it 'rev' for reverse, since that's
    what it does) are straight forward enough: reversing the deck means the index
    is mirrored, so if it is currently `i` then it was `cards - 1 - i` before.
    Cut shifts the index so and so many steps (wrapping as needed). The last one
    (deal with increment n), can be calculated in the forward direction with modulus.
    Say there's 7 cards and we deal with increment 3. Lay them down in a long
    line:
        0123456 -> 0..1..2..3..4..5..6..
    Since we wrap around every time we run out of positions, the actual position
    for each number is given by the index in the long line, modulo the number of
    cards. So the number 3 has index 9, and 9 % 7 = 2, so it goes just before the 1.
    In total we get that 0123456 -> 0..1..2
                                    ..3..4.
                                    .5..6..
                                 =  0531642
    So the forwards formula is the "long index" % number of cards. The long index
    is just the start index times the step length. So 3 ended up at index 9 since
    the step length 3 is taken 3 times: 3*3 = 9. So, when shuffling this forwards,
    the number at index i moves to index j, where `j = i*step % cards`.

    BUT, we want to reverse this process. We know where the number ended up
    (j = 2020 for the very first step), and want to find the index `i` where
    the number was before this step. From https://en.wikipedia.org/wiki/Modular_arithmetic#Properties
    (notation translated to Python):

        If ax % n = b, and a is coprime to n,
        the solution is given by x = a^(–1)b % n

    In this formula, n is the number of cards and a is the step. (The coprime req
    is probably why the number of cards is prime - no step will then *not* be
    coprime to the number of cards).

    In this context, a^-1 is the modular multiplicative inverse. Which is a number
    calculated from n and b, and there's a specific algorithm for it. Not going
    into specifics since I don't know them =) I found the code for modinv() online
    to do this for me.

    """
    coeff = 1
    shift = 0
    for cmd, n in reversed(instructions):
        if cmd == 'rev':
            coeff = -coeff
            shift = -shift + cards - 1
        elif cmd == 'cut':
            shift += n
        else:
            m = modinv(n, cards)
            coeff *= m
            shift *= m
    return coeff % cards, shift % cards

def part2():
    """
    Which number from range(cards) ends up at index 2020 after all the shuffles?

    Basic idea: Track the final index 2020 backwards. If I can find which index
    maps to 2020 on the last step, and then which index maps to that, and so on
    all the way back, then I know which number from the first step will eventually
    end up at index 2020 and that'll be the answer.

    So the first step is to figure out how to reverse one shuffle (outlined in
    analyze_shuffle()). That boils down to one `coeff` and one `shift`, such
    that the index after the shuffle (end_index = 2020) was the index
        start_index_1 = (end_index * coeff + shift) % number_of_cards
    before the one shuffle. Applying the same reverse-shuffling formula on this
    result, we find that two shuffles ago, the index was
        start_index_2 = (start_index1 * coeff + shift) % number_of_cards
                      = (end_index * coeff**2 + shift * coeff + shift) % number_of_cards
    Applying it again, we get that three shuffles ago the index was (shortening the
    variable names now):
        si3 = (si2 * c + s) % cards
            = (ei * c**3 + s * c**2 + s * c + s) % cards

    There's a pattern here to find. The result can be written as two parts:
        * The first term, `ei * c**shuffles % cards`
        * The sum (s * c**(shuffles-1) + s * c**(shuffles-2) + ... + s) % cards
    The sum is a finite geometric series, which there's a formula for:
        s * c**(n-1) + s * c**(n-2) + ... + s = s * (c**n - 1) / (c - 1)

    But this sum should be % cards. I wasn't sure how to take the modulus of a
    division, but this answer helped: https://codeforces.com/blog/entry/8323?#comment-140485

    So, that's what the code below is doing.
    """
    ei = 2020
    cards = 119315717514047
    shuffles = 101741582076661
    coeff, shift = analyse_shuffle(cards)
    first = ei * pow(coeff, shuffles, cards) % cards
    mod = cards * (coeff - 1)
    geosum = (pow(coeff, shuffles, mod) - 1) % mod
    geosum //= coeff - 1
    print((first + shift * geosum) % cards)

instructions = parse(data)
part1()
part2()
