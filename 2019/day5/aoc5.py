"""I was tired, it was early, I was stressed. Please don't look."""


from input import data


def getdigs(n):
    digs = []
    while n:
        n, d = divmod(n, 10)
        digs.append(d)
    return digs

nparams = {1:3,
           2:3,
           3:1,
           4:1,
           5:2,
           6:2,
           7:3,
           8:3,
           99:0,
}

def sol(arr, stdout=1):
    i = 0
    while True:
        pmodes, op = divmod(arr[i], 100)
        pmodes = getdigs(pmodes)
        length = nparams[op]
        params = arr[i+1: i+1+nparams[op]]
        pmodes.extend([0] * (nparams[op] - len(pmodes)))

        if op == 99:
            break
        elif op == 1:
            for idx, (pm, p) in enumerate(zip(pmodes, params[:-1])):
                if pm == 0:
                    params[idx] = arr[p]
            a, b, c = params
            arr[c] = a + b
            i += 4
        elif op == 2:
            for idx, (pm, p) in enumerate(zip(pmodes, params[:-1])):
                if pm == 0:
                    params[idx] = arr[p]
            a, b, c = params
            arr[c] = a * b
            i += 4
        elif op == 3:
            for idx, (pm, p) in enumerate(zip(pmodes, params[:-1])):
                if pm == 0:
                    params[idx] = arr[p]
            arr[params[0]] = stdout
            i += 2
        elif op == 4:
            for idx, (pm, p) in enumerate(zip(pmodes, params)):
                if pm == 0:
                    params[idx] = arr[p]
            stdout = params[0]
            i += 2
        elif op == 5:
            for idx, (pm, p) in enumerate(zip(pmodes, params)):
                if pm == 0:
                    params[idx] = arr[p]
            a, b = params
            if a:
                i = b
            else:
                i += 3
        elif op == 6:
            for idx, (pm, p) in enumerate(zip(pmodes, params)):
                if pm == 0:
                    params[idx] = arr[p]
            a, b = params
            if not a:
                i = b
            else:
                i += 3
        elif op == 7:
            for idx, (pm, p) in enumerate(zip(pmodes, params[:-1])):
                if pm == 0:
                    params[idx] = arr[p]
            a, b, c = params
            arr[c] = a < b
            i += 4
        elif op == 8:
            for idx, (pm, p) in enumerate(zip(pmodes, params[:-1])):
                if pm == 0:
                    params[idx] = arr[p]
            a, b, c = params
            arr[c] = a == b
            i += 4
        else:
            print('weird', op)
    print(stdout)

sol(data.copy(), 1)
sol(data, 5)
